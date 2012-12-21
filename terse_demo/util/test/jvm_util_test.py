'''
Created on 2012-12-21

@author: Man YUAN <epsilonyuan@gmail.com>
'''

from terse_demo.util import jvm_util
from jpype import JPackage
import glob
from nose.tools import eq_, ok_

def class_load_test():
    (lib_path, jvm_path, switches) = jvm_util.start_jvm()
    jar_list = glob.glob(lib_path)
    ok_(len(jar_list) > 0, 'Can not find the jar file, please build it before testing')
    
    Node = JPackage('net').epsilony.tsmf.model.Node
    
    ok_(Node.__name__ == 'net.epsilony.tsmf.model.Node', 'Can\'t load class Node properly')
    
if __name__ == '__main__':
    class_load_test()
    
