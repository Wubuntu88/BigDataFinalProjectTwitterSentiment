#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def sine_wave(n_x, obs_err_sd=1.5, tp_err_sd=.3):
    x = np.linspace(0, (n_x - 1) / 2, n_x)
    y = np.sin(x) + np.random.normal(0, obs_err_sd) + np.random.normal(0, tp_err_sd, n_x)
    return y

sines = np.array([sine_wave(31) for _ in range(20)])

sns.tsplot(sines)

plt.show()
