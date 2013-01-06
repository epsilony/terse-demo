'''
Created on 2013-1-5

@author: Man YUAN <epsilonyuan@gmail.com>
'''
import numpy as np
from terse_proto.tsmf.shape_func.bases_func import monomial_bases
from nose.tools import ok_

def nomial_bases_test():
    xy = (1.2, -2.3)
    nm_order = 4
    diff_order = 1
    x, y = xy
    exps = np.array([[1, x, y, x ** 2, x * y, y ** 2, x ** 3, x ** 2 * y, x * y ** 2, y ** 3, x ** 4, x ** 3 * y , x ** 2 * y ** 2, x * y ** 3, y ** 4],
                     [0, 1, 0, 2 * x, y, 0, 3 * x ** 2, 2 * x * y, y ** 2, 0, 4 * x ** 3, 3 * x ** 2 * y, 2 * x * y ** 2, y ** 3, 0],
                     [0, 0, 1, 0, x, 2 * y, 0, x ** 2, 2 * x * y, 3 * y ** 2, 0, x ** 3, 2 * x ** 2 * y, 3 * x * y ** 2, 4 * y ** 3]], dtype=np.double)
    acts = monomial_bases(xy, nm_order, diff_order)
    ok_(np.max(abs(exps - acts)) < 1e-13)
    

if __name__ == '__main__':
    exps, acts = nomial_bases_test()
