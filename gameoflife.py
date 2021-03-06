# -*- coding: utf-8 -*-
"""GameOfLife.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zpG8jaMhLvzVFF1JLC-Ob1cnUg6XqaOi

# Game Of Life
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import njit


width = 300
height = 200

p_alive = 0.04
p_die = 0.01
epochs = 600
interval = 50

@njit
def neighbours(life, x, y):
    count = 0
    if y - 1 >= 0:
        count += life[x, y - 1]
    if y + 1 < height:
        count += life[x, y + 1]
    if x - 1 >= 0:
        count += life[x - 1, y]
        if y + 1 < width:
            count += life[x - 1, y + 1]
        if y - 1 >= 0:
            count += life[x - 1, y - 1]
    if x + 1 < height:
        count += life[x + 1, y]
        if y + 1 < width:
            count += life[x + 1, y + 1]
        if y - 1 > 0:
            count += life[x + 1, y - 1]
    return count


@njit
def single_tick(life, x, y):
    ng = neighbours(life, x, y)
    if ng == 3:
        life[x, y] = 1
    elif ng != 2:
        life[x, y] = 0
    if np.random.rand() < p_die:
        life[x, y] = 0
    return life


@njit
def tick(life):
    for x in range(height):
        for y in range(width):
            life = single_tick(life, x, y)
    return life


_life = np.reshape(np.random.choice(2, width * height, p=[1 - p_alive, p_alive]), (height, width))
alive = np.array([])

fig = plt.figure()

im = plt.imshow(_life)
ims = [[im]]

for _ in range(epochs):
    _life = tick(_life)
    alive = np.append(alive, np.sum(_life))
    im = plt.imshow(_life)
    ims.append([im])

anim = animation.ArtistAnimation(
    fig,
    ims,
    interval=interval,
    blit=True
)

plt.figure().set_figwidth(10)
plt.plot(range(len(alive)), alive)

plt.show()
