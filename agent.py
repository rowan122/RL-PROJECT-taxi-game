import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

# =========================
# Q Network
# =========================
class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.net(x)

# =========================
# Agent (Double DQN)
# =========================
class DQNAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim

        self.gamma = 0.99
        self.lr = 1e-3
        self.batch_size = 64

        self.epsilon = 1.0
        self.eps_min = 0.05
        self.eps_decay = 0.995

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.q = DQN(state_dim, action_dim).to(self.device)
        self.target = DQN(state_dim, action_dim).to(self.device)
        self.target.load_state_dict(self.q.state_dict())

        self.optim = optim.Adam(self.q.parameters(), lr=self.lr)
        self.memory = deque(maxlen=20000)

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_dim)

        state = torch.FloatTensor(np.array(state)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return self.q(state).argmax().item()

    def remember(self, s, a, r, ns, d):
        self.memory.append((s, a, r, ns, d))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        s, a, r, ns, d = zip(*batch)

        s = torch.FloatTensor(np.array(s)).to(self.device)
        a = torch.LongTensor(a).to(self.device)
        r = torch.FloatTensor(r).to(self.device)
        ns = torch.FloatTensor(np.array(ns)).to(self.device)
        d = torch.FloatTensor(d).to(self.device)

        q_val = self.q(s).gather(1, a.unsqueeze(1)).squeeze()

        # -------- Double DQN --------
        with torch.no_grad():
            next_actions = self.q(ns).argmax(1)
            next_q = self.target(ns).gather(
                1, next_actions.unsqueeze(1)
            ).squeeze()

        target = r + self.gamma * next_q * (1 - d)

        loss = nn.MSELoss()(q_val, target)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        self.epsilon = max(self.eps_min, self.epsilon * self.eps_decay)

    def update_target(self):
        self.target.load_state_dict(self.q.state_dict())
