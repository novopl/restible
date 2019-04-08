##################
Basic restible App
##################

This is a very basic example of how to expose a model over HTTP as REST API.
The example below is geared toward using the least amount of code to achieve
it's goals.

For this example we're using *restible* with *Flask* and *SQLAlchemy* since
it's easy to set up, allows for self-contained easy to follow code and simple
code. You can also use other underlying frameworks through other integrations
like **restible-django** or **restible-appengine**.

We will build a very simple blogging app. In this example it will have just
one resource, the ``BlogPost`` that will be exposed over HTTP on
``/api/post`` URL.

.. note::
    You can get the full source code for this example
    `here <github.com/novopl/restible/docs/examples/01_basic>`_

.. contents:: Table of Contents
    :local:


1. Start with an empty Flask app
================================

We use the most basic flask structure there is: everything is contained within
one ``main.py`` file. The app is very simple so there's not need to split it
up yet.

.. literalinclude:: /examples/01_basic/main.py
    :lines: 1-31,127-130
    :linenos:



2. ``BlogPost`` model
=====================

Next we create a simple model to persist our blog posts. Only the bare minimum
here as that's not the point.

.. literalinclude:: /examples/01_basic/main.py
    :lines: 38-52
    :linenos:


3. Create REST Resource for ``BlogPost``
========================================

.. literalinclude:: /examples/01_basic/main.py
    :lines: 60-63
    :linenos:

This is the REST resource associated with the BlogPost model. We're using
`resource.RestResource` which comes with least amount of functionality built-in.
Everything has to be done manually. There are more base resource classes
provided by restible and third party libraries.

Here we just want to kick things of with the simplest one (rarely used in real
apps).


3.1 Query blog posts
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 64,71-72
    :linenos:

Here we define the generic ``GET /api/post`` route. In our case it will return
all blog posts stored by the backend.

In real app, this will probably also support some filtering of the results
and possibly pagination as well.


3.2 Get single post
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 74-80
    :linenos:

This is the detail route to get a blog post by ID (``/api/post/<post_id>``).
**restible** provides a handy method for getting the route param
associated with the request: `RestResource.get_pk`. It will take into
account the


3.3 Create new blog post
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 82-93
    :linenos:


3.4 Update blog post
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 95-115
    :linenos:


3.5 Delete blog post
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 117-127
    :linenos:


4. Setup Flask URLs
===================

.. literalinclude:: /examples/01_basic/main.py
    :lines: 27-34
    :emphasize-lines: 6-8
    :linenos:


Putting it all together
=======================

.. literalinclude:: /examples/01_basic/main.py
    :linenos:
