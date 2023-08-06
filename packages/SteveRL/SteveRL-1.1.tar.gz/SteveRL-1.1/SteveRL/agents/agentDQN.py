import torch
from typing import Tuple
from copy import deepcopy
from torch import Tensor

from SteveRL.agents.agentBase import AgentBase
from SteveRL.agents.net import QNet,QNetDuel
from SteveRL.agents.net import QnetTwin,QnetTwinDuel
from SteveRL.train.config import Config
from SteveRL.train.replay_buffer import ReplayBuffer

class AgentDQN(AgentBase):
    def __init__(self,net_dims:[int],state_dim:int,action_dim:int,gpu_id:int=0,args:Config= Config()):
        self.act_class =getattr(self,'act_class',QNet)
        self.cri_class =None
        super().__init__(net_dims=net_dims,state_dim=state_dim,action_dim=action_dim,gpu_id=gpu_id,args=args)
        self.act_target =self.cri_target =deepcopy(self.act)

        self.act.explore_rate = getattr(args,'explore_rate',0.25)
    def explore_one_env(self, env, horizon_len: int, if_random: bool = False) -> Tuple[Tensor, ...]:
        states =torch.zeros((horizon_len,self.num_envs,self.state_dim),dtype=torch.float32).to(self.devcie)
        actions =torch.zeros((horizon_len,self.num_envs,1),dtype=torch.int32).to(self.devcie)
        rewards =torch.zeros((horizon_len,self.num_envs),dtype=torch.float32).to(self.devcie)
        dones =torch.zeros((horizon_len,self.num_envs),dtype=torch.bool).to(self.devcie)

        state =self.last_state

        get_action =self.act.get_action
        for t in  range(horizon_len):
            action = torch.randint(self.action_dim,size=(1,1)) if if_random else get_action(state)
            states[t] =state
            ary_action =action[0,0].detach().cpu().numpy()
            ary_state,reward,done,_ = env.step(ary_action)
            ary_state = env.reset() if done else ary_state
            state =torch.as_tensor(ary_state,dtype=torch.float32,device=self.devcie).unsqueeze(0)
            actions[t] =action
            rewards[t] =reward
            dones[t] =done

        self.last_state = state
        rewards*=self.reward_scale
        undones =1.0 -dones.type(torch.float32)
        return states,actions,rewards,undones

    def update_net(self, buffer:ReplayBuffer) -> Tuple[float, ...]:
        with torch.no_grad():
            states,actions,rewards, undons =buffer.add_item
            self.update_avg_std_for_normalization(
                states= states.reshape((-1,self.state_dim)),
                returns= self.get_cumulative_rewards(rewards=rewards,undones=undons).reshape((-1,))

            )

        obj_critics =0.0
        obj_actors =0.0

        update_times =int(buffer.add_size*self.repeat_times)
        assert update_times >=1
        for _ in range(update_times):
            obj_critic,q_value =self.get_obj_critic(buffer,self.batch_size)
            obj_critics+=obj_critic.item()
            obj_actors+=q_value.mean().item()
            self.optimzer_update(self.cri_optimizer,obj_critic)
            self.soft_update(self.cri_target,self.cri,self.soft_update_tau)
        return obj_critics/update_times,obj_actors/update_times

class AgentDoubleDQN(AgentDQN):
    def __init__(self,net_dims:[int],state_dim:int,action_dim:int,gpu_id:int=0,args: Config =Config()):
        self.act_class =getattr(self,'act_class',QnetTwin)
        self.cri_class =getattr(self,'cri_class',None)
        super().__init__(net_dims=net_dims,state_dim=state_dim,action_dim=action_dim,gpu_id=gpu_id,args=args)

    def get_obj_critic_raw(self, buffer: ReplayBuffer, batch_size: int) -> Tuple[Tensor, Tensor]:
        with torch.no_grad():
            states,actions,rewards,undones ,next_ss =buffer.sample(batch_size)
            next_qs =torch.min(*self.cri_target.get_q1_q2(next_ss)).max(dim=1,keepdim=True)[0].squeeze(1)
            q_labels =rewards+undones*self.gamma*next_qs
        q1,q2 =[qs.gather(1,actions.long()).squeeze(1)   for qs in self.act.get_q1_q2(states)]
        obj_critic =self.criterion(q1,q_labels)+self.criterion(q2,q_labels)
        return obj_critic,q1


class AgentDuelingDQN(AgentDQN):
    def __init__(self,net_dims:[int],state_dim:int,action_dim:int,gpu_id:int=0,args:Config =Config()):
        self.act_class =getattr(self,'act_class',QNetDuel)
        self.cri_class =getattr(self,'cri_class',None)
        super().__init__(net_dims=net_dims,state_dim=state_dim,action_dim=action_dim,gpu_id=gpu_id,args=args)
class AgentD3QN(AgentDoubleDQN):
    def __init__(self,net_dims:[int],state_dim:int,action_dim:int,gpu_id:int=0,args:Config =Config()):
        self.act_class =getattr(self,'act_class',QnetTwinDuel)
        self.cri_class =getattr(self,'cri_class',None)
        super().__init__(net_dims=net_dims,state_dim=state_dim,action_dim=action_dim,gpu_id=gpu_id,args=args)






