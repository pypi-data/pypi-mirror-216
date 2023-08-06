#!/usr/bin/env python
import sys
import numpy as np
from distutils.core import setup, Extension
from Cython.Distutils import build_ext
import glob
import os

# Get numpy include directory (works across versions)
numpy_include = np.get_include()

print(sys.argv)

if '--disable-openmp' in sys.argv:
    sys.argv.pop(sys.argv.index('--disable-openmp'))
    USE_OPENMP = False
else:
    USE_OPENMP = True

if '--icc' in sys.argv:
    sys.argv.pop(sys.argv.index('--icc'))
    USE_ICC = True
else:
    USE_ICC = False

libs = ['m']

extra = ['-std=gnu99']
if USE_ICC:
    if USE_OPENMP:
        libs += ['gomp', 'iomp5']
        extra += ['-openmp']
else:
#    extra += ['-O2']
    if USE_OPENMP:
        libs += ['gomp']
        extra += ['-fopenmp']


hello = Extension( name="hello",
                    sources=["SELDOMpy/src/*.c"],
                    libraries=libs,
                    include_dirs=['SELDOMpy/include/include_amigo', 'SELDOMpy/include/include_cvodes', numpy_include],
                    library_dirs=["SELDOMpy/src"],
                    extra_compile_args=extra
                    )

setup(name="SELDOMpy",
      description="Code for xQML",
      author="S. Vanneste & M. Tristram",
      version="0.5.1",
      packages=['SELDOMpy'],
      ext_modules=[hello],
      install_requires=["numpy", "scikit-learn", "pandas", "mealpy", "matplotlib", "Cython"],
      cmdclass={'build_ext': build_ext}
      )
