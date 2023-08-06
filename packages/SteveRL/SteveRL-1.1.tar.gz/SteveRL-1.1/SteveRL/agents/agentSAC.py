import math
import torch
from typing import Tuple
from copy import deepcopy
from torch import Tensor

from SteveRL.agents.agentBase import AgentBase
from SteveRL.agents.net import ActorSAC,CriticTwin
from SteveRL.train.config import Config
from SteveRL.train.replay_buffer import ReplayBuffer


class AgentSAC(AgentBase):
    def __init__(self,net_dims:[int],state_dim:int,action_dim:int,gpu_id:int=0,args:Config=Config()):
        self.act_class =getattr(self,'act_class',ActorSAC)
        self.cri_class =getattr(self,'cri_class',CriticTwin)
        super().__init__(net_dims=net_dims,state_dim=state_dim,action_dim=action_dim,gpu_id=gpu_id,args=args)
        self.cri_target = deepcopy(self.cri)

        self.alpha_log = torch.tensor((-1,),dtype=torch.float32,requires_grad=True,device=self.devcie)
        self.alpha_optimizer =torch.optim.AdamW((self.alpha_log,),lr=self.learning_rate*4)
        self.target_entopy =getattr(args,'target_entropy',action_dim)

    def update_net(self,buffer:ReplayBuffer):
        with torch.no_grad():
            states,actions,rewards,undones =buffer.add_item
            self.update_avg_std_for_normalization(
                states=states.reshape((-1,self.state_dim)),
                returns=self.get_cumulative_rewards(rewards=rewards,undones=undones).reshape((-1,))

            )

            obj_critics =0.0
            obj_actors =0.0
            alphas =0.0

            update_times = int(buffer.add_size*self.repeat_times)

            assert update_times >=1
            for _ in range(update_times):
                obj_critic,state =self.get_obj_critic(buffer,self.batch_size)
                obj_critics+=obj_critic.item()

                self.optimzer_update(self.cri_optimizer,obj_critic)
                self.soft_update(self.cri_target,self.cri,self.soft_update_tau)

                action_pg,log_prob = self.act.get_action_logprob(state)
                obj_alpha = (self.alpha_log*(self.target_entopy -log_prob).detach()).mean()

                self.optimzer_update(self.alpha_optimizer,obj_alpha)

                alpha = self.alpha_log.exp().detach()
                alphas+=alpha
                with torch.no_grad():
                    self.alpha_log[:] =self.alpha_log.clamp(-16,2)
                q_value_pg=self.cri_target(state,action_pg).mean()
                obj_actor = (q_value_pg - log_prob*alpha).mean()

                self.optimzer_update(self.act_optimizer,-obj_actor)
            return obj_critics/update_times,obj_actors/update_times,alphas/update_times



