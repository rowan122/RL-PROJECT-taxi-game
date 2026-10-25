# RL Project - Taxi Game

A reinforcement-learning taxi game. A Double DQN agent (PyTorch) learns to pick up and drop off a passenger in a grid environment, with Pygame GUIs to watch the trained agent or play manually.

## Contents
- `env.py`, `env_gui.py`, `env_gui_emoji.py` - environments
- `agent.py` - DQN agent
- `train.py`, `evaluate.py`, `monitor_training.py` - training and evaluation
- `play_gui.py`, `human_play.py` - watch the trained agent / play by hand
- `taxi_ddqn.pth` - trained weights; `outputs/` - training results
- `data/` - additional dataset files

## Technologies
Python, PyTorch, Gymnasium, NumPy, Matplotlib, Pygame

## Setup & Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt pygame
python train.py      # train the agent
python play_gui.py   # watch the trained agent
```