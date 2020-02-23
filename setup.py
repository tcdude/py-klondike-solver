import os
import platform
from setuptools import setup
from setuptools import find_namespace_packages
from distutils.extension import Extension
from Cython.Build import cythonize

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.0.6'
__copyright__ = """
Copyright (c) 2020 Tiziano Bettio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read()

if platform.system() == 'Windows':
    extensions = [
        Extension(
            '*',
            ['src/**/*.pyx'],
            include_dirs=['ext/klondike-solver'],
        )
    ]
elif platform.system() == 'Darwin':
    extensions = [
        Extension(
            '*',
            ['src/**/*.pyx'],
            include_dirs=['ext/klondike-solver'],
            extra_compile_args=['-std=c++11', '-stdlib=libc++'],
            extra_link_args=['-std=c++11', '-stdlib=libc++']
        )
    ]

else:
    extensions = [
        Extension(
            '*',
            ['src/**/*.pyx'],
            include_dirs=['ext/klondike-solver'],
            extra_compile_args=['-std=c++11'],
            extra_link_args=['-std=c++11']
        )
    ]


setup(
    name='pyksolve',
    version=version,
    author='Tiziano Bettio',
    author_email='tc@tizilogic.com',
    description='Cython wrapper for Klondike-Solver.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tcdude/py-klondike-solver',
    packages=find_namespace_packages(where='src'),
    package_data={'pyksolve': [
        'LICENSE.md',
        'VERSION'
    ]},
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    setup_requires=['Cython'],
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': 3, 'embedsignature': True},
        annotate=False
    ),
)
