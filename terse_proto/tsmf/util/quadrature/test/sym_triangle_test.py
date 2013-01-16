'''
Created on 2013-1-16

@author: Man YUAN <epsilonyuan@gmail.com>
'''

import numpy as np
from terse_proto.tsmf.util.quadrature import SymTriangleQuadrature
from terse_proto.tsmf.shape_func import MonomialBasis
from scipy.integrate import dblquad
from nose.tools import ok_
class Random2DPolygon(object):
    def value(self, vec):
        bs = self.basis.values(vec)
        return np.dot(bs, self.pars)[0]
    
    def __init__(self, power):
        self.basis = MonomialBasis(power)
        self.pars = np.random.randn(self.basis.basis_length())
        
def area_test():
    x1, y1, x2, y2, x3, y3 = (0.0, 0.0, 10.0, 0.0, 5.0, 10.0)
    height = 0.8
    exp = height * x2 * y3 * 0.5
    class SampleFunc(object):
        def value(self, vec):
            return height
    func = SampleFunc()
    ts = SymTriangleQuadrature(x1, y1, x2, y2, x3, y3, 1)
    for power in xrange(SymTriangleQuadrature.MIN_POWER, 1 + SymTriangleQuadrature.MAX_POWER):
        ts.set_power(power)
        act = ts.quadrate(func)
        ok_(abs(act - exp) < 1e-12)

def polygon_test():
    x1, y1, x2, y2, x3, y3 = (0.1, 0.3, 10.2, 1.1, 5.5, 4.9)
    triQuad = SymTriangleQuadrature(x1, y1, x2, y2, x3, y3, 1)
    for power in xrange(1, SymTriangleQuadrature.MAX_POWER + 1):
        randPoly = Random2DPolygon(power)
        for i in xrange(power, SymTriangleQuadrature.MAX_POWER + 1):
            triQuad.set_power(i)
            act = triQuad.quadrate(randPoly)
            exp1, _abserr1 = dblquad(lambda y, x:-randPoly.value([x, y]), x1, x2,
                         lambda x:0.0,
                         lambda x:(x - x1) / (x2 - x1) * (y2 - y1) + y1)
            exp2, _abserr2 = dblquad(lambda y, x:randPoly.value([x, y]), x1, x3,
                         lambda x:0.0,
                         lambda x:(x - x1) / (x3 - x1) * (y3 - y1) + y1)
            exp3, _abserr3 = dblquad(lambda y, x:randPoly.value([x, y]), x3, x2,
                        lambda x:0.0,
                        lambda x:(x - x2) / (x3 - x2) * (y3 - y2) + y2)
            exp = exp1 + exp2 + exp3
            ok_(abs(exp - act) <= max(exp * 1e-7, 1e-7))
            
