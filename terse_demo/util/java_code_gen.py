'''
Created on 2013-1-17

@author: Man YUAN <epsilonyuan@gmail.com>
'''
import numpy as np
def gen_array_code(np_arr):
    result="new double"
    for _i in xrange(len(np_arr.shape)):
        result+="[]"
    result+=_code_array_cont(np_arr)
    result+=';'
    return result

def _code_array_cont(np_arr):
    if len(np_arr.shape)>1:
        result="{"
        for i in xrange(np_arr.shape[0]):
            result+=_code_array_cont(np_arr[i])
            result+=',\n'
        result=result[:-2]
        result+="}"
    else:
        result="{"
        for i in xrange(np_arr.shape[0]):
            result+=str(np_arr[i])+', '
        result=result[:-2]
        result+="}"
    return result

if __name__=='__main__':
    t=np.array([[1,2,3],[4,5,6],[7,8,9]])
    print gen_array_code(t)