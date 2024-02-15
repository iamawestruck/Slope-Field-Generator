import math

from matplotlib import pyplot as plt
import numpy as np


def parseFunc(func, x, y):
    return eval(func, {}, {"x": x, "y": y})


def slopeField(func, xmin, xmax, ymin, ymax):
    if not (type(func) is str or hasattr(func, '__call__')):
        raise Exception("L")
    x = np.arange(xmin, xmax)
    y = np.arange(ymin, ymax)
    X, Y = np.meshgrid(x, y)
    if hasattr(func, '__call__'):
        slopes = func(X, Y)
    else:
        slopes = parseFunc(func, X, Y)
    U = (1 / (1 + slopes ** 2) ** 0.5) * np.ones(X.shape)
    V = (1 / (1 + slopes ** 2) ** 0.5) * slopes
    plt.figure()
    plt.title("Slope Field Generator")
    plt.xlabel("X")
    plt.ylabel("Y")
    Q = plt.quiver(X, Y, U, V, headlength=0, headwidth=1, color='deepskyblue')
    plt.grid(True)


def solutionCurve(func, xinit, yinit, xmin, xmax, ymin, ymax):
    xstep, ystep = (xinit, yinit)
    X = []
    Y = []
    for i in range(10000):
        X.append(xstep)
        Y.append(ystep)
        slope = func(xstep, ystep)
        ystep += slope * 0.01
        xstep += 0.01
        if xstep > xmax or xstep < xmin or ystep > ymax or ystep < ymin:
            break
    for i in range(10000):
        X.append(xstep)
        Y.append(ystep)
        slope = func(xstep, ystep)
        ystep -= slope * 0.01
        xstep -= 0.01
        if xstep > xmax or xstep < xmin or ystep > ymax or ystep < ymin:
            break
    X = np.array(X)
    Y = np.array(Y)
    plt.plot(X, Y)
    plt.grid(True)
    plt.show()


def f(x, y):
    return np.e-np.sin(y-x)


slopeField("y*x", -10, 10, -10, 10)
solutionCurve(f, -3, 1, -10, 10, -10, 10)
