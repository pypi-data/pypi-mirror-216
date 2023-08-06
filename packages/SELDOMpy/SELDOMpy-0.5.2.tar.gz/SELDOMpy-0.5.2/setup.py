from distutils.core import setup, Extension
import glob
import os

DESCRIPTION = 'Package for modelling cellular signalling networks'

hello_module = Extension(
    'SELDOMpy.hello',  # Nombre del módulo
    sources=['src/*.c'],  # Lista de archivos fuente (.c)
    include_dirs=['include/include_amigo', 'include/include_cvodes'],  # Lista de directorios de inclusión
    define_macros=[],  # Macros de compilación opcionales
    undef_macros=[],  # Macros de compilación para deshabilitar
    library_dirs=[],  # Directorios de búsqueda de bibliotecas
    libraries=[],  # Bibliotecas a enlazar
)

setup(
    name='SELDOMpy',
    packages=['SELDOMpy'],
    version='0.5.2',
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
    ext_modules=[hello_module],  # Agregar el módulo "hello" como extensión
)
