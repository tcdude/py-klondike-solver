import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read()

setuptools.setup(
    name='py-klondike-solver',
    version=version,
    author='Tiziano Bettio',
    author_email='tc@tizilogic.com',
    description='Cython wrapper for Klondike-Solver.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tcdude/py-klondike-solver',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
