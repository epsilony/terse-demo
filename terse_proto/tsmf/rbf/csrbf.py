'''
Created on 2013-1-8

@author: Man YUAN <epsilonyuan@gmail.com>
'''

import numpy as np
from terse_proto.tsmf.shape_func import Wendland
from terse_proto.tsmf.shape_func import WeightFunction
from collections import deque
import scipy.sparse as spm
import scipy.sparse.linalg as spm_alg
from terse_proto.tsmf.util.part_diff_math import output_length_2d


class CSRbf(object):
    
    def __init__(self, xys, xys_vals, rads, base=Wendland(4)):
        self.xys = xys
        self.base = WeightFunction(base)
        self.rads = rads
        base_vals = deque()
        iq = deque()
        jq = deque()
        if len(rads) > 1:
            uni_rad = None
        else:
            uni_rad = rads[0]
        for i in xrange((len(xys))):
            w_dists = deque()
            if not uni_rad:
                w_rads = deque()
            
            for j in xrange((len(xys))):
                x_i, y_i = xys[i]
                x_j, y_j = xys[j]
                dist = ((x_j - x_i) ** 2 + (y_j - y_i) ** 2) ** 0.5
                if uni_rad:
                    rad = uni_rad
                else:
                    rad = rads[j]
                if dist < rad:
                    w_dists.append((dist,))
                    if not uni_rad:
                        w_rads.append(rad)
                    iq.append(i)
                    jq.append(j)
            if uni_rad:
                w_rads = rads    
            vs = self.base.values(w_dists, w_rads)
            base_vals.extend(vs[:, 0])
                
        main_mat = spm.csr_matrix((base_vals, (iq, jq)), (len(xys), len(xys)))
        self.a = spm_alg.spsolve(main_mat, xys_vals)
        self.set_diff_order(0)
    
    def set_diff_order(self, order):
        self._diff_order = order
        self.base.set_diff_order(order)
        
    def value(self, xy):
        res_length = output_length_2d(self._diff_order)
        res = np.ndarray((res_length,), dtype=np.double)
        dists, rads, indes = self._search_supporting(xy)
        vs = self.base.values(dists, rads)
        for i in xrange(res_length):
            t = 0
            k = 0
            for j in indes:
                t += vs[k, i] * self.a[j]
                k += 1
            res[i] = t
        return res
    
    def _search_supporting(self, xy):
        if len(self.rads) > 1:
            uni_rad = None
            rads_iter = iter(self.rads)
            res_rads = deque()
        else:
            uni_rad = self.rads[0]
        res_dists = deque()
        indes = deque()
        i = 0
        for coord in self.xys:
            if uni_rad:
                rad = uni_rad
            else:
                rad = next(rads_iter)
            x1, y1 = coord
            x, y = xy
            d = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
            if d < rad:
                indes.append(i)
                if self._diff_order == 0:
                    res_dists.append((d,))
                elif self._diff_order == 1:
                    if 0 != d:
                        res_dists.append((d, (x - x1) / d, (y - y1) / d))
                    else:
                        res_dists.append((0, 0, 0))
                if not uni_rad:
                    res_rads.append(rad)
            i += 1
        if uni_rad:
            return (res_dists, self.rads, indes)
        else:
            return (res_dists, res_rads, indes)  
                
