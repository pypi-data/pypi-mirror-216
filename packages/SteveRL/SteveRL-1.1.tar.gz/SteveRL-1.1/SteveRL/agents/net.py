import math
import torch
import torch.nn as nn
from torch import Tensor
from torch.distributions.normal import Normal

"""DQN"""


class QNetBase(nn.Module):
    def __init__(self, state_dim: int, action_dim: int):
        super().__init__()
        self.explore_rate = 0.125

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.net = None

        self.state_avg = nn.Parameter(torch.zeros((state_dim,)), requires_grad=False)
        self.state_std = nn.Parameter(torch.zeros((state_dim,)), requires_grad=False)
        self.value_avg = nn.Parameter(torch.zeros((1,)), requires_grad=False)
        self.value_std = nn.Parameter(torch.zeros((1,)), requires_grad=False)

    def state_norm(self, state: Tensor) -> Tensor:
        return (state - self.state_avg) / self.state_std

    def value_re_norm(self, value: Tensor) -> Tensor:
        return (value - self.value_avg) / self.value_std

class QNet(QNetBase):
    def __init__(self,dims:[int],state_dim:int,action_dim:int):
        super().__init__(state_dim=state_dim,action_dim=action_dim)
        self.net = bulid_mlp(dims=[state_dim,*dims,action_dim])
        layer_init_with_orthogonal(self.net[-1],std=0.5)
    def forward(self,state):
        state = self.state_norm(state)
        value = self.net(state)
        value =self.value_re_norm(value)
        return value

    def gete_action(self,state):
        state = self.state_norm(state)
        if self.explore_rate <torch.rand(1):
            action =self.net(state).argmax(dim=1,keepdim=True)
        else:
            action =torch.randint(self.action_dim,size=(state.shape[0],1))
        return action
class QNetDuel(QNetBase):
    def __init__(self,dims:[int],state_dim:int,action_dim:int):
        super().__init__(state_dim=state_dim,action_dim=action_dim)
        self.net_state = bulid_mlp(dims=[state_dim,*dims])
        self.net_adv = bulid_mlp(dims[-1],1)
        self.net_val = bulid_mlp(dims=[dims[-1],action_dim])

        layer_init_with_orthogonal(self.net_val[-1],std=0.1)
        layer_init_with_orthogonal(self.net_adv[-1],std=0.1)

    def forward(self,state):
        state = self.state_norm(state)
        s_enc =self.net_state(state)
        q_val =self.net_val(s_enc)
        q_adv =self.net_adv(s_enc)

        value = q_val  -q_val.mean(dim =1,keepdim=True) +q_adv
        value = self.value_re_norm(value)
        return value
    def get_action(self,state):
        state = self.state_norm(state)
        if self.explore_rate < torch.rand(1):
            s_env =self.net_state(state)
            q_val =self.net_val(s_env)
            action = q_val.argmax(dim=1,keepdim=True)
        else:
            action = torch.randint(self.action_dim,size=(state.shape[0],1))
        return action

class QnetTwin(QNetBase):
    def __init__(self,dims:[int],state_dim:int,action_dim:int):
        super().__init__(state_dim=state_dim,action_dim=action_dim)
        self.net_state =bulid_mlp(dims=[state_dim,*dims])
        self.net_val1 = bulid_mlp(dims=[dims[-1],action_dim])
        self.net_val2= bulid_mlp(dims=[dims[-1],action_dim])

        self.soft_max  =nn.Softmax(dim=1)

        layer_init_with_orthogonal(self.net_val1[-1],std=0.1)
        layer_init_with_orthogonal(self.net_val2[-2],std=0.1)

    def forward(self,state):
        state= self.state_norm(state)
        s_enc =self.net_state(state)
        q_val = self.net_val1(s_enc)
        return q_val
    def get_q1_q2(self,state):
        state = self.state_norm(state)
        s_enc = self.net_state(state)
        q_val1 =self.net_val1(s_enc)
        q_val1 = self.value_re_norm(q_val1)
        q_val2 =self.net_val2(s_enc)
        q_val2 = self.value_re_norm(q_val2)

        return q_val1,q_val2
    def get_action(self,state):
        state =self.state_norm(state)
        s_enc =self.net_state(state)
        q_val =self.net_val1(s_enc)
        if self.explore_rate <torch.rand(1):
            action =q_val.argmax(dim =1,keepdim=True)
        else:
            a_prob  =self.soft_max(q_val)
            action =torch.multinomial(a_prob,num_samples=1)
        return action

class QnetTwinDuel(QNetBase):
    def __init__(self,dims:[int],state_dim:[int],action_dim:int):
        super().__init__(state_dim=state_dim,action_dim=action_dim)
        self.net_state =bulid_mlp(dims=[state_dim,*dims])
        self.net_adv1 = bulid_mlp(dims=[dims[-1],1])
        self.net_val1 =bulid_mlp(dims=[dims[-1],action_dim])
        self.net_adv2 = bulid_mlp(dims=[dims[-1], 1])
        self.net_val2 = bulid_mlp(dims=[dims[-1], action_dim])
        self.soft_max =nn.Softmax(dim=1)

        layer_init_with_orthogonal(self.net_adv1[-1],std=0.1)
        layer_init_with_orthogonal(self.net_val1[-1], std=0.1)
        layer_init_with_orthogonal(self.net_adv2[-1], std=0.1)
        layer_init_with_orthogonal(self.net_val2[-1], std=0.1)

    def forward(self,state):
        state =self.state_norm(state)
        s_enc =self.net_state(state)
        q_val =self.net_val1(s_enc)
        q_adv =self.net_adv1(q_val)
        value =q_val - q_val.mean(dim =1,keepdim =True)+q_adv
        value =self.value_re_norm(value)

        return value
    def get_q1_q2(self,state):
        state =self.state_norm(state)
        s_enc =self.net_state(state)

        q_val1= self.net_val1(s_enc)
        q_adv1 = self.net_adv1(q_val1)

        q_duel1 =q_val1 - q_val1.mean(dim =1,keepdim =True)+q_adv1
        q_duel1 = self.value_re_norm( q_duel1)

        q_val2 = self.net_val2(s_enc)
        q_adv2 = self.net_adv2(q_val1)
        q_duel2 = q_val2 - q_val2.mean(dim=1, keepdim=True) + q_adv2
        q_duel2 = self.value_re_norm(q_duel2)
        return q_duel1,q_duel2

    def get_action(self,state):
        state =self.state_norm(state)
        s_enc =self.net_state(state)
        q_val =self.net_val1(s_enc)
        if self.explore_rate <torch.rand(1):
            action = q_val.argmax(dim=1,keepdim=True)
        else:
            a_prob =self.soft_max(q_val)
            action =torch.multinomial(a_prob,num_samples=1)
        return action












"""Actor (policy network)"""


class ActorBase(nn.Module):
    def __init__(self, state_dim: int, action_dim: int):
        super().__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.net = None
        self.explore_noise_std = None
        self.ActionDist = torch.distributions.normal.Normal

        self.state_avg = nn.Parameter(torch.zeros((state_dim,)), requires_grad=False)
        self.state_std = nn.Parameter(torch.ones((state_dim,)), requires_grad=False)

    def state_norm(self, state: Tensor) -> Tensor:
        x = self.state_std
        y = self.state_avg
        return (state - self.state_avg) / self.state_std


class Actor(ActorBase):
    def __init__(self, dims: [int], state_dim: int, action_dim: int):
        super().__init__(state_dim=state_dim, action_dim=action_dim)
        self.net = bulid_mlp(dims=[state_dim, *dims, action_dim])
        layer_init_with_orthogonal(self.net[-1], std=0.1)
        self.explore_noise_std = 0.1

    def forward(self, state: Tensor) -> Tensor:
        state = self.state_norm(state)
        return self.net(state).tanh()

    def get_action(self, state: Tensor) -> Tensor:
        state = self.state_norm(state)
        action = self.net(state).tanh()
        noise = (torch.randn_like(action) * self.explore_noise_std).clamp(-0.5, 0.5)
        return (action + noise).clamp(-1, 1)

    def get_action_noise(self, state: Tensor, action_std: float) -> Tensor:
        state = self.state_norm(state)
        action = self.net(state).tanh()
        noise = (torch.randn_like(action) * action_std).clamp(-1, 1)
        return (action + noise).clamp(-1, 1)


class ActorPPO(ActorBase):
    def __init__(self, dims: [int], state_dim: int, action_dim: int):
        super().__init__(state_dim=state_dim, action_dim=action_dim)
        self.net = bulid_mlp(dims=[state_dim, *dims, action_dim])
        layer_init_with_orthogonal(self.net[-1], std=0.1)

        self.action_std_log = nn.Parameter(torch.zeros((1, action_dim)), requires_grad=True)

    def forward(self, state: Tensor) -> Tensor:
        state = self.state_norm(state)
        return self.net(state).tanh()

    def get_action(self, state: Tensor) -> (Tensor, Tensor):
        state = self.state_norm(state)
        action_avg = self.net(state)
        action_std = self.action_std_log.exp()

        dist = self.ActionDist(action_avg, action_std)
        action = dist.sample()
        logprob = dist.log_prob(action).sum(1)
        return action, logprob

    def get_logprob_entropy(self, state: Tensor, action: Tensor) -> (Tensor, Tensor):
        state = self.state_norm(state)
        action_avg = self.net(state)
        action_std = self.action_std_log.exp()
        dist = self.ActionDist(action_avg, action_std)
        logprob = dist.log_prob(action).sum(1)
        entropy = dist.entropy().sum(1)
        return logprob, entropy


    @staticmethod
    def convert_action_for_env(action: Tensor) -> Tensor:
        return action.tanh()



class ActorSAC(ActorBase):
    def __init__(self,dims:[int],state_dim:int,action_dim:int):
        super().__init__(state_dim=state_dim,action_dim=action_dim)
        self.net_s =bulid_mlp(dims=[state_dim,*dims],if_raw_out=False)
        self.net_a = bulid_mlp([dims[-1],action_dim*2])

        layer_init_with_orthogonal(self.net_a[-1],std=0.1)

    def forward(self,state):
        state =self.state_norm(state)
        s_enc =self.net_s(state)
        a_avg =self.net_a(s_enc)[:,:self.action_dim]
        return a_avg.tanh()

    def get_action(self,state):
        state = self.state_norm(state)
        s_enc =self.net_s(state)
        a_avg,a_std_log = self.net_a(s_enc).chunk(2,dim=1)
        a_std =a_std_log.clamp(-16,2).exp()
        dist = Normal(a_avg,a_std)

        return dist.rsample().tanh()

    def get_action_logprob(self,state):
        state = self.state_norm(state)
        s_enc =self.net_s(state)
        a_avg,a_std_log =self.net_a(s_enc).chunk(2,dim=1)
        a_std  =a_std_log.clamp(-16,2).exp()

        dist = Normal(a_avg,a_std)
        action =dist.rsample()
        action_tanh =action.tanh()
        logprob =dist.log_prob(a_avg)
        logprob -= (action_tanh.pow(2)+1.0000001).log()

        return action_tanh,logprob.sum(1)






"""Critic (value network)"""


class CriticBase(nn.Module):
    def __init__(self, state_dim: int, action_dim: int):
        super().__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.net = None

        self.state_avg = nn.Parameter(torch.zeros((state_dim,)), requires_grad=False)
        self.state_std = nn.Parameter(torch.ones((state_dim,)), requires_grad=False)
        self.value_avg = nn.Parameter(torch.zeros((1,)), requires_grad=False)
        self.value_std = nn.Parameter(torch.ones((1,)), requires_grad=False)

    def state_norm(self, state: Tensor) -> Tensor:
        return (state - self.state_avg) / self.state_std  # todo state_norm

    def value_re_norm(self, value: Tensor) -> Tensor:
        return value * self.value_std + self.value_avg  # todo value_norm


class Critic(CriticBase):
    def __init__(self, dims: [int], state_dims: int, action_dims: int):
        super().__init__(state_dim=state_dims, action_dim=action_dims)
        self.net = bulid_mlp(dims=[state_dims + action_dims, *dims, 1])

        layer_init_with_orthogonal(self.net[-1], std=0.5)

    def forward(self, state: Tensor, action: Tensor) -> Tensor:
        state = self.state_norm(state)
        values = self.net(torch.clamp(state, action), dim=1)
        values = self.value_re_norm(values)
        return values.squeeze(dim=1)


class Critic_PPO(CriticBase):
    def __init__(self, dims: [int], state_dims: int, action_dims: int):
        super().__init__(action_dim=action_dims, state_dim=state_dims)
        self.net = bulid_mlp(dims=[state_dims, *dims, 1])
        layer_init_with_orthogonal(self.net[-1], std=0.5)

    def forward(self, state: Tensor) -> Tensor:
        state = self.state_norm(state)
        value = self.net(state)
        value = self.value_re_norm(value)
        return value.squeeze(1)

class CriticTwin(CriticBase):
    def __init__(self,dims:[int],state_dim:int,action_dim:int):
        super().__init__(state_dim=state_dim,action_dim=action_dim)
        self.net =bulid_mlp(dims= [state_dim+action_dim,*dims,2])
        layer_init_with_orthogonal(self.net[-1],std=0.5)

    def forward(self,state,action):
        state  =self.state_norm(state)

        values =self.net(torch.cat((state,action),dim=1))
        values = self.value_re_norm(values)
        return values.mean(dim=1)
    def get_q_min(self,state,action):
        state =self.state_norm(state)
        values= self.net(torch.cat((state,action),dim=1))
        values =self.value_re_norm(values)
        return torch.min(values,dim=1)[0]
    def get_q1_q2(self,state,action):
        state =self.state_norm(state)
        values =self.net(torch.cat((state,action),dim=1))
        values =self.value_re_norm(values)
        return values[:,0],values[:,1]







def bulid_mlp(dims: [int], activation: nn = None, if_raw_out: bool = True) -> nn.Sequential:
    if activation is None:
        activation = nn.ReLU
    net_list = []
    for i in range(len(dims) - 1):
        net_list.extend([nn.Linear(dims[i], dims[i + 1]), activation()])
    if if_raw_out:
        del net_list[-1]  # delete the activation function of the output layer to keep raw output
    return nn.Sequential(*net_list)


def layer_init_with_orthogonal(layer, std=1.0, bias_const=1e-6):
    '''
    初始化网络参数
    '''
    torch.nn.init.orthogonal_(layer.weight, std)
    torch.nn.init.constant_(layer.bias, bias_const)


if __name__=='__main__':
    pass

