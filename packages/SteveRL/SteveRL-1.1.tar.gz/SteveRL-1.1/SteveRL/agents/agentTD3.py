import torch
from typing import Tuple
from copy import deepcopy
from torch import Tensor

from SteveRL.train.config import Config
from SteveRL.train.replay_buffer import ReplayBuffer
from SteveRL.agents.agentBase import AgentBase
from SteveRL.agents.net import Actor,CriticTwin


class AgentTD3(AgentBase):

    def __init__(self,net_dims:[int],state_dim:int,action_dim:int,gpu_id:int=0,args:Config=Config()):
        self.act_class = getattr(self,'act_class',Actor)
        self.cri_class =getattr(self,'cri_class',CriticTwin)
        super().__init__(net_dims=net_dims,state_dim=state_dim,action_dim=action_dim,gpu_id=gpu_id,args=args)
        self.act_target =deepcopy(self.act)
        self.cri_target =deepcopy(self.cri)

        self.explore_noise_std =getattr(args,'explore_noise_std',0.05)
        self.policy_noise_std =getattr(args,'policy_noise_std',0.10)
        self.updata_freq = getattr(args,'update_freq',2)

        self.act.explore_noise_std =self.explore_noise_std
    def update_net(self, buffer:ReplayBuffer) -> Tuple[float, ...]:
        with torch.no_grad():
            states,actions,rewards,undones =buffer.add_item
            self.update_avg_std_for_normalization(
                states=states.reshape((-1,self.state_dim)),
                returns=self.get_cumulative_rewards(rewards=rewards,undones=undones).reshape((-1,))
            )

        obj_critics =0.0
        obj_actors= 0.0
        update_times =int(buffer.add_size*self.repeat_times)
        assert  update_times>=1
        for update_c  in range(update_times):
            obj_critic,state = self.get_obj_critic(buffer,self.batch_size)
            obj_critics+=obj_critic.item()
            self.optimzer_update(self.cri_optimizer,obj_critic)
            self.soft_update(self.cri_target,self.cri,self.soft_update_tau)

            if update_c %self.updata_freq ==0:
                action_pg =self.act(state)
                obj_actor =self.cri_target(state,action_pg).mean()
                obj_actors+=obj_actor.item()
                self.optimzer_update(self.act_optimizer,-obj_actor)
                self.soft_update(self.act_target,self.act,self.soft_update_tau)
        return obj_critics/update_times,obj_actors/update_times







