import time
import torch
from env import TaxiEnv
from agent import DQNAgent

# =========================
# Helper: Render Environment
# =========================
def render_env(state):
    # Extract taxi row, col, passenger, destination
    taxi_r, taxi_c, pass_idx, dest_idx = state

    # Define possible destinations
    destinations = [(0,0), (0,5), (5,0), (5,5)]
    
    if dest_idx >= len(destinations):
        print(f"Warning: dest_idx {dest_idx} out of range")
        return
    
    dest_r, dest_c = destinations[dest_idx]

    print(f"Taxi: ({taxi_r},{taxi_c}) | Passenger: {pass_idx} | Destination: ({dest_r},{dest_c})")

# =========================
# Main
# =========================
env = TaxiEnv()
agent = DQNAgent(state_dim=4, action_dim=6)  # adjust dims as per your env

# Load trained model
agent.q.load_state_dict(torch.load("taxi_ddqn.pth", map_location=agent.device))
agent.q.eval()

state, _ = env.reset()
done = False
step = 0

while not done:
    print(f"Step: {step}")
    render_env(state)
    
    # Agent selects action
    action = agent.act(state)
    
    # Step environment
    next_state, reward, done, _, _ = env.step(action)
    
    print(f"Action: {action} | Reward: {reward}\n")
    time.sleep(0.5)
    
    state = next_state
    step += 1

print("Delivered 🚕")
