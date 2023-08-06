import os
import sys
import time
import math
import gym
import torch
from typing import Tuple,List
import numpy as np
from pprint import pprint
from  torch import Tensor
from multiprocessing import Pipe,Process

class Config:
    def __init__(self,agent_class= None,env_class =None,env_args =None,if_wandb = False):
        self.num_envs =None
        self.agent_class =agent_class
        self.if_off_policy = self.get_if_off_policy()


        '''Argument of environment'''

        self.env_class =env_class
        self.env_args = env_args
        if  env_args is None:
            env_args ={"env_name":None,
                       'num_envs':1,
                       'max_steps':12345,
                       'state_dim':None,
                       'action_dim':None,
                       'if_discrete':None}
        env_args.setdefault('num_envs',1)
        env_args.setdefault('max_steps',12345)
        self.env_name =env_args['env_name']
        self.num_envs =env_args['num_envs']
        self.max_steps =env_args['max_steps']
        self.state_dim= env_args['state_dim']
        self.action_dim= env_args['action_dim']
        self.if_discrete = env_args['if_discrete']

        '''Arguments for reward shaping'''
        self.gamma =0.99
        self.reward_sclae =2**0   #调整reward大小范围

        '''Arguments for training'''
        self.net_dims =(64,32)
        self.learning_rate =6e-5
        self.clip_grad_norm =3.0
        self.state_value_tau = 0
        self.soft_update_tau  =5e-3
        self.noise_std =0.5
        if self.if_off_policy:
            self.batch_size =int(64)
            self.horizon_len = int(512)
            self.buffer_size = int(2e6)
            self.repeat_time =1.0
            self.if_use_per  =False
        else:
            self.batch_size =int(128)
            self.horizon_len =int(2048)
            self.buffer_size =None
            self.repeat_time =8.0
            self.if_use_vtrace =False
        '''Arguments for device'''
        self.gpu_id = int(0)
        self.num_workers =2
        self.num_threads =8
        self.random_seed  =0
        self.learner_gpus =0

        '''Arguments for evaluate'''
        self.cwd = None
        self.if_remove =True
        self.break_step = np.inf
        self.break_score =np.inf
        self.if_keep_save= True
        self.if_over_write = False
        self.if_save_buffer =False

        self.save_gap =int(8)
        self.eval_times =int(3)
        self.eval_per_step =int(1000)
        self.eval_env_class =None
        self.eval_env_args =None
        '''
        是否记录
        '''
        self.wandb =if_wandb

    def init_before_training(self):
        np.random.seed(self.random_seed)
        torch.manual_seed(self.random_seed)
        torch.set_num_threads(self.num_threads)
        torch.set_default_dtype(torch.float32)


        '''set cwd (current working directory) for saving model'''
        if self.cwd is None:
            self.cwd = f'./{self.env_name}_{self.agent_class.__name__[5:]}_{self.random_seed}'

        '''remove history'''
        if self.if_remove is None:
            self.if_remove =bool(input(f"| Arguments PRESS 'y' to REMOVE: {self.cwd}? ") == 'y')
        if self.if_remove:
            import shutil
            shutil.rmtree(self.cwd,ignore_errors=True)
            print(f"| Arguments Remove cwd: {self.cwd}")
        else:
            print(f"| Arguments Keep cwd: {self.cwd}")
        os.makedirs(self.cwd,exist_ok=True)
    def get_if_off_policy(self):
        agent_name = self.agent_class.__name__ if self.agent_class else ""
        on_policy_names = ('SARSA', 'VPG', 'A2C', 'TRPO', 'PPO', 'MPO')
        return all([agent_name.find(s) == -1 for s in on_policy_names])
    def print(self):

        print(vars(self))
def bulid_env(env_class = None,env_args:dict = None,gpu_id :int =-1):
    env_args['gpu_id'] =gpu_id
    if env_args.get('if_build_vec_env'):
        env =None
        pass
    elif env_class.__module__ =='gym.envs.registration':
        import gym
        assert '0.18.0' <= gym.__version__ <= '0.25.2'  # pip3 install gym==0.24.0
        gym.logger.set_level(40)  # Block warning
        env = env_class(id=env_args['env_name'])
    else:
        env =env_class(**kwargs_filter(env_class.__init__,env_args.copy()))

    env_args.setdefault('num_envs',1)
    env_args.setdefault('max_step',12345)

    for attr_str in ('env_name','num_envs','max_step','state_dim','action_dim','if_discrete'):
        setattr(env, attr_str, env_args[attr_str])
    return env

def kwargs_filter(function,kwargs:dict) -> dict:
    import  inspect
    sign =inspect.signature(function).parameters.values()
    sign ={val.name for val in  sign}
    common_args = sign.intersection(kwargs.keys())
    return {key:kwargs[key] for  key in common_args}


def get_gym_env_args(env,if_print:bool)->dict:
    import  gym
    if_gym_standard_env = {'unwrapped','observation_space','action_space','spec'}.issubset(dir(env))
    if if_gym_standard_env and (not  hasattr(env,'num_envs')):
        assert "0.18.0" <=gym.__version__ <="0.25.2"
        env_name =env.unwrapped.spec.id
        num_envs =getattr(env,'num_envs',1)
        max_step= getattr(env,'max_episode_steps',1000)

        state_shape =env.observation_space.shape
        state_dim =state_shape[0] if len( state_shape)==1 else state_shape

        if_discrete= isinstance(env.action_space,gym.spaces.Discrete)
        if if_discrete:
            action_dim = getattr(env.action_space,'n')
        elif isinstance(env.action_space,gym.spaces.Box):
            action_dim =env.action_space.shape[0]
            if any(env.action_space.high -1):
                print('WARNING: env.action_space.high:f{}'.format(env.action_space.high), env.action_space.high)
            if any(env.action_space.low+1):
                print('WARNING: env.action_space.low:f{}'.format(env.action_space.low), env.action_space.low)
        else:
            raise RuntimeError('\n| Error in get_gym_env_info(). Please set these value manually:'
                               '\n  `state_dim=int; action_dim=int; if_discrete=bool;`'
                               '\n  And keep action_space in range (-1, 1).')

    else:
        env_name = getattr(env,'env_name','env')
        num_envs =getattr(env,'num_envs',1)
        max_step =getattr(env,'max_step',1000)
        state_dim = env.state_dim
        action_dim =env.action_dim
        if_discrete =env.if_discrete



    env_args ={'env_name':env_name,
               'num_envs':num_envs,
               'max_step':max_step,
               'state_dim':state_dim,
               'action_dim':action_dim,
               'if_discrete':if_discrete

    }
    if if_print:
        env_args_str =repr(env_args).replace(',',f",\n{'':11}")
        pprint(f"env_args = {env_args_str}")
    return env_args

if __name__ =='__main__':
    x = gym.make('MountainCarContinuous-v0')
    env_args = get_gym_env_args(x, if_print=False)

    env =bulid_env(env_class=gym.make,env_args=env_args)

    from  elegantrl.agents import AgentPPO
    agent_class =AgentPPO
    config =Config(agent_class=agent_class,env_class=gym.make,env_args=env_args)
    config.print()
    x = [1,2,3,4,5,6]
    print(x[-2:])

























