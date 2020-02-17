Installing pyksolve
===================

Dependencies
############

pyksolve requires Python 3.6 or higher.

There are currently binary wheels available for Linux, macOSX and Windows on
PyPI for various Python versions.

Installing binary wheels
########################

Run the following command:

.. code-block:: bash

    pip3 install --upgrade pyksolve


Installing from source
######################

Otherwise the package can be built from source, which requires a C++ tool chain
installed.

On Debian/Ubuntu based **Linux**, this command will install all
dependencies you need to build pyksolve:

.. code-block:: bash

    sudo apt install build-essential python3-dev

On **Windows**, `this <https://wiki.python.org/moin/WindowsCompilers>`_ wiki
page contains all necessary information to get a compiler installed.

This package is not, as of yet tested on **macOS**, although in CI it seems to
build correctly for Python 3.8 .

PyPI
****

To install the source distribution from PyPI, run:

.. code-block:: bash

    pip3 install --upgrade --no-binary pyksolve


GitHub
******

To install directly from the master branch of pyksolve, run the following
command:

.. code-block:: bash

    pip3 install --upgrade git+https://github.com/tcdude/py-klondike-solver.git
