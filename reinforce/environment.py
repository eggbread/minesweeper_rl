from minesweeper.Minesweeper import Minesweeper
import pygame, time, random
import numpy as np


class Env(object):
    def __init__(self):
        super(Env, self).__init__()
        self.action_space = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE']
        self.n_actions = len(self.action_space)

        self.minesweeper = Minesweeper()
        self.minesweeper.build_canvas()
        self.counter = 0
        self.rewards = []
        self.goal = []

        self.width = self.minesweeper.WIDTH
        self.height = self.minesweeper.HEIGHT
        self.state = np.array([random.randint(0, self.width - 1), random.randint(0, self.height - 1)])
        self.cnt = 0

    def reset(self):
        self.minesweeper.reset_game()
        time.sleep(0.5)

    def get_step(self):
        return [self.state[0], self.state[1], 0]

    def move(self, action):
        next_state = np.array(self.state)
        if action == 0:  # N
            if self.state[1] > 0:
                next_state[1] -= 1
        elif action == 1:  # NW
            if self.state[0] > 0 and self.state[1] > 0:
                next_state[0] -= 1
                next_state[1] -= 1
        elif action == 2:  # W
            if self.state[0] > 0:
                next_state[0] -= 1
        elif action == 3:  # SW
            if self.state[0] > 0 and self.state[1] < self.height - 1:
                next_state[0] -= 1
                next_state[1] += 1
        elif action == 4:  # S
            if self.state[1] < self.height - 1:
                next_state[1] += 1
        elif action == 5:  # SE
            if self.state[0] < self.width - 1 and self.state[1] < self.height - 1:
                next_state[0] += 1
                next_state[1] += 1
        elif action == 6:  # E
            if self.state[0] < self.width - 1:
                next_state[0] += 1
        elif action == 7:  # NE
            if self.state[0] < self.width - 1 and self.state[1] > 0:
                next_state[0] += 1
                next_state[1] -= 1
        return next_state

    def check_if_reward(self, state):
        check_list = dict()
        check_list['if_goal'] = False
        rewards = 0

        for reward in self.rewards:
            if reward['state'] == state:
                rewards += reward['reward']
                if reward['reward'] == 1:
                    check_list['if_goal'] = True

        check_list['rewards'] = rewards

        return check_list

    def step(self, action, episode):

        next_state = self.move(action)
        # check = self.check_if_reward(self.coords_to_state(next_state))
        # done = check['if_goal']
        # reward = check['rewards']

        # print("state : ", self.state, 'next_state : ', next_state)
        self.minesweeper.click(next_state)

        if self.minesweeper.check_mine(next_state):
            reward = -1
            done = True
        elif self.minesweeper.check_empty(next_state):
            reward = -1
            done = False
        elif self.minesweeper.check_success(next_state):
            reward = 1
            done = True
            self.cnt += 1
        else:
            reward = 0
            done = False
        # print('reward : ', reward, 'done : ', done)
        self.state = next_state
        self.minesweeper.step(episode, self.cnt)
        return np.append(next_state,reward), reward, done
