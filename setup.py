from distutils.core import setup

setup(
    name='matSHEEP',
    version='1.4.5',
    author='Amartya Sanyal',
    author_email='amartya18x@gmail.com',
    packages=['matSHEEP'],
    #scripts=['bin/stowe-towels.py', 'bin/wash-towels.py'],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE',
    description='Programmatic interface to SHEEP',
    long_description=open('docs/README.rst').read(),
    install_requires=[
        "numpy",
        "multiprocessing",
        "networkx",
        "tqdm",
        "pillow"
    ],
)
