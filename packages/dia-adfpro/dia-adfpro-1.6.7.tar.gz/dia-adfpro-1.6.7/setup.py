from setuptools import setup, find_packages
from codecs import open
import numpy
import os

# thanks Pipy for handling markdown now
ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, 'README.md'), encoding="utf-8") as f:
    README = f.read()

import diaadfpro
VERSION = diaadfpro.__version__

# The following block
# is copied from sklearn as a way to avoid cythonizing source
# files in source dist
# We need to import setuptools before because it monkey-patches distutils
#from distutils.command.sdist import sdist
#cmdclass = {'sdist': sdist}

setup(
    name='dia-adfpro',  # How you named your package folder (MyLib)
    description='A Python application for anomaly detection',  # Short description about your library
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT',
    include_dirs=[numpy.get_include()],
    packages=find_packages(),
    install_requires=[
        'dia-aiml'
    ],
    version=VERSION,
    url="https://github.com/EliLillyCo/MQIT_DIA_ADFPRO",
    author='Francesco Gabbanini, Manjunath Bagewadi, Henson Tauro',  # Type in your name
    author_email='fgabbanini@yahoo.it',  # Type in your E-Mail
)