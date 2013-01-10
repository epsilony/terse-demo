'''
Created on 2012-12-31

@author: Man YUAN <epsilonyuan@gmail.com>
'''
import numpy as np
from terse_proto.tsmf.util.part_diff_math import output_length_2d
from terse_proto.tsmf.shape_func.radial_funcs import RadialFunction
from terse_proto.tsmf.shape_func.bases_func import MonomialBases

def _dists(center, coords, diff_order):
    num_col = output_length_2d(diff_order)
    result = np.ndarray((len(coords), num_col), dtype=np.double)
    for i in xrange(len(coords)):
        d_xy = center - coords[i]
        dst = np.dot(d_xy, d_xy) ** 0.5
        result[i][0] = dst
        if diff_order == 1:
            if dst == 0:
                result[i, 1:] = 0
            else:
                result[i][1] = d_xy[0] / dst
                result[i][2] = d_xy[1] / dst  
    return result

class MLS(object):
    '''
    classdocs
    '''
    def set_diff_order(self, order):
        if order > 1:
            raise ValueError("Only supports 0 or 1 differential order")
        # self.bases_func.set_diff_order(order) #nonsense about mls
        self.weight_func.set_diff_order(order)
        self._diff_order = order
        self.mat_As = []
        base_dim = self.bases_func.size()
        self._t_mat=np.ndarray((base_dim,base_dim),dtype=np.double)
        for _i in xrange(output_length_2d(order)):
            self.mat_As.append(np.ndarray((base_dim, base_dim), dtype=np.double))   
    
    def _get_diff_order(self):
        return self._diff_order
    
    diff_order = property(_get_diff_order, set_diff_order)
    
    def __init__(self, weight_func=None, bases_func=None):
        '''
        Constructor
        '''
        if None is weight_func:
            self.weight_func = RadialFunction()
        else:
            self.weight_func = weight_func
        if None is bases_func:
            self.bases_func = MonomialBases()
        else:
            self.bases_func = bases_func
        self.set_diff_order(0)
        
    def _zero_mat_As(self):   
        for mat_A in self.mat_As:
            mat_A.fill(0)
    
    def _gen_mat_Bs(self,coords_lens):
        mat_Bs = []
        for _i in xrange(output_length_2d(self.diff_order)):
            mat_Bs.append(np.zeros((coords_lens, self.bases_func.size())))
        return mat_Bs
        
    
    def values(self, center, coords, influence_rads, dists=None):
        center=np.array(center,dtype=np.double)
        
        if None is dists:
            dists = _dists(center, coords, self.diff_order)   
        
        weights = self.weight_func.values(dists, influence_rads)
        
        self._zero_mat_As()
        mat_As = self.mat_As

        t_mat = self._t_mat
        
        num_col = output_length_2d(self.diff_order)
        
        mat_Bs=self._gen_mat_Bs(len(coords))
        
        self.bases_func.set_diff_order(0)
        for i in xrange(len(coords)):
            nd_crd = coords[i]
            p = self.bases_func.values(nd_crd - center)
            
            for diff_index in xrange(num_col):
                w = weights[i][diff_index]
                
                mat_B = mat_Bs[diff_index]
                mat_B[i] = p
                mat_B[i] *= w
                
                mat_A = mat_As[diff_index]
                
                np.multiply(p.reshape((-1, 1)), p, t_mat)
                t_mat *= w
                mat_A += t_mat
        
        self.bases_func.set_diff_order(self.diff_order)
        if self.diff_order > 0:
            self.bases_func.set_diff_order(self.diff_order)
        p = self.bases_func.values((0.0,0.0))
        g = np.linalg.solve(mat_As[0], p[0])
        
        results = np.ndarray((len(coords), num_col), dtype=np.double)
        results[:, 0] = np.dot(mat_Bs[0] , g)
        
        if self.diff_order > 0:
            g_x = np.linalg.solve(mat_As[0], p[1] - np.dot(mat_As[1], g))
            g_y = np.linalg.solve(mat_As[0], p[2] - np.dot(mat_As[2] , g))
            results[:, 1] = np.dot(mat_Bs[1], g) + np.dot(mat_Bs[0], g_x)
            results[:, 2] = np.dot(mat_Bs[2], g) + np.dot(mat_Bs[0], g_y)
        
        return results
    
