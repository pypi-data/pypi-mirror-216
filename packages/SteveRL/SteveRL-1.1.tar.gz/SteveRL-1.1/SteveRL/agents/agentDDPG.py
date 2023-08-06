import numpy as np
import numpy.random as rd
import torch
from copy import deepcopy
from typing import Tuple
from torch import  Tensor

from SteveRL.train.config import Config
from SteveRL.train.replay_buffer import ReplayBuffer
from SteveRL.agents.agentBase import AgentBase
from SteveRL.agents.net import Actor,Critic



class AgentDDPG(AgentBase):

    def __init__(self,net_dims:[int],state_dim:int,action_dim:int,gpu_id:int=0,args:Config=Config()):
        self.act_class =getattr(self,'act_class',Actor)
        self.cri_class =getattr(self,'cri_class',Critic)
        super().__init__(state_dim=state_dim,action_dim=action_dim,gpu_id=gpu_id,args=args,net_dims=net_dims)
        self.act_target = deepcopy(self.act)
        self.cri_target =deepcopy(self.cri)

        self.explore_noise_std =getattr(args,'explore_noise_std',0.05)

        self.act.explore_noise_std =self.explore_noise_std
    def update_net(self, buffer:ReplayBuffer) -> Tuple[float, ...]:
        with torch.no_grad:
            states,actions,rewards,undones =buffer.add_item
            self.update_avg_std_for_normalization(
                states=states.reshape((-1,self.state_dim)),
                returns=self.get_cumulative_rewards(rewards=rewards,undones=undones).reshape((-1,))
            )

        obj_critics =0.0
        obj_actors =0.0
        update_times= int(buffer.add_size*self.repeat_times)
        assert  update_times>=1
        for update_c in range(update_times):
            obj_critic,state = self.get_obj_critic(buffer,self.batch_size)
            obj_critics+=obj_critic.item()
            self.optimzer_update(self.cri_optimizer,obj_critic)
            self.soft_update(self.cri_target,self.cri,self.soft_update_tau)

            action_pg =self.act(state)
            obj_actor =self.cri_target(state,action_pg).mean()
            obj_actors+=obj_actor.item()
            self.optimzer_update(self.act_optimizer,-obj_actor)
            self.soft_update(self.act_target,self.act,self.soft_update_tau)
        return obj_critics/update_times,obj_actors/update_times

    def get_cumulative_rewards(self,rewards:Tensor,undones:Tensor)->Tensor:
        returns =torch.empty_like(rewards)

        masks = undones*self.gamma

        horizon_len =rewards.shape[0]

        last_state =self.last_state
        next_action = self.act_target(last_state)
        next_value = self.cri_target(last_state,next_action).detach()
        for t in range(horizon_len-1,-1,-1):
            returns[t] = next_value =rewards[t]+masks*next_value
        return returns

class OrnsteinUhlenbeckNoise:
    def __init__(self,size:int,theta =0.15,sigma= 0.3,ou_noise =0.0,dt= 1e-2):
        self.theta =theta
        self.sigma =sigma
        self.ou_noise =ou_noise
        self.dt =dt
        self.size =size


    def __call__(self, *args, **kwargs):
        noise =self.sigma*np.sqrt(self.dt)*rd.normal(size=self.size)
        self.ou_noise -=self.theta*self.ou_noise*self.dt+noise
        return self.ou_noise





