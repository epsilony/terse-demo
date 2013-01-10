'''
Created on 2013-1-9

@author: Man YUAN <epsilonyuan@gmail.com>
'''

import numpy as np
from nose.tools import ok_
#from terse_proto.tsmf.shape_func.test.mls_test import polynomial_sample, sin_cos_sample
from terse_proto.tsmf.rbf import CSRbf

def flat_func(xy):
    return np.array([1,0,0],dtype=np.double)

def gen_sample(func, xys, rads):
    vals = np.ndarray((len(xys),), dtype=np.double)
    for i in xrange(len(xys)):
        vals[i] = func(xys[i])[0]
    res = CSRbf(xys, vals, rads)
    res.set_diff_order(1)
    return res

def simplest_test():
    xys=[(0,0),(0,1),(1,0),(1,1)]
    rad=2.0
    func=flat_func
    csrbf=gen_sample(func,xys,(rad,))
    sample_pts=[(0.5,0.5),(0.75,0.6)]
    exp_vals=[(1.09298195552180,0,0),(1.0952843048221457,-0.038816185884811061, 0.028917716128895377)]
    for i in xrange(len(sample_pts)):
        xy=sample_pts[i]
        act = csrbf.value(xy)
        exp = exp_vals[i]
        ok_(np.max(abs(act-exp)),1e-15)

##def flat_fitness_test():
#    rad=2.5
#    gap=1.0
#    num_node_rowcol=6
#    num_sample_rowcol=6
#    xs=np.linspace(0, 1.0*(num_node_rowcol-1),num_node_rowcol)
#    ys=np.copy(xs)
#    xys=[(x,y) for x in xs for y in ys]
#    csrbf=gen_sample(flat_func,xys,(rad,))
#    xs_smp=np.linspace(xs[0],xs[-1],num_sample_rowcol)
#    ys_smp=np.linspace(ys[0],ys[-1],num_sample_rowcol)
#    xys_smp=[(x,y) for x in xs_smp for y in ys_smp]
#    csrbf.set_diff_order(1)
#    for xy in xys_smp:
#        act=csrbf.value(xy)
#        exp=flat_func(xy)
#        print xy,exp,act,exp-act

#def fitness_test():
#    xs = np.linspace(-1, 2, 20)
#    ys = np.linspace(2, 4, 20)
#    rad_avg = 3 / 20.0* 3.5
#    xys = [(x, y)for x in xs for y in ys]
#
#    funcs = [polynomial_sample, sin_cos_sample]
#    tx = np.linspace(xs[0], xs[1], 3)
#    ty = np.linspace(ys[0], ys[1], 3)
#    t = [(x, y)for x in tx for y in ty]
#    ptss = [t, xys]
#    errs = [1e-5, 1e-10]
#    radss = [(rad_avg,), rad_avg + np.linspace(-0.1, 0.1, len(xys))]
#    datas = [(func, pts, rads) for func in funcs for pts in ptss for rads in radss]
#    
#    for func, pts, rads in datas:
#        csrbf = gen_sample(func, rads)
#        csrbf.set_diff_order(1)
#        
#        err = errs[ptss.index(pts)]
#        
#        for pt in pts:
#            act = csrbf.value(pt)
#            exps = func(pt)
#            print pt
#            ok_(np.max(abs(act - exps)) < err)

