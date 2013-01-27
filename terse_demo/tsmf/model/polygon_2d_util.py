'''
Created on 2013-1-20

@author: Man YUAN <epsilonyuan@gmail.com>
'''

from matplotlib.patches import PathPatch
from matplotlib.path import Path

def plot_jpolygon(pg, ax, *args, **kwds):
    vertes = pg.getVertes()
    xys = []
    codes = []
    for act_vs in vertes:
        atBegin = True
        for nd in act_vs:
            xys.append(nd.coord)
            if atBegin:
                codes.append(Path.MOVETO)
                atBegin = False
            else:
                codes.append(Path.LINETO)
        codes.append(Path.CLOSEPOLY)
        xys.append((0, 0))
    pp = PathPatch(Path(xys, codes), *args, **kwds)
    ax.add_patch(pp)
    
if __name__ == "__main__":
    from terse_demo.util.jvm_util import start_jvm
    from jpype import JClass
    start_jvm()
    JTestTool = JClass('net.epsilony.tsmf.util.TestTool')
    pg = JTestTool.samplePolygon(None)
    from matplotlib import pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_jpolygon(pg, ax)
    fig.show()
            
