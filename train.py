from env import TaxiEnv
from agent import DQNAgent
from utils import moving_average
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import torch
import os

# =========================
# Setup
# =========================
os.makedirs("outputs", exist_ok=True)

env = TaxiEnv()

state_dim = 4        # [taxi_x, taxi_y, passenger_x, passenger_y]
action_dim = 6       # up, down, left, right, pickup, dropoff

agent = DQNAgent(state_dim=state_dim, action_dim=action_dim)

episodes = 600
rewards = []

# =========================
# Training Loop
# =========================
for ep in trange(episodes):
    state, _ = env.reset()
    total_reward = 0

    while True:
        action = agent.act(state)
        next_state, reward, done, _, _ = env.step(action)

        agent.remember(state, action, reward, next_state, done)
        agent.replay()

        state = next_state
        total_reward += reward

        if done:
            agent.update_target()
            rewards.append(total_reward)
            break

    # ✅ الطباعة لكل Episode
    print(f"Episode {ep} | Reward = {total_reward}")

# =========================
# Save Outputs
# =========================
np.save("outputs/rewards.npy", np.array(rewards))
torch.save(agent.q.state_dict(), "taxi_ddqn.pth")

# =========================
# Plot
# =========================
plt.figure(figsize=(8,5))
plt.plot(rewards, label="Reward")
plt.plot(moving_average(rewards), label="Moving Average")
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("Taxi Double DQN Training")
plt.legend()
plt.savefig("outputs/training_plot.png")
plt.show()
