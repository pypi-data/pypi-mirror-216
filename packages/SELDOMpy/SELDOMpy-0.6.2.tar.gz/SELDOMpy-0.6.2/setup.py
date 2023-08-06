#!/usr/bin/env python
import sys
#import numpy as np
from distutils.core import Extension
from setuptools import setup
from Cython.Distutils import build_ext
import glob
import os



# Get numpy include directory (works across versions)
#numpy_include = np.get_include()



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

hello = Extension(name="hello",
                  sources=["src/AMIGO_problem.c", "src/cvodea.c", "src/cvodea_io.c",
                           "src/cvodes_band.c", "src/cvodes_bbdpre.c", "src/cvodes_diag.c",
                           "src/cvodes_dense.c", "src/cvodes_bandpre.c", "src/cvodes.c",
                           "src/AMIGO_model_stats.c", "src/AMIGO_model.c", "src/anODEModel.c",
                           "src/cvodes_direct.c", "src/cvodes_io.c", "src/cvodes_spbcgs.c",
                           "src/cvodes_spgmr.c", "src/cvodes_spils.c", "src/cvodes_sptfqmr.c",
                           "src/decimal2binary.c", "src/dhc.c", "src/fnvector_serial.c",
                           "src/findStates.c", "src/get_count_bits.c", "src/get_support_truth_tables.c",
                           "src/get_input_index.c", "src/get_truth_tables_index.c", "src/getAdjacencyMatrix.c",
                           "src/getNumBits.c", "src/getNumInputs.c", "src/getStateIndex.c", "src/getTruthTables.c",
                           "src/hill_function.c", "src/linear_transfer_function.c", "src/normHill.c",
                           "src/nvector_serial.c", "src/printAdjMat.c", "src/printInterMat.c",
                           "src/printNminiTerms.c", "src/printTruthTables.c", "src/sim_logic_ode.c",
                           "src/sim_logic_ode_R.c", "src/simulate_amigo_model.c", "src/sundials_band.c",
                           "src/sundials_dense.c", "src/sundials_direct.c", "src/sundials_iterative.c",
                           "src/sundials_math.c", "src/sundials_nvector.c", "src/sundials_spbcgs.c",
                           "src/sundials_spgmr.c", "src/sundials_sptfqmr.c"],
                  libraries=libs,
                  include_dirs=['include/include_amigo', 'include/include_cvodes'],
                  library_dirs=["src"],
                  extra_compile_args=extra
                  )

setup(name="SELDOMpy",
      description="Code for xQML",
      author="S. Vanneste & M. Tristram",
      version="0.6.2",
      packages=['SELDOMpy'],
      ext_modules=[hello],
      install_requires=["numpy", "scikit-learn", "pandas", "mealpy", "matplotlib", "Cython"],
      cmdclass={'build_ext': build_ext}
      )
