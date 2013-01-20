'''
Created on 2012-12-22

@author: Man YUAN <epsilonyuan@gmail.com>
'''

import numpy as np
from terse_demo.util import jvm_util
from jpype import JPackage,JArray,JDouble
from terse_proto.tsmf.model import Polygon2D

jvm_util.start_jvm(8998)
JPolygon2D=JPackage('net').epsilony.tsmf.model.Polygon2D

            
def sample_vertes_xys():
    return np.array([[[0, 0], [1, 0], [1, 1],[0.5,0.5],[0,1]]],dtype=np.double)  

if __name__ == '__main__':

    pg_j = JPolygon2D.byCoordChains(sample_vertes_xys().tolist())
    dist_func_j=np.frompyfunc(lambda x,y:pg_j.distanceFunc(x,y),2,1)
    
    pg_py = Polygon2D(sample_vertes_xys())
    dist_func_py=np.frompyfunc(lambda x,y:pg_py.distance_function((x,y)),2,1)
    
    xs=np.linspace(-0.5,1.5,100)
    ys=np.linspace(-0.5,1.5,100)    
    (g_xs,g_ys)=np.meshgrid(xs, ys)
    
    g_zs_j=dist_func_j(g_xs,g_ys)
    g_zs_py=dist_func_py(g_xs,g_ys)
       
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(221,projection='3d')
    ax.contour(g_xs,g_ys,g_zs_py)
    ax.plot_wireframe(g_xs,g_ys,g_zs_py,rstride=5,cstride=5)
    
    ax=fig.add_subplot(222,projection='3d')
    ax.contour(g_xs,g_ys,g_zs_py,20)
    ax.contourf(g_xs,g_ys,g_zs_py,(0,0.05))
    
    ax=fig.add_subplot(223,projection='3d')   
    ax.contour(g_xs,g_ys,g_zs_j)
    ax.plot_wireframe(g_xs,g_ys,g_zs_py,rstride=5,cstride=5)
    
    ax=fig.add_subplot(224,projection='3d')
    ax.contour(g_xs,g_ys,g_zs_j,20)
    ax.contourf(g_xs,g_ys,g_zs_j,(0,0.05))
    fig.show()
    