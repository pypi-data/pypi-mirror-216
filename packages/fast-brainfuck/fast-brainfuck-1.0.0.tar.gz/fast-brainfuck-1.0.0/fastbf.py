import platform,os
import sys
from random import choice
from setuptools import setup,Extension
from pybind11 import get_include
from subprocess import run,PIPE
def random_string():
    """
    Random string for directory name
    :return: Random string.
    """
    return ''.join([choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM') for i in range(12)])
def _tmp():
    if platform.system()=='Windows':
        return os.environ['TMP'] # For Windows.
    else:
        return '/tmp' # For Non-Windows OS's.
def brainfuck_to_cpp(brainfuck,cellsize=300000):
    """
    Convert brainfuck into C++ code.
    :param brainfuck: Brainfuck code.
    :param cellsize: Number of cells, default is 300000.
    :return: C++ code equivalent to the input brainfuck code.
    """
    if not isinstance(cellsize,int):
        raise ValueError('Cell size must be integer.')
    code='void run(){\n'
    code+='    char cell['+str(cellsize)+']={0};\n    int p=0;\n'
    translate={'>':'p++;','<':'p--;',',':'cell[p]=getchar();','.':'putchar(cell[p]);','[':'while(cell[p]){',']':'}','+':'++cell[p];','-':'--cell[p];'}
    for i in brainfuck:
        if i in translate:
            code += '    '+translate[i]+'\n'
    code+='}'
    return code
def wrap_cpp(cpp):
    """
    Wrap C++ code into code usable by Python.
    :param cpp: C++ code
    :return: Wrapped code
    """
    code='''
#include<pybind11/pybind11.h>
#include<cstdio>
namespace py=pybind11;
    '''
    code+=cpp
    code+='''
PYBIND11_MODULE(_foo,self){
    self.def("run",&run);
}
    '''
    return code
def dist_cpp(cpp):
    """
    Distribute C++ code into Python module.
    :param cpp: C++ code
    :return: None
    """
    with open('_foo.cpp','w') as f:
        f.write(cpp)
    _foo=Extension(
        name='_foo',
        sources=['_foo.cpp'],
        language='c++',
        include_dirs=[get_include()],
        extra_compile_args=['-std=c++11']
    )
    setup(
        ext_modules=[_foo]
    )
def brainfuck_to_function(brainfuck):
    """
    Converts brainfuck into a fast Python function.
    :param brainfuck: Brainfuck code
    :return: A function, call it with no arguments to run the brainfuck code
    """
    cwd=os.getcwd()
    os.chdir(_tmp())
    dn=random_string()
    os.mkdir(dn)
    os.chdir(dn)
    distcode='''
from setuptools import setup,Extension
from pybind11 import get_include
_foo=Extension(
    name='_foo',
    sources=['_foo.cpp'],
    language='c++',
    include_dirs=[get_include()],
    extra_compile_args=['-std=c++11']
)
setup(
    ext_modules=[_foo]
)
    '''
    cpp=brainfuck_to_cpp(brainfuck)
    wrap=wrap_cpp(cpp)
    with open('_foo.cpp','w') as f:
        f.write(wrap)
    with open('setup.py','w') as f:
        f.write(distcode)
    python=sys.executable
    run(
        [
            python,
            'setup.py',
            'build_ext',
            '--inplace',
        ],shell=True,stdout=PIPE,stderr=PIPE
    )
    sys.path.append(os.path.join(_tmp(),dn))
    foo=__import__('_foo')
    os.chdir(cwd)
    sys.path.pop()
    return foo.run
def dist_brainfuck(brainfuck,modulename='foo'):
    """
    Distribute brainfuck code into a python module.
    :param brainfuck: Brainfuck code
    :param modulename: Python module name.
    :return: None
    """
    with open(modulename+'.py','w') as f:
        f.write('from ._foo import *')
    cpp = brainfuck_to_cpp(brainfuck)
    wrap = wrap_cpp(cpp)
    dist_cpp(wrap)
def _fastbf_inter():
    from argparse import ArgumentParser
    ap=ArgumentParser(description='FastBF brainfuck interpreter')
    ap.add_argument('filename',help='Input brainfuck file name')
    args=ap.parse_args()
    with open(args.filename) as f:
        code=f.read()
    func=brainfuck_to_function(code)
    func()
if __name__=='__main__':
    _fastbf_inter()