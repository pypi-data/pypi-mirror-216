from sympy.plotting.plot import MatplotlibBackend, Plot
from sympy import plot, plot_implicit
from sympy.abc import x, y
from spb import *


def get_sympy_subplots(plot: Plot):
    backend = MatplotlibBackend(plot)
    backend.process_series()
    backend.fig.tight_layout()
    return backend.plt


def plot_points(*args, plot: Plot, show: bool):
    plt = get_sympy_subplots(plot)
    print(args)
    plt.plot(*args)
    plt.show()
    return plt


if __name__ == "__main__":
    p = plot(x**2-5,xlim=(-2,2),show=False)
    p2 = plot_implicit(x**2 + y**2 - 2**2,show=False)
        
    xx = [1,2,3]
    yy = [4,4,2]
    p3 = plot_list(xx, yy,show=False)
    
    tot = p + p2 + p3
    tot.show()
   
    # plot_points([1, 2, 3], [4, 5, 6], 'gx', plot=p2, show=False)
    # p2.show()
    # print(p2)

    # p2.extend(p3)
    # plot_points(1, 5, 'rx')
    # plt.plot([1, 2], [6, 9], 'bo')
    # show()
