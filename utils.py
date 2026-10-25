import numpy as np

def moving_average(x, w=20):
    return np.convolve(x, np.ones(w)/w, mode="valid")
