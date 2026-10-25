import time
import pygame
import torch
from agent import DQNAgent
from env_gui_emoji import TaxiGUIReal  # env جديد

# ======= Initialize Environment and Agent =======
env = TaxiGUIReal()
agent = DQNAgent(4, 6)
agent.q.load_state_dict(torch.load("taxi_ddqn.pth"))
agent.q.eval()

state, _ = env.reset()
total_reward = 0
running = True
game_over = False  # Flag to print final reward only once
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if restart button clicked
            if env.check_restart(event.pos):
                state, _ = env.reset()
                env.has_passenger_flag = False
                env.steps = 0
                total_reward = 0
                running = True
                game_over = False  # Reset final reward flag

    if running:
        # Agent takes action
        action = agent.act(state)
        state, reward, done, _, _ = env.step(action)
        total_reward += reward
        env.steps += 1

        # Pickup
        if not env.has_passenger_flag and env.taxi == env.passenger:
            env.has_passenger_flag = True
            env.pickup_animation()
            env.render(show_message="Good! Passenger picked up!")
            pygame.display.flip()
            time.sleep(2)

        # Delivered
        elif env.has_passenger_flag and env.taxi == env.destination:
            env.has_passenger_flag = False
            env.delivered_animation()
            env.render(show_message="Delivered!")
            pygame.display.flip()
            time.sleep(2)
            running = False
            game_over = True  # Set flag to show final reward once
        else:
            env.render()

    else:
        if game_over:
            # Show final reward and steps once
            env.render(show_message=f"Final Reward: {total_reward:.1f}, Steps: {env.steps}")
            print(f"Final Reward: {total_reward:.1f}, Total Steps: {env.steps}")
            game_over = False  # Avoid repeating

    clock.tick(25)  # Faster FPS for fewer steps and better reward
