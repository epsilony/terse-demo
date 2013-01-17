'''
Created on 2013-1-17

@author: Man YUAN <epsilonyuan@gmail.com>
'''

import numpy as np
from terse_demo.util.java_code_gen import gen_array_code
shape_func_val = np.array([-1.1, 2.01, 3.42, 14, 50], dtype=np.double)
N = np.zeros((4, 2), dtype=np.double)
Phi = np.zeros((6, 2), dtype=np.double)
u = np.array([3.4, -1.2]).transpose()
N[0::2, 0] = shape_func_val[3:]
N[1::2, 1] = shape_func_val[3:]
Phi[0::2, 0] = shape_func_val[:3]
Phi[1::2, 1] = shape_func_val[:3]
nodesIds = np.array([5, 2, 0, 8, 6], dtype=np.int32)
row_ids = np.zeros((6,))
col_ids = np.zeros((4,))
row_ids[0::2] = nodesIds[:3] * 2
row_ids[1::2] = nodesIds[:3] * 2 + 1
col_ids[0::2] = nodesIds[3:] * 2
col_ids[1::2] = nodesIds[3:] * 2 + 1

nodes_size = 6
lag_size = 4

if __name__ == '__main__':
# def gen_dirichlet_exps_codes():
    m = -Phi.dot(N.transpose())
    v = -N.dot(u)
    size = 2 * (nodes_size + lag_size)
    exp_m = np.zeros((size, size), dtype=np.double)
    exp_v = np.zeros((size,), dtype=np.double)
    for j in xrange(m.shape[1]):
        exp_v[col_ids[j]] = v[j]
        for i in xrange(m.shape[0]):
            exp_m[row_ids[i], col_ids[j]] = m[i, j]
            exp_m[col_ids[j], row_ids[i]] = m[i, j]
    print "Start main matrix exp-----------------------------------------"
    print gen_array_code(exp_m)
    print "End main matrix exp--------------------------------------------"
    print "\nStart main vector exp---------------------------------------"
    print gen_array_code(exp_v)
    print "End main vector exp----------------------------"

# if __name__=="__main__":
#    gen_dirichlet_exps_codes()
 
