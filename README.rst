
restible
########

.. about_project_start

**restible** is a python library for creating consistent code for REST APIs
across different frameworks. The main motivation was that the framework used
is often dictated by requirements and I wanted to have a concise way of writing
API endpoints no matter the underlying framework.

.. about_project_end

.. project_links_start

Useful links
============

- `Docs <https://novopl.github.io/restible>`_
- `Source Code <https://github.com/novopl/restible>`_
- `CI Builds <https://circleci.com/gh/novopl/restible>`_

Related libraries
-----------------

- `restible-flask <https://github.com/novopl/restible-flask>`_
- `restible-sqlalchemy <https://github.com/novopl/restible-sqlalchemy>`_
- `restible-appengine <https://github.com/novopl/restible-appengine>`_
- `restible-django <https://github.com/novopl/restible-django>`_


Installation
============

.. code-block:: shell

    $ pip install restible

.. project_links_end

Contributing
============

.. readme_contrib_start

.. note::
    The library has a pretty good test coverage but not yet at 100%. A large
    part of the code is documented through docstrings but the general purpose
    docs are not written yet nor are any tutorials.

Cloning and setting up the development repo
-------------------------------------------

.. code-block:: shell

    $ git clone git@github.com:novopl/restible.git
    $ cd restible
    $ virtualenv env
    $ source ./env/bin/activate
    $ pip install -r requirements.txt -r ops/devrequirements.txt
    $ peltak git add-hooks


Running tests
-------------

**Config**: The types of tests are defined in ``pelconf.py`` and the
pytest configuration is defined in ``ops/tools/pytest.ini``.

.. code-block:: shell

    $ peltak test

Linting
-------

**Config**: The list of locations to lint is defined in ``pelconf.py`` and the
linters configuration is defined in ``ops/tools/{pylint,pep8}.ini``.

.. code-block:: shell

    $ peltak lint

Generating docs
---------------

**Config**: The list of documented files and general configuration is in
``pelconf.py`` and the Sphinx configuration is defined in ``docs/conf.py``.

.. code-block:: shell

    $ peltak docs

.. readme_contrib_end
