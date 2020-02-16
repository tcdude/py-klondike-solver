Installing pyksolve
===================

Dependencies
############

pyksolve requires Python 3.6 or higher.

Currently no binary wheels are available nor is the package available on PyPI.
Before installing, you need to make sure to have a C++ tool chain and the
Python header files for your Python version installed/available.

On Debian/Ubuntu based systems, this command should install all dependencies for
you:

.. code-block:: bash

    sudo apt install build-essential python3-dev

Installation
############

To install directly from the master branch of pyksolve, using ``pip`` 
(or ``pip3`` in some cases):

.. code-block:: bash

    pip install git+https://github.com/tcdude/py-klondike-solver.git
