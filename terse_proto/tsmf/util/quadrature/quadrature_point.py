'''
Created on 2013-1-16

@author: Man YUAN <epsilonyuan@gmail.com>
'''
import numpy as np
class QuadraturePoint(object):
    def __init__(self,dim=2):
        self.weight=0.0
        self.coord=np.array((0.0,0.0),dtype=np.double)