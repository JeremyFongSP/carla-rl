import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torch.nn.functional as F

from carla.agent.agent import Agent
from model import Policy

class VPGCarla(Agent):

    def __init__(self,
                 obs_converter,
                 action_converter,
                 value_loss_coef,
                 entropy_coef,
                 alpha=None,
                 lr=None,
                 eps=None,
                 gamma=None,
                 max_grad_norm=None):

        self.obs_converter = obs_converter
        self.action_converter = action_converter
        self.model = Policy(self.obs_converter.get_observation_space(), 
                            self.action_converter.get_action_space()).to("cuda:0")
        self.value_loss_coef = value_loss_coef
        self.entropy_coef = entropy_coef

        self.max_grad_norm = max_grad_norm

        self.optimizer = optim.Adam(self.model.parameters(), lr=lr, eps=eps)


    def update(self, rollouts):
        # 4: Compute rewards to go Rt
        returns = rollouts.returns[:-1]

        # 5: Compute advantage estimates At based on current value
        # function Vk
        advantages = returns - rollouts.value_preds[:-1]
        advantages = (advantages - advantages.mean()) / (
            advantages.std() + 1e-5)

        # Update Epsilon Greedy
        # self.eps_curr = max(0.0, self.eps_curr - self.eps_greedy_decay)
        obs_shape = {k: r.size()[2:] for k, r in rollouts.obs.items()}
        rollouts_flatten = {k: r[:-1].view(-1, *obs_shape[k]) for k, r in rollouts.obs.items()}
        action_shape = rollouts.actions.size()[-1]
        num_steps, num_processes, _ = rollouts.rewards.size()

        values, action_log_probs, dist_entropy, _ = self.model.evaluate_actions(
            rollouts_flatten['img'],
            rollouts_flatten['v'],
            rollouts.recurrent_hidden_states[0].view(-1, self.model.recurrent_hidden_state_size),
            rollouts.masks[:-1].view(-1, 1),
            rollouts.actions.view(-1, action_shape))

        values = values.view(num_steps, num_processes, 1)
        action_log_probs = action_log_probs.view(num_steps, num_processes, 1)

        # 6: Estimate policy gradient
        action_loss = -(action_log_probs*advantages).mean()

        # 8: Fit value function by regression on mean-squared error
        value_loss = 0.5 * F.mse_loss(returns, values)

        # 7: Compute policy update
        self.optimizer.zero_grad()
        (value_loss * self.value_loss_coef + action_loss -
         dist_entropy * self.entropy_coef).backward()
        nn.utils.clip_grad_norm_(self.model.parameters(),
                                 self.max_grad_norm)
        self.optimizer.step()

        return value_loss.item(), action_loss.item(), dist_entropy.item()

    def act(self, inputs, rnn_hxs, masks, deterministic=False):
        eps_curr = 0. # TODO: Change if you want to implement epsilon-greedy
        return self.model.act(inputs['img'], inputs['v'], rnn_hxs, masks, eps_curr, deterministic=False)

    def get_value(self, inputs, rnn_hxs, masks):
        return self.model.get_value(inputs['img'], inputs['v'], rnn_hxs, masks)

