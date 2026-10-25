import os
import time
import numpy as np
import matplotlib.pyplot as plt
from utils import moving_average

# تابع كل 10 ثواني بدون ما توقف Training
while True:
    if os.path.exists("outputs/rewards.npy"):
        rewards = np.load("outputs/rewards.npy")
        print("آخر 5 Rewards:", rewards[-5:])
        
        if len(rewards) >= 10:
            plt.clf()  # يمسح الرسم القديم
            plt.plot(rewards, alpha=0.5, label="Reward per Episode")
            plt.plot(moving_average(rewards, window=10), label="Moving Average")
            plt.xlabel("Episode")
            plt.ylabel("Reward")
            plt.title("Taxi Double DQN Training Progress")
            plt.legend()
            plt.pause(0.1)  # تحديث الرسم بدون توقف
        time.sleep(10)  # كل 10 ثواني يتحقق من الملف
    else:
        print("ملف rewards.npy لسه ما اتعملش، استني شوية بعد ما يبدأ Training.")
        time.sleep(5)
