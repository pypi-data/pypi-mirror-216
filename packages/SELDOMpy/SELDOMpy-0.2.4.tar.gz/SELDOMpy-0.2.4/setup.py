from setuptools import setup, Extension, find_packages
import glob

DESCRIPTION = 'Package for modelling cellular signalling networks'

ext_modules = [
    Extension(
        'SELDOMpy.hello',
        sources=glob.glob('src/*.c'),
        include_dirs=['include/include_amigo', 'include/include_cvodes'],
    )
]

setup(
    name='SELDOMpy',
    version='0.2.4',
    description=DESCRIPTION,
    packages=find_packages(),
    ext_modules=ext_modules,
    install_requires=["numpy", "scikit-learn", "pandas", "mealpy", "matplotlib", "setuptools"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)