from setuptools import setup, Extension, find_packages
import glob

from setuptools import setup

setup(
    name='SELDOMpy',
    version='0.2.5',
    packages=['SELDOMpy'],
    ext_modules=[
        Extension('hello', sources=['src/*.c',
                                    'include/include_amigo/*.h',
                                    'include/include_cvodes/cvodes/*.h',
                                    'include/include_cvodes/nvector/*.h',
                                    'include/include_cvodes/sundials/*.h'])
    ]
)

