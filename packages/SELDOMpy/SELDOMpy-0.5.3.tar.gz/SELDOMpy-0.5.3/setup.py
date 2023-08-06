from setuptools import setup, Extension, find_packages

import glob
import os

DESCRIPTION = 'Package for modelling cellular signalling networks'

setup(
    name='SELDOMpy',
    packages=find_packages(),
    version='0.5.3',
    license='MIT',
    description=DESCRIPTION,
    author='Luis Prado',
    author_email='pradolopezluis@gmail.com',
    url='https://github.com/lupralo31/SELDOMpy',
    download_url='https://github.com/lupralo31/SELDOMpy/archive/refs/tags/V_0.2.1.tar.gz',
    keywords=['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=["numpy", "scikit-learn", "pandas", "mealpy", "matplotlib", "setuptools"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
