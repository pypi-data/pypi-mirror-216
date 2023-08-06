from setuptools import setup, dist
from setuptools.command.install import install
import os

# force setuptools to recognize that this is
# actually a binary distribution
class BinaryDistribution(dist.Distribution):
    def has_ext_modules(foo):
        return True

# optional, use README.md as long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    # this package is called mymodule
    name='pyfigtree',

    # this package contains one module,
    # which resides in the subdirectory mymodule
    packages=['pyfigtree', 'pyfigtree.lib'],

    # make sure the shared library is included
    package_data={'pyfigtree': ['lib/libfigtree.so', 'lib/libann_figtree_version.so']},
    include_package_data=True,

    description="Python ctypes wrapper of the figtree library for fast Gaussian summation",
    # optional, the contents of README.md that were read earlier
    long_description=long_description,
    long_description_content_type="text/markdown",

    # See class BinaryDistribution that was defined earlier
    distclass=BinaryDistribution,

    version='1.0',
    author="Frederik Beaujean",
    author_email="Frederik.Beaujean@lmu.de",
    url="https://github.com/fredRos/pyfigtree"
)
