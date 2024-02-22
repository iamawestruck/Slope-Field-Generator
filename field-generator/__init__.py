import math

from matplotlib import pyplot as plt
import numpy as np


def parseFunc(func, x, y):
    return eval(func, {}, {
        "x": x,
        "y": y,
        "e": np.e,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "arcsin": np.arcsin,
        "arccos": np.arccos,
        "arctan": np.arctan,
        "pi": np.pi
    })


def slopeField(func, xmin=-10, xmax=10, ymin=-10, ymax=10, density=1, lineLength=None):
    np.seterr(divide='ignore', invalid='ignore')
    x = np.arange(xmin, xmax, 1/density)
    y = np.arange(ymin, ymax, 1/density)
    X, Y = np.meshgrid(x, y)
    # if hasattr(func, '__call__'):
    #     slopes = func(X, Y)
    # else:

    if not (type(func) is str or hasattr(func, '__call__')):
        raise Exception("L, bad argument")
    if type(func) is str:
        slopes = parseFunc(func, X, Y)
    else:
        slopes = func(X, Y)
    U = (1 / (1 + slopes ** 2) ** 0.5) * np.ones(X.shape)
    V = (1 / (1 + slopes ** 2) ** 0.5) * slopes
    plt.figure() #no clue
    plt.title("Slope Field Generator")
    plt.xlabel("X")
    plt.ylabel("Y")
    scale = 50/lineLength if lineLength is not None else None
    Q = plt.quiver(X, Y, U, V, headlength=0, headwidth=1, color='deepskyblue', scale=scale)
    plt.grid(True)

def vectorField(partialOne, partialTwo, xmin=-10, xmax=10, ymin=-10, ymax=10, density=1, lineLength=None):
    np.seterr(divide='ignore', invalid='ignore')
    x = np.arange(xmin, xmax, 1/density)
    y = np.arange(ymin, ymax, 1/density)
    X, Y = np.meshgrid(x, y)

    if not (type(partialOne) is str or hasattr(partialOne, '__call__')):
        raise Exception("L, bad argument")
    if type(partialOne) is str:
        U = parseFunc(partialOne, X, Y)
    else:
        U = partialOne(X, Y)

    if not (type(partialTwo) is str or hasattr(partialTwo, '__call__')):
        raise Exception("L, bad argument")
    if type(partialTwo) is str:
        V = parseFunc(partialTwo, X, Y)
    else:
        V = partialTwo(X, Y)

    plt.title("Vector Field Generator")
    plt.xlabel("X")
    plt.ylabel("Y")
    scale = 50/lineLength if lineLength is not None else None
    Q = plt.quiver(X, Y, U, V, headwidth=5, color='deepskyblue', scale=scale)
    plt.grid(True)
def solutionCurve(func, xinit, yinit, xmin=-10, xmax=10, ymin=-10, ymax=10):
    xstep, ystep = (xinit, yinit)
    X = []
    Y = []
    if not (type(func) is str or hasattr(func, '__call__')):
        raise Exception("L, bad argument")

    for i in range(10000):
        X.append(xstep)
        Y.append(ystep)
        if type(func) is str:
            slope = parseFunc(func, xstep, ystep)
        else:
            slope = func(xstep, ystep)
        ystep += slope * 0.01
        xstep += 0.01
        if xstep > xmax or xstep < xmin or ystep > ymax or ystep < ymin:
            break
    for i in range(10000):
        X.append(xstep)
        Y.append(ystep)
        if type(func) is str:
            slope = parseFunc(func, xstep, ystep)
        else:
            slope = func(xstep, ystep)
        ystep -= slope * 0.01
        xstep -= 0.01
        if xstep > xmax or xstep < xmin or ystep > ymax or ystep < ymin:
            break
    X = np.array(X)
    Y = np.array(Y)
    plt.plot(X, Y)
    plt.grid(True)



def f(x, y):
    return x

g = "y"

# slopeField(g, -10, 10, -10, 10, 1)
vectorField(f, g, -10, 10, -10, 10, 1)
solutionCurve(g, -3, 1, -10, 10, -10, 10)
plt.show()