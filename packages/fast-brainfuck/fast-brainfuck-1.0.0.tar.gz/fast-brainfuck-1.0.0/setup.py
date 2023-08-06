from setuptools import setup
def readme():
    with open('README.md','r') as f:
        return f.read()
setup(
    name='fast-brainfuck',
    py_modules=['fastbf'],
    version='1.0.0',
    entry_points={
        'console_scripts':[
            'fastbf=fastbf:_fastbf_inter'
        ]
    },
    description='Brainfuck "compiler" for Python (fast)',
    long_description=readme(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['pybind11','setuptools'],
    keywords=['brainfuck'],
    classifiers=[
        'Programming Language :: C++',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 6 - Mature'
    ]
)
