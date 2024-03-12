import math
import numbers
from scipy.integrate import solve_ivp

from matplotlib import pyplot as plt
import numpy as np


def _parseFunc(func, x, y):
    """
    If the func argument in slopeField() is a string, _parseFunc function is called.
    _parseFunc evaluates a string, specifies the x and y in the equation.
    Using eval(), the string returns values from the function.
    """
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


def slopeField(func, xmin=-10, xmax=10, ymin=-10, ymax=10, density=1, lineLength=None, figureNumber=None):
    """
    slopeField() generates a slope field plot for a given DFQ.

    Args:
    - func: String representing a first-order DFQ.
    - xmin, xmax, ymin, ymax: Limits for the x and y axes.
    - density: Density of the grid points.
    - lineLength: Length of the arrows representing slopes.
    - figureNumber: Number of the figure to display.

    Returns fig, a matplotlib figure object.
    """
    np.seterr(divide='ignore', invalid='ignore')
    x = np.linspace(xmin, xmax, density * 20)
    y = np.linspace(ymin, ymax, density * 20)
    X, Y = np.meshgrid(x, y)
    # if hasattr(func, '__call__'):
    #     slopes = func(X, Y)
    # else:

    if not (type(func) is str or hasattr(func, '__call__')):
        raise Exception("L, bad argument")
    if type(func) is str:
        slopes = _parseFunc(func, X, Y)
    else:
        slopes = func(X, Y)
    U = (1 / (1 + slopes ** 2) ** 0.5) * np.ones(X.shape)
    V = (1 / (1 + slopes ** 2) ** 0.5) * slopes

    fig = plt.figure(num=figureNumber)
    plt.title("Slope Field Generator")
    plt.xlabel("X")
    plt.ylabel("Y")
    scale = 50 / lineLength if lineLength is not None else None
    Q = plt.quiver(X, Y, U, V, headlength=0, headwidth=1, color='deepskyblue', scale=scale)
    plt.grid(True)
    return fig


def vectorField(partialOne, partialTwo, xmin=-10, xmax=10, ymin=-10, ymax=10, density=1, lineLength=None,
                figureNumber=None):
    """
    VectorField() generates a vector field plot for a given pair of DFQs.
    Args:
    - partialOne, partialTwo: Strings representing DFQs
    - xmin, xmax, ymin, ymax: Limits for the x and y axes.
    - density: Density of the grid points.
    - lineLength: Length of the arrows representing vectors.
    - figureNumber: Number of the figure to display.

    Returns fig, a matplotlib figure object.
    """

    np.seterr(divide='ignore', invalid='ignore')
    x = np.linspace(xmin, xmax, density * 20)
    y = np.linspace(ymin, ymax, density * 20)
    X, Y = np.meshgrid(x, y)

    if not (type(partialOne) is str or hasattr(partialOne, '__call__')):
        raise Exception("L, bad argument")
    if type(partialOne) is str:
        U = _parseFunc(partialOne, X, Y)
    else:
        U = partialOne(X, Y)

    if not (type(partialTwo) is str or hasattr(partialTwo, '__call__')):
        raise Exception("L, bad argument")
    if type(partialTwo) is str:
        V = _parseFunc(partialTwo, X, Y)
    else:
        V = partialTwo(X, Y)

    fig = plt.figure(num=figureNumber)
    plt.title("Vector Field Generator")
    plt.xlabel("X")
    plt.ylabel("Y")
    scale = 50 / lineLength if lineLength is not None else None
    Q = plt.quiver(X, Y, U, V, headwidth=5, color='deepskyblue', scale=scale)
    plt.grid(True)
    return fig


def solutionCurve(func, xinit, yinit, xmin=-10, xmax=10, ymin=-10, ymax=10, figureNumber=None):
    """
    solutionCurve() Generates a solution curve plot for a given DFQ.

    Args:
    - func: String representing a DFQ.
    - xinit, yinit: Initial conditions for the solution curve. [OPTIONAL]
    - xmin, xmax, ymin, ymax: Limits for the x and y axes. [OPTIONAL]
    - figureNumber: Number of the figure to display. [OPTIONAL]

    Returns fig, a matplotlib figure object.
    """
    xstep, ystep = (xinit, yinit)
    X = []
    Y = []
    if not (type(func) is str or hasattr(func, '__call__')):
        raise Exception("L, bad argument")

    for i in range(2000000):
        X.append(xstep)
        Y.append(ystep)
        try:
            if type(func) is str:
                slope = _parseFunc(func, xstep, ystep)
            else:
                slope = func(xstep, ystep)
        except ZeroDivisionError:
            break
        ystep += slope * 0.0005
        xstep += 0.0005
        if xstep > xmax or xstep < xmin or ystep > ymax or ystep < ymin:
            break
    for i in range(2000000):
        X.append(xstep)
        Y.append(ystep)
        try:
            if type(func) is str:
                slope = _parseFunc(func, xstep, ystep)
            else:
                slope = func(xstep, ystep)
        except ZeroDivisionError:
            break
        ystep -= slope * 0.0005
        xstep -= 0.0005
        if xstep > xmax or xstep < xmin or ystep > ymax or ystep < ymin:
            break
    X = np.array(X)
    Y = np.array(Y)
    fig = plt.figure(num=figureNumber)
    plt.plot(X, Y)
    plt.grid(True)
    return fig


def parametricCurve(xfunc, yfunc, xinit, yinit, tmax=50, figureNumber=None, sharedTimeGraphs=True):
    """
    Generates a parametric curve plot for a system of DFQs.

    Args:
    - xfunc, yfunc: Strings representing first-order ordinary differential equations or callable functions of two variables (x, y).
    - xinit, yinit: Initial conditions for the parametric curve.
    - tmax: Maximum value of the parameter 't'. [OPTIONAL]
    - figureNumber: Number of the figure to display. [OPTIONAL]
    - sharedTimeGraphs: Boolean indicating whether to display x and y plots on the same figure or separate figures. [OPTIONAL]

    Returns 1-3 matplot figure objects, depending on whether sharedTimeGraphs is True or False.
    """

    times = np.linspace(0, tmax, 500)
    if not (type(xfunc) is str or hasattr(xfunc, '__call__')):
        raise Exception("L, bad argument")
    if type(xfunc) is str:
        xlambda = lambda x, y: _parseFunc(xfunc, x, y)
    else:
        xlambda = lambda x, y: xfunc(x, y)

    if not (type(yfunc) is str or hasattr(yfunc, '__call__')):
        raise Exception("L, bad argument")
    if type(yfunc) is str:
        ylambda = lambda x, y: _parseFunc(yfunc, x, y)
    else:
        ylambda = lambda x, y: yfunc(x, y)

    solution = solve_ivp(lambda t, vars: [xlambda(vars[0], vars[1]), ylambda(vars[0], vars[1])], [0, tmax],
                         [xinit, yinit], t_eval=times)
    figures = []
    figures.append(plt.figure(figureNumber))
    plt.plot(solution.y[0], solution.y[1])
    if sharedTimeGraphs:
        figures.append(plt.figure())
        plt.title("Parametric Curves in Terms of t")
        plt.plot(solution.t, solution.y[0], label="x(t)")
        plt.plot(solution.t, solution.y[1], label="y(t)")
        plt.xlabel("Time")
    else:
        figures.append(plt.figure())
        plt.title("x in Terms of Time")
        plt.plot(solution.t, solution.y[0], label="x(t)")
        plt.xlabel("Time")
        plt.ylabel("x")
        figures.append(plt.figure())
        plt.title("y in Terms of Time")
        plt.plot(solution.t, solution.y[1], label="y(t)")
        plt.xlabel("Time")
        plt.ylabel("y")
    return figures


def show():
    plt.show()

