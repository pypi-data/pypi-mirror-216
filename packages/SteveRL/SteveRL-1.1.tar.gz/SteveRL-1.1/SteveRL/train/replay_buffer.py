import os
import math
import torch
from typing import Tuple
from  torch import Tensor
import numpy as np

from SteveRL.train.config import Config

class ReplayBuffer():
    def __init__(self,
                 max_size:int,
                 state_dim:int,
                 action_dim:int,
                 gpu_id:int=0,
                 num_seqs:int=1,
                 if_use_per:int=False,
                 args:Config =Config()):

        self.p =0
        self.if_full =False
        self.cur_size =0
        self.add_size =0
        self.add_item = None

        self.max_size =max_size
        self.num_seqs =num_seqs
        self.device =torch.device(f'cuda:{gpu_id}' if (torch.cuda.is_available() and (gpu_id>=0)) else "cpu")


        self.states = torch.empty((max_size,num_seqs,state_dim),dtype=torch.float32,device=self.device)
        self.actions= torch.empty((max_size,num_seqs,action_dim),dtype=torch.float32,device=self.device)
        self.rewards =torch.empty((max_size,num_seqs),dtype=torch.float32,device=self.device)
        self.undones =torch.empty((max_size,num_seqs),dtype=torch.float32,device=self.device)


        self.if_use_per =if_use_per
        if self.if_use_per:
            # self.sum_trees = [SumTree(buf_len =max_size) for  _ in range(num_seqs)]
            # self.per_alpha =getattr(args,'per_alpha',0.6)
            # self.per_beta =getattr(args,'per_beta',0.4)
            pass

        else:
            self.sum_trees =None
            self.per_alpha =None
            self.per_beta =None
    def update(self,items:Tuple[Tensor,...]):
        self.add_item =items
        states,actions,rewards,undones =items
        self.add_size =rewards.shape[0]

        p  =self.p +self.add_size
        if p >self.max_size:
            self.if_full =True
            p0 = self.p
            p1 = self.max_size
            p2  =self.max_size-self.p
            p =p -self.max_size

            self.states[p0:p1],self.states[0:p] = states[:p2],states[-p:]
            self.actions[p0:p1],self.actions[0:p] =actions[:p2],states[-p:]
            self.rewards[p0:p1], self.rewards[0:p] = rewards[:p2], rewards[-p:]
            self.undones[p0:p1], self.undones[0:p] = undones[:p2], undones[-p:]
        else:

            self.states[self.p:p] = states
            self.actions[self.p:p] =actions
            self.rewards[self.p:p] =rewards
            self.undones[self.p:p] =undones

        if self.if_use_per:
            'data_ids for single env'
            data_ids =torch.arange(self.p,p,dtype=torch.long,device=self.device)
            if p >self.max_size:
                data_ids =torch.fmod(data_ids,self.max_size)

            for sum_tree in self.sum_trees:
                sum_tree.update_ids(data_ids=data_ids.cpu(),prob=10.)

        self.p =p
        self.cur_size =self.max_size  if self.if_full else self.p

    def sample(self,batch_size:int)-> Tuple[Tensor,Tensor,Tensor,Tensor,Tensor]:
        sample_len =self.cur_size-1
        ids =torch.randint(sample_len*self.num_seqs,size =(batch_size,),requires_grad=False)
        ids0 =torch.fmod(ids,sample_len)
        ids1 =torch.div(ids,sample_len,rounding_mode='floor')

        return (self.states[ids0,ids1],
                self.actions[ids0,ids1],
                self.rewards[ids0,ids1],
                self.undones[ids0,ids1],
                self.states[ids0+1,ids1])


    def sample_for_per(self,batch_size:int):
        pass






if __name__ =='__main__':
    pass


























