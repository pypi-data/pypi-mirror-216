import os
import sys
import time
import torch
import numpy as np
import torch.multiprocessing as mp  # torch.multiprocessing extends multiprocessing of Python
from copy import deepcopy
from multiprocessing import Process, Pipe

from SteveRL.train.evaluator import Evaluator
from SteveRL.train.config import Config,bulid_env

from SteveRL.train.replay_buffer import ReplayBuffer

if os.name == 'nt':  # if is WindowOS (Windows NT)
    """Fix bug about Anaconda in WindowOS
    OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
    """
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def train_agent(args:Config):
    args.init_before_training()
    torch.set_grad_enabled(False)
    '''init environment'''
    env = bulid_env(args.env_class, args.env_args, args.gpu_id)

    '''init agent'''
    agent =args.agent_class(args.net_dims,args.state_dim,args.action_dim,gpu_id=args.gpu_id,args=args)


    state =env.reset()

    if args.num_envs ==1:
        assert  state.shape ==(args.state_dim,)
        assert isinstance(state,np.ndarray)
        state =torch.tensor(state,dtype=torch.float32,device=agent.device).unsqueeze(0)
    else:
        pass

    assert state.shape == (args.num_envs, args.state_dim)
    assert isinstance(state,torch.Tensor)
    agent.last_state =state.detach()

    '''init buffer'''
    if args.if_off_policy:
        buffer = ReplayBuffer(
            gpu_id=args.gpu_id,
            num_seqs=args.num_envs,
            max_size=args.buffer_size,
            state_dim=args.state_dim,
            action_dim=1 if args.if_discrete else args.action_dim,
            if_use_per=args.if_use_per,
            args=args,
        )
        buffer_items =agent.explore_env(env,args.horizon_len*args.eval_times,if_random=True)
        buffer.update(buffer_items)
    else:
        buffer =[]

    '''
    init_evaluator
    '''
    eval_env_class =args.eval_env_class if args.eval_env_class else args.env_class
    eval_env_args =args.eval_env_args if args.eval_env_args else args.env_args
    eval_env = bulid_env(eval_env_class,eval_env_args,args.gpu_id)
    evaluator =Evaluator(cwd=args.cwd,env= eval_env,args=args)


    break_step =args.break_step
    horizon_len =args.horizon_len
    if_off_policy =args.if_off_policy
    if_save_buffer= args.if_save_buffer
    del args

    if_train =True
    steps =0
    while if_train:
        buffer_items =agent.explore_env(env,horizon_len)

        exp_r =buffer_items[2].mean().item()
        if if_off_policy:
            buffer.update(buffer_items)
        else:
            buffer[:] =buffer_items

        steps+=horizon_len
        torch.set_grad_enabled(True)
        logging_tuple =agent.update_net(buffer)
        torch.set_grad_enabled(False)
        evaluator.evaluate_and_save(actor=agent.act,steps=horizon_len,exp_r=exp_r,logging_tuple=logging_tuple)

        if_train = (break_step>steps)


    env.close()
    print(f'|UsedTime:{time.time() - evaluator.start_time}')







