#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from distutils.core import Extension
from distutils.log import warn
from Cython.Distutils import build_ext

import re
import os


with open('README.md') as f:
    readme = f.read()

with open('czifile/__init__.py') as f:
    text = f.read()

version = re.search("__version__ = '(.*?)'", text).groups()[0]

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()
    
setup_args = dict(
    name='czifile',
    version=version,
    install_requires=required,
    setup_requires=['Cython','numpy'],
    description='Read and write image data from and to CZI files.',
    long_description=readme,
    author='Christoph Gohlke', 
    author_email='cgohlke@uci.edu',
    maintainer='Dave Williams',
    maintainer_email='cdavew@alleninstitute.org',
    url='https://github.com/AllenCellModeling/czifile',
    include_package_data=True,
    install_requires=[
        'numpy>=1.8.2',
        'enum34;python_version<"3.0"',
        'futures; python_version == "2.7"'
    ],
    license="BSD",
    zip_safe=False,
    packages=find_packages(),
    keywords='czifile',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        "Programming Language :: C",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)

try:
    import numpy
    setup_args['cmdclass']= {'build_ext': build_ext}

    jxrlib_dir = 'czifile/jxrlib'
    jpeg_dir = 'czifile/libjpeg'
    include_dirs = [numpy.get_include(),'/usr/local/include','/usr/local/include/libjxr']
    include_dirs += jpeg_dir
    include_dirs += [os.path.join(jxrlib_dir, d) for d in 
                     ('jxrgluelib', 'image/sys', 'common/include')]
    library_dirs = ['/usr/local/lib']	
    
    extra_compile_args = ['-std=c11','-D__ANSI__',
                          '-mmacosx-version-min=10.7']

    setup_args['ext_modules'] = [
        Extension('czifile._czifile',
                  ['czifile/_czifile.pyx'],
                  include_dirs=include_dirs, 
                  library_dirs=library_dirs,
                  libraries=['jpeg','jpegxr','jxrglue'],
                  extra_compile_args=extra_compile_args)
    ]
except ImportError:
    warn('Cannot build the extension module without numpy')


setup(**setup_args)
