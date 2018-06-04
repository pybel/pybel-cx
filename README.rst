PyBEL-CX
========
A PyBEL extension for interconversion with CX

Installation
------------
Before this is deployed to PyPI, it can be installed with:

.. code-block:: sh

   $ python3 -m pip install git+https://github.com/pybel/pybel-cx.git

Command Line Usage
------------------
PyBEL-CX installs two command line utilities: ``bel_to_cx`` and ``cx_to_bel``.

CX to BEL
~~~~~~~~~
Running this script has the caveat that the CX document should conform to the schema created by PyBEL-CX.

.. code-block:: sh

   $ cat my_network.cx | cx_to_bel > my_network.bel

BEL to CX
~~~~~~~~~
.. code-block:: sh

   $ cat my_network.bel | bel_to_cx > my_network.cx
