'''
Created on 2013-1-17

@author: Man YUAN <epsilonyuna@gmail.com>
'''
import numpy as np
from terse_demo.util.java_code_gen import gen_array_code
consLaw = np.array([[11, 12, 0], [12, 22, 0], [0, 0, 33]], dtype=np.double)
shapeFuncVal = np.array([
                       [1.1, 2.0, -3.3, 0.4, 5.2, -6.0],
                       [21.1, 22.0, -23.3, 0.24, 25.2, -2.60],
                       [31.1, 22.0, -23.3, 3.4, 35.2, -36.0]])
B = np.zeros((3, 12), dtype=np.double)
PHI=np.zeros((12,2),dtype=np.double)
PHI[0::2,0]=shapeFuncVal[0]
PHI[1::2,1]=shapeFuncVal[0]
B[0, 0::2] = shapeFuncVal[1]
B[1, 1::2] = shapeFuncVal[2]
B[2, 0::2] = shapeFuncVal[2]
B[2, 1::2] = shapeFuncVal[1]

nodes_size = 10

penalty = 1e4

volumnForce = np.array([2.7, -3.6], dtype=np.double)

nodesIds = [9, 1, 3, 0, 7, 5]

def mat_convert_to_exps(m):
    exp_m = np.zeros((nodes_size * 2, nodes_size * 2),dtype=np.double)
    for i in xrange(len(nodesIds)):
        id_i=nodesIds[i]
        for j in xrange(len(nodesIds)):
            id_j=nodesIds[j]
            exp_m[id_i*2,id_j*2]=m[i*2,j*2]
            exp_m[id_i*2+1,id_j*2]=m[i*2+1,j*2]
            exp_m[id_i*2+1,id_j*2+1]=m[i*2+1,j*2+1]
            exp_m[id_i*2,id_j*2+1]=m[i*2,j*2+1]
    return exp_m

def vec_convert_to_exps(v):
    exp_v=np.zeros((nodes_size*2,),dtype=np.double)
    for i in xrange(len(nodesIds)):
        id_i=nodesIds[i]
        exp_v[id_i*2]=v[i*2]
        exp_v[id_i*2+1]=v[i*2+1]
    return exp_v

def gen_balance_exps_codes():
    m = B.transpose().dot(consLaw).dot(B)
    exp_m=mat_convert_to_exps(m);
    print "Start main matrix exp-----------------------------------------"
    print gen_array_code(exp_m)
    print "End main matrix exp--------------------------------------------"
    v=PHI.dot(volumnForce.transpose())
    exp_v=vec_convert_to_exps(v)
    print "\nStart main vector exp---------------------------------------"
    print gen_array_code(exp_v)
    print "End main vector exp---------------------------------------------"
  
def gen_dirichlet_exps_codes():
    m=PHI.dot(np.array([[penalty,0],[0,penalty]])).dot(PHI.transpose())
    exps_m=mat_convert_to_exps(m)
    print "Start main matrix exp-----------------------------------------"
    print gen_array_code(exps_m)
    print "End main matrix exp--------------------------------------------"
    v=PHI.dot(np.array([[penalty,0],[0,penalty]])).dot(volumnForce.transpose())
    exp_v=vec_convert_to_exps(v)
    print "\nStart main vector exp---------------------------------------"
    print gen_array_code(exp_v)
    print "End main vector exp---------------------------------------------"
   
            
        