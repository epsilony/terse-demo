'''
Created on 2013-1-4

@author: Man YUAN <epsilonyuan@gmail.com>
'''
from terse_proto.tsmf.util.part_diff_math import output_length_2d
import numpy as np

def bases_length(nm_order):
    return (nm_order + 1) * (nm_order + 2) / 2

def monomial_bases(xy, base_order, diff_order):
    if diff_order < 0 or diff_order > 1:
        raise ValueError("Only supports diff_order = 0 or 1")
    if base_order< 0:
        raise ValueError("monomial order should be non-negative")
    num_row = output_length_2d(diff_order)
    num_col = bases_length(base_order)
    res = np.ndarray((num_row, num_col), dtype=np.double)
    x, y = xy
    p = (1, x, y, x ** 2, x * y, y ** 2)
    if diff_order >= 1:
        p_x = (0, 1, 0, 2 * x, y, 0)
        p_y = (0, 0, 1, 0, x, 2 * y)
    if num_col <= len(p):
        res[0] = p[:num_col]
        if diff_order >= 1:
            res[1] = p_x[:num_col]
            res[2] = p_y[:num_col]
    else:
        res[0, :len(p)] = p
        if diff_order >= 1:
            res[1, :len(p)] = p_x
            res[2, :len(p)] = p_y
        for n in xrange(2, base_order):
            i1 = bases_length(n - 1)
            i2 = bases_length(n)
            for i in xrange(i2 - i1):
                res[0, i2 + i + 1] = y * res[0, i1 + i]
                if diff_order >= 1:
                    res[1, i2 + i + 1] = y * res[1, i1 + i]
                    res[2, i2 + i] = x * res[2, i1 + i]
            res[0, i2] = res[0, i1] * x
            if diff_order >= 1:
                res[1, i2] = res[0, i1] * (n + 1)
                res[2, i2 + n + 1] = res[0, i1 + n] * (n + 1)
    return res

class MonomialBases(object):
    def __init__(self, base_order=2):
        self.base_order = base_order
        self.diff_order = 0
    
    def size(self):
        return bases_length(self.base_order)
    
    def values(self, xy):
        return monomial_bases(xy, self.base_order, self.diff_order)
    
    def set_diff_order(self, diff_order):
        self.diff_order = diff_order
    
if __name__ == '__main__':
    print monomial_bases((1, 2), 4, 1)
    
