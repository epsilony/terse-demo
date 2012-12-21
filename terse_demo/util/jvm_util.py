'''
Created on 2012-12-21

@author: Man YUAN <epsilonyuan@gmail.com>
'''
from jpype import *
import os

def start_jvm(debug_port=None):
    if isJVMStarted():
        print "JVM has been started!"
        if debug_port is not None:
            print("Warning the debug_port setting: " + 
                str(debug_port) + " may not be activate, if it hasn't been activate before")
        return (None, None, None)
    jvm_path = getDefaultJVMPath()
    terse_meshfree_path = os.getenv("TERSE_MESHFREE_PATH")
    switches = []
    if terse_meshfree_path is None:
        import terse_demo
        #switches.append('-Djava.class.path=/home/epsilon/SimpMeshfree/dist/SimpMeshfree.jar:/home/epsilon/SimpMeshfree/libs/JavaUtils/dist/EpsilonYUtil.jar')
        lib_path = terse_demo.__path__[0] + '/../../meshfree/dist/terse-meshfree.jar'
        lib_switch = '-Djava.class.path=' + lib_path
        print "lib_path is ", lib_path
        switches.append(lib_switch)
#    switches.append('net.epsilony.utils.geom.Coordinate')
    if debug_port is not None:
        switches.extend(["-Xdebug", "-Xrunjdwp:transport=dt_socket,address=" + str(debug_port) + ",server=y,suspend=n"])
    startJVM(jvm_path, *switches)
    return (lib_path, jvm_path, switches)
