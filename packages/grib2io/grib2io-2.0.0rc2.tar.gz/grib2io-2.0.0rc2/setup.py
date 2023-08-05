from setuptools import setup, Extension
from os import environ
import configparser
import numpy
import os
import platform
import sys

VERSION = '2.0.0rc2'

# ----------------------------------------------------------------------------------------
# Class to parse the setup.cfg
# ----------------------------------------------------------------------------------------
class _ConfigParser(configparser.ConfigParser):
    def getq(self, s, k, fallback):
        try:
            return self.get(s, k)
        except:
            return fallback

# ----------------------------------------------------------------------------------------
# Build time dependancy
# ----------------------------------------------------------------------------------------
try:
    from Cython.Distutils import build_ext
    cmdclass = {'build_ext': build_ext}
    redtoreg_pyx = 'redtoreg.pyx'
    g2clib_pyx  = 'g2clib.pyx'
except(ImportError):
    cmdclass = {}
    redtoreg_pyx = 'redtoreg.c'
    g2clib_pyx  = 'g2clib.c'

# ---------------------------------------------------------------------------------------- 
# Read setup.cfg. Contents of setup.cfg will override env vars.
# ----------------------------------------------------------------------------------------
setup_cfg = environ.get('GRIB2IO_SETUP_CONFIG', 'setup.cfg')
config = _ConfigParser()
if os.path.exists(setup_cfg):
    sys.stdout.write('Reading from setup.cfg...')
    config.read(setup_cfg)

# ---------------------------------------------------------------------------------------- 
# Get NCEPLIBS-g2c library info
# ---------------------------------------------------------------------------------------- 
incdirs=[]
libdirs=[]
g2c_dir = config.getq('directories', 'g2c_dir', environ.get('G2C_DIR'))
g2c_libdir = config.getq('directories', 'g2c_libdir', environ.get('G2C_LIBDIR'))
g2c_incdir = config.getq('directories', 'g2c_incdir', environ.get('G2C_INCDIR'))
if g2c_libdir is None and g2c_dir is not None:
    libdirs.append(os.path.join(g2c_dir,'lib'))
    libdirs.append(os.path.join(g2c_dir,'lib64'))
else:
    libdirs.append(g2c_libdir)
if g2c_incdir is None and g2c_dir is not None:
    incdirs.append(os.path.join(g2c_dir,'include'))
else:
    incdirs.append(g2c_incdir)

# ----------------------------------------------------------------------------------------
# Cleanup library and include path lists to remove duplicates and None.
# ----------------------------------------------------------------------------------------
libdirs = [l for l in set(libdirs) if l is not None]
incdirs = [i for i in set(incdirs) if i is not None]
runtime_libdirs = libdirs if os.name != 'nt' else None
incdirs.append(numpy.get_include())

# ----------------------------------------------------------------------------------------
# Define extensions
# ---------------------------------------------------------------------------------------- 
g2clibext = Extension('grib2io.g2clib',[g2clib_pyx],include_dirs=incdirs,\
            library_dirs=libdirs,libraries=['g2c'],runtime_library_dirs=runtime_libdirs)
redtoregext = Extension('grib2io.redtoreg',[redtoreg_pyx],include_dirs=[numpy.get_include()])

# ----------------------------------------------------------------------------------------
# Create __config__.py
# ----------------------------------------------------------------------------------------
cnt = \
"""# This file is generated by grib2io's setup.py
# It contains configuration information when building this package.
grib2io_version = '%(grib2io_version)s'
"""
a = open('grib2io/__config__.py','w')
cfgdict = {}
cfgdict['grib2io_version'] = VERSION
try:
    a.write(cnt % cfgdict)
finally:
    a.close()

# ----------------------------------------------------------------------------------------
# Import README.md as PyPi long_description
# ----------------------------------------------------------------------------------------
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# ----------------------------------------------------------------------------------------
# Run setup.py.  See pyproject.toml for package metadata.
# ----------------------------------------------------------------------------------------
setup(ext_modules = [g2clibext,redtoregext],
      cmdclass = cmdclass,
      long_description = long_description,
      long_description_content_type = 'text/markdown')
