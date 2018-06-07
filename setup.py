from distutils.core import setup

setup(
    name='matSHEEP',
    version='0.2.0',
    author='Amartya Sanyal',
    author_email='amartya18x@gmail.com',
    packages=['matSHEEP'],
    #scripts=['bin/stowe-towels.py', 'bin/wash-towels.py'],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Programmatic interface to SHEEP',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "multiprocessing",
        "networkx",
        "tqdm"
    ],
)
