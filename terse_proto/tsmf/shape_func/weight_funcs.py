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

class Wendland(object):
    _coefs_1 = (-1, 1)
    _coefs_1_orders = (4, 6, 8)
    _coefs_2s = [(4, 1),
            (35, 18, 3),
            (32, 25, 8, 1)]
    _c_ops = (2, 4, 6)
    
    def __init__(self, c=4):
        c_ops = self._c_ops
        if not c in c_ops:
            raise ValueError("c should be one of " + str(c_ops))
        index = c / 2
        p_1 = (1,)
        for _i in xrange(self._coefs_1_orders[index]):
            p_1 = np.polymul(p_1, self._coefs_1)
        p_2 = self._coefs_2s[index]
        p = np.polymul(p_1, p_2)
        self.poly = np.poly1d(p)
        self.set_diff_order(0)
    
    def set_diff_order(self, order):
        self.diff_order = order
        self.polys = [self.poly]
        p = self.poly
        for _i in xrange(order):
            p = np.polyder(p)
            self.polys.append(p)
    
    def values(self, r):
        if r >= 1:
            return np.zeros((self.diff_order + 1,))
        
        res = np.ndarray((self.diff_order + 1,), dtype=np.double)
        for i in xrange(self.diff_order + 1):
            res[i] = self.polys[i](r)
        return res
    
    __call__ = values
    

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
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.linspace(0, 1.5)
    wend = Wendland()
    wend.set_diff_order(2)
    ys = np.ndarray((len(x), wend.diff_order + 1))
    for i in xrange(len(x)):
        ys[i] = wend(x[i])
    for i in xrange(wend.diff_order + 1):
        ax.plot(x, ys[:, i])
    fig.show()
