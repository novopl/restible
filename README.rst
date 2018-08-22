
restible
########

.. readme_inclusion_marker

**restible** is a python library for creating consistent code for REST APIs
across different frameworks. The main motivation was that the framework used
is often dictated by requirements and I wanted to have a concise way of writing
API endpoints no matter the underlying framework.

**WARNING: Pre release state**: The library is not ready for general public. The
core has a pretty good test coverage but the integrations with frameworks don't.
A large part of the code is documented through docstrings but the general
purpose docs are not written yet nor are any tutorials. The project versioning
is also a bit random at this point, but will follow semantic versioning from now
on. Until 1.0 the minor version bumps will have changes to the interface that
in some cases might break existing code. The patch version updates will have
backwards compatible code.


.. note::
    The CircleCI builds can be found
    `here <https://circleci.com/gh/novopl/restible>`_

Installation
============

.. code-block:: shell

    $ pip install restible


Contributing
============

Setting up development repo
---------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/restible.git
    $ cd restible
    $ virtualenv env
    $ source ./env/bin/activate
    $ pip install -r requirements.txt -r ops/devrequirements.txt
    $ peltak git add-hooks


Running tests
.............

**Config**: The types of tests are defined in ``pelconf.py`` and the
pytest configuration is defined in ``ops/tools/pytest.ini``.

.. code-block:: shell

    $ peltak test

Linting
.......

**Config**: The list of locations to lint is defined in ``pelconf.py`` and the
linters configuration is defined in ``ops/tools/{pylint,pep8}.ini``.

.. code-block:: shell

    $ peltak lint

Generating docs
...............

**Config**: The list of documented files and general configuration is in
``pelconf.py`` and the Sphinx configuration is defined in ``docs/conf.py``.

.. code-block:: shell

    $ peltak docs
