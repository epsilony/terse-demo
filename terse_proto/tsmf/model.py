'''
Created on 2012-12-22

@author: Man YUAN <epsilonyuan@gmail.com>
'''

import numpy as np

class Polygon2D(object):
    def __init__(self, vertex_xys):
        self.vertex_xys = np.array(vertex_xys, dtype=np.double)
        if len(self.vertex_xys.shape) < 2 or self.vertex_xys.shape[1] < 2 or self.vertex_xys.shape[0] < 3:
            raise ValueError("vertex_xys must have a shape which is bigger than (3,2)")
    
    def ray_crossing(self, xy):
        # Originate from:
        #       Joseph O'Rourke, Computational Geometry in C,2ed. Page 244, Code 7.13
        rcross = 0
        lcross = 0
        n = self.vertex_xys.shape[0]
        xys = self.vertex_xys
        x = xy[0]
        y = xy[1]
        for i in xrange(n):
            if np.alltrue(xys[i] == xy):
                return 'v'
            i1 = (i + n - 1) % n
            
            x_i, y_i = xys[i]
            x_i1, y_i1 = xys[i1]
            rstrad = (y_i > y) != (y_i1 > y)
            lstrad = (y_i < y) != (y_i1 < y)
            
            if rstrad or lstrad:
                if rstrad and x_i > x and x_i1 > x:
                    rcross += 1
                elif lstrad and x_i < x and x_i1 < x:
                    lcross += 1
                else:
                    xcross = (x_i * y - x_i * y_i1 - x_i1 * y + x_i1 * y_i) / (y_i - y_i1)
                    if(rstrad and xcross > x):
                        rcross += 1
                    if(lstrad and xcross < x):
                        lcross += 1
        if rcross % 2 != lcross % 2 :
            return 'e'
        if rcross % 2 == 1:
            return 'i'
        else:
            return 'o'
        
    def distance_function(self, xy):
        r_crs = self.ray_crossing(xy)
        if r_crs == 'e' or r_crs == 'v':
            return 0
        inf_abs = self.distance_to_segment(0, xy)
        for i in xrange(1, self.vertex_xys.shape[0]):
            t = self.distance_to_segment(i, xy)
            if t < inf_abs:
                inf_abs = t
        return inf_abs if r_crs == 'i' else -inf_abs
        
    def distance_to_segment(self, i, xy):
        i2 = (i + 1) % self.vertex_xys.shape[0]
        v1 = self.vertex_xys[i]
        v2 = self.vertex_xys[i2]
        v_e = v2 - v1
        len_e = np.dot(v_e, v_e) ** 0.5
        v_xy = xy - v1
        nv_e = v_e / len_e
        dt = np.dot(nv_e, v_xy)
        if dt >= len_e:
            return np.dot(dt, dt) ** 0.5
        elif dt <= 0:
            return np.dot(v_xy, v_xy) ** 0.5
        else:
            return abs(np.cross(v_e, v_xy))
            
def sample_vertes_xys():
    return np.array([[0, 0], [1, 0], [1, 1], [0.5, 0.5], [0, 1]], dtype=np.double)  

if __name__ == '__main__':

    pg_py = Polygon2D(sample_vertes_xys())
    dist_func_py = np.frompyfunc(lambda x, y:pg_py.distance_function((x, y)), 2, 1)
    
    xs = np.linspace(-0.5, 1.5, 100)
    ys = np.linspace(-0.5, 1.5, 100)    
    (g_xs, g_ys) = np.meshgrid(xs, ys)
    
    g_zs_py = dist_func_py(g_xs, g_ys)

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(121, projection='3d')
    ax.contour(g_xs, g_ys, g_zs_py)
    ax.plot_wireframe(g_xs, g_ys, g_zs_py, rstride=5, cstride=5)
    
    ax = fig.add_subplot(122, projection='3d')
    ax.contour(g_xs, g_ys, g_zs_py, 20)
    ax.contourf(g_xs, g_ys, g_zs_py, (0, 0.05))
    
    fig.show()
    
