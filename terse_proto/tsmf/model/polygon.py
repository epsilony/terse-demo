'''
Created on 2012-12-22

@author: Man YUAN <epsilonyuan@gmail.com>

@author: Sparrow HU <huhao200709@163.com>
'''

from terse_proto.tsmf.model.segment import Segment2D
import numpy as np       
            
class _Polygon2DIterator(object):
    def __init__(self, pg):
        self.pg = pg
        self.index = 0
        self.result = self.pg.chains_heads[self.index]
        self.just_raise = False
    
    def next(self):
        # if self.index < len(self.pg.vertes):
        if self.just_raise:
            raise StopIteration()
        re = self.result.succ
            # result = self.pg.chains_heads[self.index]
        if re is not self.pg.chains_heads[self.index]:
            self.result = self.result.succ
            return self.result.pred
                      
        else:
            self.index += 1
                # return re.pred
                
            if self.index == len(self.pg.vertes):
                self.just_raise = True
                return re.pred
            else:
                self.result = self.pg.chains_heads[self.index]
                return re.pred
 
class Polygon2D(object):
    def __init__(self, vertes):
        self.vertes = vertes
        self.chains_heads = [Segment2D(e[0]) for e in vertes ]
        for i in xrange(len(vertes)):
            
            point = self.chains_heads[i]
            for p in vertes[i][1:]:
                point.succ = Segment2D(p)
                t = point
                point = point.succ
                point.pred = t
            point.succ = self.chains_heads[i]
            self.chains_heads[i].pred = point
    def __iter__(self):
        return _Polygon2DIterator(self)

    
    def ray_crossing(self, xy):
        # Originate from:
        #       Joseph O'Rourke, Computational Geometry in C,2ed. Page 244, Code 7.13
        rcross = 0
        lcross = 0
        x,y=xy
        for seg in self:
            if np.alltrue(seg.head.coord == xy):
                return 'v'
            x_i, y_i = seg.head.coord
            x_i1, y_i1 = seg.rear.coord
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
        inf_abs = float('inf')
        for seg in self:
            t = seg.distance_to(xy)
            if t < inf_abs:
                inf_abs = t
        return inf_abs if r_crs == 'i' else -inf_abs
        
   
def sample_vertes_xys():
    return np.array([[[0, 0], [1, 0], [1, 1], [0.5, 0.5], [0, 1]]], dtype=np.double)  

if __name__ == '__main__':

    pg = Polygon2D(sample_vertes_xys())
    dist_func_py = np.frompyfunc(lambda x, y:pg.distance_function((x, y)), 2, 1)
    
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
    
