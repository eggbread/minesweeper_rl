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
        # self.minesweeper.step()

        self.width = self.minesweeper.WIDTH
        self.height = self.minesweeper.HEIGHT
        self.state = np.array([random.randint(0, self.width-1), random.randint(0, self.height-1)])
        self.cnt = 0

    def reset(self):
        self.minesweeper.reset_game()
        time.sleep(0.5)

    def get_step(self):
        return self.state

    def step(self, action, episode):

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
        print("state : ",self.state,'next_state : ',next_state)
        self.minesweeper.click(next_state)

        if self.minesweeper.check_mine(next_state):
            reward = -10
            done = True
        elif self.minesweeper.check_empty(next_state):
            reward = -1
            done = False
        elif self.minesweeper.check_success(next_state):
            reward = 10
            done = True
            self.cnt += 1
        else:
            reward = 0
            done = False
        print('reward : ',reward,'done : ',done)
        self.state = next_state
        self.minesweeper.step(episode, self.cnt)
        return next_state, reward, done
