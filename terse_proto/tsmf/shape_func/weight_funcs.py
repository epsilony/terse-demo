'''
Created on 2013-1-2

@author: Man YUAN <epsilonyuan@gmail.com>
'''
from terse_proto.tsmf.util.part_diff_math import output_length_2d
import numpy as np

def triple_spline(dist, diff_order):
    if diff_order > 1 or diff_order < 0:
        raise ValueError('Only support 0 or 1 diff_order')
    res = np.ndarray((diff_order + 1,))
    if dist >= 1:
        res.fill(0)
        return res
    if dist < 0:
        raise ValueError("distance should be non-negative")
    if dist <= 0.5:
        res[0] = 2 / 3.0 - 4 * dist ** 2 + 4 * dist ** 3
        if diff_order >= 1:
            res[1] = -8 * dist + 12 * dist ** 2
    else:
        res[0] = 4 / 3.0 - 4 * dist + 4 * dist ** 2 - 4 / 3.0 * dist ** 3
        if diff_order >= 1:
            res[1] = -4 + 8 * dist - 4 * dist ** 2
    return res

class WeightFunction(object):
    def __init__(self, core_func=None):
        if core_func is None:
            self.core_func = triple_spline
        else:
            self.core_func = core_func
        self.set_diff_order(0)
        
    
    def set_diff_order(self, diff_order):
        self._diff_order = diff_order
        
    def get_diff_order(self):
        return self._diff_order
    
    diff_order = property(get_diff_order, set_diff_order)
    
    def values(self, dists, infl_rads):
        num_row = output_length_2d(self.diff_order)
        results = np.ndarray(dists.shape, dtype=np.double)
        if len(infl_rads) == 1:
            uni_rad = infl_rads[0]
        else:
            uni_rad = None
            
        for i in xrange(results.shape[0]):
            if uni_rad:
                rad = uni_rad
            else:
                rad = infl_rads[i]
            core_value = self.core_func(dists[i][0] / rad, self._diff_order)
            results[i][0] = core_value[0]
            for j in xrange(1, num_row):
                results[i][j] = core_value[1] / rad * dists[i][j]
        return results

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.linspace(0, 1.5)
    ys = np.ndarray((2, len(x)))
    for i in xrange(len(x)):
        res = triple_spline(x[i], 1)
        ys[:, i] = res
        
    for y in ys:
        ax.plot(x, y)
    fig.show()
