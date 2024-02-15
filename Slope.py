from matplotlib import pyplot as plt
import numpy as np


def slopeField(func, xmin, xmax, ymin, ymax):
    x = np.arange(xmin, xmax)
    y = np.arange(ymin, ymax)
    X, Y = np.meshgrid(x, y)
    slopes = func(X, Y)
    U = (1 / (1 + slopes ** 2) ** 0.5) * np.ones(X.shape)
    V = (1 / (1 + slopes ** 2) ** 0.5) * slopes
    plt.figure()
    plt.title("Slope Field Generator")
    plt.xlabel("X")
    plt.ylabel("Y")
    Q = plt.quiver(X, Y, U, V, headlength=0, headwidth=1, color='deepskyblue')
    plt.grid(True)
    plt.show()


def f(x, y):
    return x - y


slopeField(f, 0, 5, 0, 5)
