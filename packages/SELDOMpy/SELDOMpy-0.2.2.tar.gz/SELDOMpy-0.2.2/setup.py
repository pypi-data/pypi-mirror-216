from distutils.core import setup

DESCRIPTION = 'Package for modelling cellular signalling networks'
setup(
    name='SELDOMpy',  # How you named your package folder (MyLib)
    packages=['SELDOMpy'],  # Chose the same as "name"
    version='0.2.2',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description=DESCRIPTION,  # Give a short description about your library
    author='Luis Prado',  # Type in your name
    author_email='pradolopezluis@gmail.com',  # Type in your E-Mail
    url='https://github.com/lupralo31/SELDOMpy',  # Provide either the link to your github or to your website
    download_url='https://github.com/lupralo31/SELDOMpy/archive/refs/tags/V_0.2.1.tar.gz',  # I explain this later on
    keywords=['SOME', 'MEANINGFULL', 'KEYWORDS'],  # Keywords that define your package best
    install_requires=["numpy", "scikit-learn", "pandas", "mealpy", "matplotlib", "setuptools"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.8',  # Specify which pyhton versions that you want to support
    ],
)
