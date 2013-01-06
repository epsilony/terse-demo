'''
Created on 2013-1-2

@author: Man YUAN <epsilonyuan@gmail.com>

'''
from __future__ import division
from scipy.misc import comb
def output_length(dim, diff_order):
    if dim == 1:
        return diff_order
    elif dim == 2:
        return output_length_2d(diff_order)
    elif dim == 3:
        return output_length_3d(diff_order)
    else:
        raise ValueError("Only supports 1D, 2D and 3D")

def output_length_2d(diff_order):
    return (diff_order + 2) * (diff_order + 1) // 2

def output_length_3d(diff_order):
    result = 0
    for i in xrange(0, diff_order + 1):
        result += comb(2 + i, 2)
    return result
