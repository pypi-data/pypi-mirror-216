from distutils.core import setup, Extension
import glob
import os

DESCRIPTION = 'Package for modelling cellular signalling networks'

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.misc_util import get_info

    # Necessary for the half-float d-type.
    info = get_info('npymath')

    config = Configuration('',
                           parent_package,
                           top_path)
    config.add_extension('hello', sources=glob.glob(os.path.join(os.getcwd(), 'src', '*.c')), **info)
    config.add_include_dirs(['include/include_amigo', 'include/include_cvodes'])

    return config

if __name__ == "__main__":
    setup(
        name='SELDOMpy',
        packages=['SELDOMpy'],
        version='0.2.9',
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
        **configuration().todict()
    )
