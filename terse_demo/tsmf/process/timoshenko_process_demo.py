'''
Created on 2013-1-25

@author: Man YUAN <epsilonyuan@gmail.com>
'''

from terse_demo.util.jvm_util import start_jvm
start_jvm(8998)
from jpype import JClass
import numpy as np
from matplotlib import pyplot as plt

def plot_vs_by_y(pp, ax, y):
    xs = np.linspace(0.01, 48 - 0.01);
    ys = np.zeros_like(xs, dtype=np.double) + y
    plot_uvs(pp, ax, xs, ys)

def plot_uvs(pp, ax, xs, ys, axis=None, is_vs=True):
    if len(xs) != len(ys):
        raise ValueError("xs and ys should have same length")
    pp.setDiffOrder(0)
    act_uvs = []
    for i in xrange(len(xs)):
        xy = np.array((xs[i], ys[i]), dtype=np.double)
        uv = pp.value(xy, None)
        if is_vs:
            act_uvs.append(uv[1])
        else:
            act_uvs.append(uv[0])
    timoBeam = processor.weakformTask.timoBeam
    exp_uvs = []
    for i in xrange(len(xs)):
        xy = np.array((xs[i], ys[i]), dtype=np.double)
        uv = timoBeam.displacement(xy[0], xy[1], 0, None)
        if is_vs:
            exp_uvs.append(uv[1])
        else:
            exp_uvs.append(uv[0])
    if None is axis:
        axis = xs
    ax.plot(axis, act_uvs, 'r', label='Numerical')
    ax.plot(axis, exp_uvs, 'b', label='Precise') 

if __name__ == '__main__':
    WeakformProcessor2D = JClass('net.epsilony.tsmf.process.WeakformProcessor2D')
    processor = WeakformProcessor2D.genTimoshenkoProjectProcess()
    processor.process()
    processor.solve()
    pp = processor.postProcessor()
    fig = plt.figure()
    
    ax = fig.add_subplot(221)
    ax.set_title('displacement $v$ along axis $x$ ($y=0$)')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$v(x,0)$')
    
    y = 0
    plot_vs_by_y(pp, ax, y)
    ax2 = fig.add_subplot(222)
    ax2.set_title('displacement $u$\n along the left edge ($x=0$)')
    ax2.set_xlabel('$y$')
    ax2.set_ylabel('$u$')
    
    ys = np.linspace(-5.99, 5.99)
    xs = np.zeros_like(ys) + 0.01
    plot_uvs(pp, ax2, xs, ys, ys, False)
    ax3 = fig.add_subplot(223)
    ax3.set_title('displacement $v$\n along the left edge ($x=0$)')
    ax3.set_xlabel('$y$')
    ax3.set_ylabel('$v$')
    plot_uvs(pp, ax3, xs, ys, ys, True)
    ax3.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    fig.tight_layout()
    fig.show()  
