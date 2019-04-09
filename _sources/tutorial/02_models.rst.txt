################################
Using ``restible.ModelResource``
################################


.. note::
    You can get the full source code for this example
    `here <https://github.com/novopl/restible/tree/master/docs/examples/02_models>`_.

.. contents:: Table of Contents
    :local:

Improve the code structure
==========================

The app in this section will have almost the same level of complexity so we
could still implement this section as a single file. We do know the app will
grow in the future sections so we might go ahead and structure the project
files a bit better so it's easier to extend them and reference them from the
docs where needed.

We will also create a fully fledged pypi package instead of using
*requirements.txt*. On top of requirements, it will also allow us to create
define console scripts which we will use to run the devserver.


Project structure::

    ├─ setup.py
    └─ src
       └─ restiblog
          ├─ __init__.py
          ├─ app.py
          ├─ models.py
          └─ routes.py


And here's the *setup.py* we will use for the package.

.. literalinclude:: /examples/02_models/setup.py
    :linenos:

New base resource class - `ModelResource`
=========================================

How RestResource methods map to ModelResource methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

============== ===============
 RestResource   ModelResource
============== ===============
 rest_query     query_items
 rest_get       get_item
 rest_create    create_item
 rest_update    update_item
 rest_delete    delete_item
============== ===============
