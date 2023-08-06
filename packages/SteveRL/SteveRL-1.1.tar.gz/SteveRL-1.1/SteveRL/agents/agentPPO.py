import torch
from typing import Tuple
from torch import Tensor

from SteveRL.train.config import Config
from SteveRL.agents.agentBase import AgentBase
from SteveRL.agents.net import ActorPPO, Critic_PPO
import wandb


class AgentPPO(AgentBase):
    def __init__(self, net_dims: [int], state_dims: int, action_dims: int, gpu_id: int, args: Config = Config()):
        self.act_class = getattr(self, "act_class", ActorPPO)
        self.cri_class = getattr(self, "cri_class", Critic_PPO)
        super().__init__(net_dims=net_dims, state_dim=state_dims, action_dim=action_dims, gpu_id=gpu_id, args=args)
        self.if_off_polciy = False

        self.ratio_clip = getattr(self, "ratio_clip", 0.25)
        self.lambda_gae_adv = getattr(args, 'lambda_gae_adv', 0.95)
        self.lambda_entropy = getattr(args, "lambda_entropy", 0.01)
        self.lambda_entropy = torch.tensor(self.lambda_entropy, dtype=torch.float32, device=self.device)

        self.get_advantages = self.get_advantages_origin

        self.value_avg = torch.zeros(1, dtype=torch.float32, device=self.device)
        self.value_std = torch.ones(1, dtype=torch.float32, device=self.device)

        self.reward = 0
    def explore_one_env(self, env, horizon_len: int, if_random: bool = False) -> Tuple[Tensor, ...]:
        states = torch.zeros((horizon_len, self.num_envs, self.state_dim), dtype=torch.float32).to(self.device)
        actions = torch.zeros((horizon_len, self.num_envs, self.action_dim), dtype=torch.float32).to(self.device)
        logprobs = torch.zeros((horizon_len, self.num_envs), dtype=torch.float32).to(self.device)
        rewards = torch.zeros((horizon_len, self.num_envs), dtype=torch.float32).to(self.device)
        dones = torch.zeros((horizon_len, self.num_envs), dtype=torch.bool).to(self.device)

        state = self.last_state

        get_action = self.act.get_action
        convert = self.act.convert_action_for_env
        for t in range(horizon_len):
            action, logprob = get_action(state)
            states[t] = state
            ary_action = convert(action[0]).detach().cpu().numpy()

            ary_state, reward, done, _ = env.step(ary_action)



            if done:

                ary_state =env.reset()


                if if_random == False:
                    if self.wandb:
                        self.reward+=reward

                        wandb.log({'reward': self.reward})

                        self.reward = 0
                else:
                    '初始化buffer阶段'
                    pass
            else:
                if if_random == False:
                    self.reward += reward

                else:
                    pass

            state = torch.as_tensor(ary_state, dtype=torch.float32, device=self.device).unsqueeze(0)
            actions[t] = action
            logprobs[t] = logprob
            rewards[t] = reward
            dones[t] = done
        self.last_state = state
        rewards *= self.reward_scale
        undones = 1.0 - dones.type(torch.float32)
        return states, actions, logprobs, rewards, undones

    def update_net(self, buffer) -> Tuple[float, ...]:

        with torch.no_grad():
            states, actions, logprobs, rewards, undones = buffer
            buffer_size = states.shape[0]
            buffer_num = states.shape[1]

            bs = 2 ** 10
            values = torch.empty_like(rewards)
            for i in range(0, buffer_size, bs):
                for j in range(buffer_num):
                    values[i:i + bs, j] = self.cri(states[i:i + bs, j])

            advantages = self.get_advantages(rewards, undones, values)
            reward_sums = advantages + values

            del  rewards,undones,values
            advantages = (advantages - advantages.mean()) / (advantages.std(dim=0) + 1e-4)

            self.update_avg_std_for_normalization(
                states=states.reshape((-1, self.state_dim)),
                returns=reward_sums.reshape((-1,))
            )
            obj_critics = 0.0
            obj_actors = 0.0

            sample_len = buffer_size - 1
            update_times = int(buffer_size * self.repeat_times / self.batch_size)
            assert update_times >= 1
            for _ in range(update_times):
                ids = torch.randint(sample_len * buffer_num, size=(self.batch_size,), requires_grad=False)
                ids0 = torch.fmod(ids, sample_len)
                ids1 = torch.div(ids, sample_len, rounding_mode='floor')

                state = states[ids0, ids1]
                action = actions[ids0, ids1]
                logprob = logprobs[ids0, ids1]
                advantage = advantages[ids0, ids1]
                reward_sum = reward_sums[ids0, ids1]
                torch.set_grad_enabled(True)
                value = self.cri(state)
                obj_critic = self.criterion(value, reward_sum)
                self.optimzer_update(self.cri_optimizer, obj_critic)
                new_logprob, obj_entropy = self.act.get_logprob_entropy(state, action)
                ratio = (new_logprob - logprob.detach()).exp()
                surrpgate1 = advantage * ratio
                surrpgate2 = advantage * ratio.clamp(1 - self.ratio_clip, 1 + self.ratio_clip)
                obj_surrogate = torch.min(surrpgate1, surrpgate2).mean()

                obj_actor = obj_surrogate + obj_entropy.mean() * self.lambda_entropy
                self.optimzer_update(self.act_optimizer, -obj_actor)

                obj_critics += obj_critic.item()
                obj_actors += obj_actor.item()
            a_std_log = self.act.action_std_log.mean() if hasattr(self.act, 'action_std_log') else torch.zeros()

            if self.wandb:
                    wandb.log({'obj_critics:': obj_critics / update_times})
                    wandb.log({'obj_actors:': obj_actors / update_times})
                    wandb.log({'obj_entropy:': obj_entropy})
                    wandb.log({'a_std_log:':a_std_log})
            torch.set_grad_enabled(False)

            return obj_critics / update_times, obj_actors / update_times, a_std_log.item()

    def get_advantages_origin(self, rewards: Tensor, undones: Tensor, values: Tensor) -> Tensor:
        advantages = torch.empty_like(values)

        masks = undones * self.gamma
        horizon_len = rewards.shape[0]
        next_value = self.cri(self.last_state).detach()

        advantage = torch.zeros_like(next_value)
        for t in range(horizon_len - 1, -1, -1):
            next_value = rewards[t] + masks[t] * next_value
            # r+yV(s)
            advantages[t] = advantage = next_value - values[t] + masks[t] * self.lambda_gae_adv * advantage
            next_value = values[t]

        return advantages



