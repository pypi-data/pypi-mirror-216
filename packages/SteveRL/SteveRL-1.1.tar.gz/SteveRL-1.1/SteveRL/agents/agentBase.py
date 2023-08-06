import os
import torch
from typing import Tuple, Union

import wandb
from torch.nn.utils import clip_grad_norm_
from SteveRL.train.config import Config
from SteveRL.train.replay_buffer import ReplayBuffer
from torch import Tensor


class AgentBase:

    def __init__(self, net_dims: [int], state_dim: int, action_dim: int, gpu_id: int = 0, args: Config = Config()):
        self.gamma = args.gamma
        self.num_envs = args.num_envs
        self.batch_size = args.batch_size
        self.repeat_times = args.repeat_time
        self.reward_scale = args.reward_sclae
        self.learning_rate = args.learning_rate
        self.if_off_polciy = args.if_off_policy
        self.clip_grad_norm = args.clip_grad_norm
        self.soft_update_tau = args.soft_update_tau
        self.state_value_tau = args.state_value_tau

        self.state_dim = args.state_dim
        self.action_dim = args.action_dim
        self.last_state = None
        self.logging_reward = 0

        self.device = torch.device(f'cuda:{gpu_id}' if (torch.cuda.is_available() and gpu_id >= 0) else 'cpu')

        'network'

        act_class = getattr(self, 'act_class', None)
        cri_class = getattr(self, 'cri_class', None)

        self.act = self.act_target = act_class(net_dims, state_dim, action_dim).to(self.device)
        self.cri = self.cri_target = cri_class(net_dims, state_dim, action_dim).to(self.device) \
            if cri_class else self.act

        '''optimizer'''
        self.act_optimizer = torch.optim.AdamW(self.act.parameters(), self.learning_rate)
        self.cri_optimizer = torch.optim.AdamW(self.cri.parameters(), self.learning_rate) \
            if cri_class else self.act_optimizer
        from types import MethodType
        self.act_optimizer.parameters = MethodType(get_optim_param, self.act_optimizer)
        self.cri_optimizer.parameters = MethodType(get_optim_param, self.cri_optimizer)
        """ recoder    """
        self.wandb = args.wandb

        """attribute"""
        if self.num_envs == 1:
            self.explore_env = self.explore_one_env
        else:
            pass

        self.if_use_per = getattr(args, 'if_use_per', None)
        if self.if_use_per:
            pass
        else:
            self.criterion = torch.nn.SmoothL1Loss(reduction='mean')
            self.get_obj_critic = self.get_obj_critic_raw

        self.save_attr_names = {'act', 'act_target', 'act_optimizer', 'cri', 'cri_target', 'cri_optimizer'}

    def explore_one_env(self, env, horizon_len: int, if_random: bool = False) -> Tuple[Tensor, ...]:
        states = torch.zeros((horizon_len, self.num_envs, self.state_dim), dtype=torch.float32).to(self.device)
        actions = torch.zeros((horizon_len, self.num_envs, self.action_dim), dtype=torch.float32).to(self.device)
        rewards = torch.zeros((horizon_len, self.num_envs), dtype=torch.float32).to(self.device)
        dones = torch.zeros((horizon_len, self.num_envs), dtype=torch.bool).to(self.device)

        state = self.last_state

        get_action = self.act.get_action

        for t in range(horizon_len):

            action = torch.rand(1, self.action_dim) * 2 - 1.0 if if_random else get_action(state)
            states[t] = state
            ary_action = action[0].detach().cpu().numpy()
            ary_state, reward, done, _ = env.step(ary_action)

            ary_state = env.reset() if done else ary_state
            if done:
                if if_random == False:
                    if self.wandb == True:
                        wandb.log({"reward": self.logging_reward})
                        self.logging_reward = 0
                else:
                    '初始化buffer阶段'
                    pass
            else:
                if if_random == False:
                    self.logging_reward += reward

                else:
                    pass
            state = torch.as_tensor(ary_state, dtype=torch.float32, device=self.device).unsqueeze(0)
            actions[t] = action
            rewards[t] = reward
            dones[t] = done
        self.last_state = state

        rewards *= self.reward_scale

        undones = 1.0 - dones.type(torch.float32)

        return states, actions, rewards, undones

    def expore_vec_env(self):
        pass

    def update_net(self, buffer: Union[ReplayBuffer, tuple]) -> Tuple[float, ...]:
        obj_critic = 0.0
        obj_actor = 0.0
        assert isinstance(buffer, ReplayBuffer) or isinstance(buffer, tuple)
        assert isinstance(self.batch_size, int)
        assert isinstance(self.repeat_times, int)
        assert isinstance(self.reward_scale, float)
        return obj_critic, obj_actor

    def get_obj_critic_raw(self, buffer: ReplayBuffer, batch_size: int) -> Tuple[Tensor, Tensor]:
        with torch.no_grad():
            states, actions, rewards, undones, next_ss = buffer.sample(batch_size)
            next_as = self.act_target(next_ss)
            next_qs = self.cri_target(next_ss, next_as)

            q_lables = rewards + self.gamma * next_qs * undones

        q_values = self.cri(states, actions)

        obj_critic = self.criterion(q_values, q_lables)
        return obj_critic, states

    def optimzer_update(self, optimizer: torch.optim, objective: Tensor):
        optimizer.zero_grad()
        objective.backward()
        clip_grad_norm_(parameters=optimizer.param_groups[0]["params"], max_norm=self.clip_grad_norm)
        optimizer.step()

    @staticmethod
    def soft_update(target_net: torch.nn.Module, current_net: torch.nn.Module, tau: float):
        for tar, cur in zip(target_net.parameters(), current_net.parameters()):
            tar.data.copy_(cur.data * tau + (1 - tau) * tar.data)

    def update_avg_std_for_normalization(self, states: Tensor, returns: Tensor):
        tau = self.state_value_tau
        if tau == 0:
            return
        state_avg = states.mean(dim=0, keepdim=True)
        state_std = states.std(dim=0, keepdim=True)

        self.act.state_avg[:] = self.act.state_avg * (1 - tau) + state_avg * tau
        self.act.state_std[:] = self.cri.state_std * (1 - tau) + state_std * tau + 1e-4
        self.cri.state_avg[:] = self.act.state_avg
        self.cri.state_std[:] = self.cri.state_std

        returns_avg = returns.mean(dim=0)
        returns_std = returns.std(dim=0)

        self.cri.value_avg[:] = self.cri.value_avg * (1 - tau) + returns_avg * tau
        self.cri.value_std[:] = self.cri.value_std * (1 - tau) + returns_std * tau + 1e-4

    def get_cumulative_rewards(self, rewards: Tensor, undones: Tensor) -> Tensor:
        returns = torch.empty_like(rewards)

        masks = undones * self.gamma
        horizon_len = rewards.shape[0]

        last_state = self.last_state
        next_action = self.act_target(last_state)
        next_value = self.cri_target(last_state, next_action).detach()
        for t in range(horizon_len - 1, -1, -1):
            returns[t] = next_value = rewards[t] + masks[t] * next_value
        return returns


def get_optim_param(optimizer: torch.optim) -> list:
    params_list = []
    for params_dict in optimizer.state_dict()['state'].value():
        params_list.extend([t for t in params_dict.values() if isinstance(t, torch.Tensor)])
    return params_list
