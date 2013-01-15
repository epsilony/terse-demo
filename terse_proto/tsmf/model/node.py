'''
Created on 2013-1-15


@author: Man YUAN <epsilonyuan@gmail.com>

@author: Sparrow HU <huhao200709@163.com>
'''

import numpy as np

class Node(object):
    def __init__(self, array=None):
        if None is not array:
            self.coord = np.array(array, dtype=np.double)
        else:
            self.coord = None
        self.id = 0