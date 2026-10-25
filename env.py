import numpy as np
from gymnasium import Env
from gymnasium.spaces import Discrete, Box

class TaxiEnv(Env):
    def __init__(self):
        self.grid = 5
        self.action_space = Discrete(6)
        self.observation_space = Box(0, 4, shape=(4,), dtype=np.int32)
        self.reset()

    def reset(self, seed=None):
        self.taxi = [0, 0]
        self.passenger = [4, 4]
        self.destination = [0, 4]
        self.has_passenger = False
        return self._state(), {}

    def _state(self):
        return np.array([
            self.taxi[0], self.taxi[1],
            self.passenger[0], self.passenger[1]
        ])

    def step(self, action):
        reward = -1
        done = False

        if action == 0: self.taxi[0] = max(0, self.taxi[0]-1)
        elif action == 1: self.taxi[0] = min(4, self.taxi[0]+1)
        elif action == 2: self.taxi[1] = max(0, self.taxi[1]-1)
        elif action == 3: self.taxi[1] = min(4, self.taxi[1]+1)

        elif action == 4:  # pickup
            if self.taxi == self.passenger:
                self.has_passenger = True
                self.passenger = [-1, -1]
            else:
                reward = -10

        elif action == 5:  # dropoff
            if self.has_passenger and self.taxi == self.destination:
                reward = 20
                done = True
            else:
                reward = -10

        return self._state(), reward, done, False, {}
