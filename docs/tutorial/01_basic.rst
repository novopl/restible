##################
Basic restible App
##################

.. note::
    You can get the full source code for this example
    `here <https://github.com/novopl/restible/tree/master/docs/examples/01_basic>`_.

.. contents:: Table of Contents
    :local:

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


Start with an empty Flask app
=============================

We use the most basic flask structure there is: everything is contained within
one ``main.py`` file. The app is very simple so there's not need to split it
up yet.

.. literalinclude:: /examples/01_basic/main.py
    :lines: 1-31,127-130
    :linenos:

And here are the project requirements for this app:

.. literalinclude:: /examples/01_basic/requirements.txt
    :linenos:



``BlogPost`` model
==================

Next we create a simple model to persist our blog posts. Only the bare minimum
here as that's not the point.

.. literalinclude:: /examples/01_basic/main.py
    :lines: 38-52
    :linenos:


Create REST Resource for ``BlogPost``
=====================================

.. literalinclude:: /examples/01_basic/main.py
    :lines: 60-63
    :linenos:

This is the REST resource associated with the BlogPost model. We're using
`resource.RestResource` which comes with least amount of functionality built-in.
Everything has to be done manually. There are more base resource classes
provided by restible and third party libraries.

Here we just want to kick things of with the simplest one (rarely used in real
apps).


Query blog posts
~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 64,71-72
    :linenos:

Here we define the generic ``GET /api/post`` route. In our case it will return
all blog posts stored by the backend.

In real app, this will probably also support some filtering of the results
and possibly pagination as well.


Get single post
~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 74-80
    :linenos:

This is the detail route to get a blog post by ID (``GET /api/post/<post_id>``).
**restible** provides a handy method for getting the route param
associated with the request: `RestResource.get_pk`. It will take into
account the


Create new blog post
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 82-100
    :linenos:

Next up is the blog post create handler (``POST /api/post``). In this basic
example we only do a very simple validation - are all the required fields
present. You can have a more complex validation logic in real life, but as we'll
learn later in this tutorial series, **restible** has some tools for that as
well. Here we won't be using them to keep things as simple as possible.


Update blog post
~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 102-124
    :linenos:


Delete blog post
~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 126-136
    :linenos:


Setup Flask URLs
================

.. literalinclude:: /examples/01_basic/main.py
    :lines: 27-34
    :emphasize-lines: 6-8
    :linenos:


Putting it all together
=======================

Here's the full source code for the app we just created:

.. literalinclude:: /examples/01_basic/main.py
    :linenos:
