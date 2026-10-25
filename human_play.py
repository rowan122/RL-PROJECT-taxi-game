import gymnasium as gym

def human_control():
    env = gym.make("Taxi-v3", render_mode="human")
    state, _ = env.reset()

    print("\n🎮 Human Control Mode")
    print("W: North | S: South | D: East | A: West")
    print("P: Pickup | O: Dropoff | Q: Quit\n")

    key_to_action = {
        "w": 1,
        "s": 0,
        "d": 2,
        "a": 3,
        "p": 4,
        "o": 5
    }

    while True:
        key = input("Enter move: ").lower()

        if key == "q":
            break

        if key not in key_to_action:
            print("❌ Invalid key")
            continue

        action = key_to_action[key]
        state, reward, done, truncated, _ = env.step(action)

        print(f"Reward: {reward}")

        if done or truncated:
            print("✅ Episode finished")
            break

    env.close()


if __name__ == "__main__":
    human_control()
