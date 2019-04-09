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
    :lines: 1-31,141-145
    :linenos:

And here are the project requirements for this app:

.. literalinclude:: /examples/01_basic/requirements.txt
    :linenos:


``BlogPost`` model
==================

Next we create a simple model to persist our blog posts. Only the bare minimum
here as that's not the point.

.. literalinclude:: /examples/01_basic/main.py
    :lines: 41-55
    :linenos:


Create REST Resource for ``BlogPost``
=====================================

.. literalinclude:: /examples/01_basic/main.py
    :lines: 63-66
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
    :lines: 67,74-75
    :linenos:

Here we define the generic ``GET /api/post`` route. In our case it will return
all blog posts stored by the backend.

In real app, this will probably also support some filtering of the results
and possibly pagination as well.


Get single post
~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 77-83
    :linenos:

This is the detail route to get a blog post by ID (``GET /api/post/<post_id>``).
**restible** provides a handy method for getting the route param
associated with the request: `RestResource.get_pk`. It will take into
account the


Create new blog post
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 85-103
    :linenos:

Next up is the blog post create handler (``POST /api/post``). In this basic
example we only do a very simple validation - are all the required fields
present. You can have a more complex validation logic in real life, but as we'll
learn later in this tutorial series, **restible** has some tools for that as
well. Here we won't be using them to keep things as simple as possible.


Update blog post
~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 105-128
    :linenos:

Here we allow the users to update any existing post (``PUT /api/post/<post_id>``).
The code is pretty self-explanatory, but there are a few things we can point out
here. As you can see we remove few values from the payload to prevent overwriting
them (they are set automatically by the backend and user should not be able to
overwrite those).

Another thing is the use of `restible.util.update_from_values`.
This is a small helper function that will take each item in *values* (second
argument) and set the corresponding attribute on the object passed to it as the
first argument (*post* in this case). The first argument doesn't have to be a
model, any python object will do (as long as you can set each of the properties
passed in *values*).


Delete blog post
~~~~~~~~~~~~~~~~

.. literalinclude:: /examples/01_basic/main.py
    :lines: 130-140
    :linenos:

And last but not least: deleting posts (``DELETE /api/post/<post_id>``). Not
much left to say here, just get the ID of the requested post and delete it from
database.


Setup Flask URLs
================

Now that we have our API resource defined, the last thing to do is setup the
flask URL mappings. For that, we will use an integration library
`restible-flask <https://github.com/novopl/restible-flask>`_ and the
``Endpoint`` class provided by it. You just need to pass the resource base URL
and the associated resource class.

The resource <-> URL mapping is the one thing that will be very differente
depending on what framework/libraries are you using to power restible.
`restible-flask <https://github.com/novopl/restible-flask>`_,
`restible-django <https://github.com/novopl/restible-django>`_ and
`restible-appengine <https://github.com/novopl/restible-appengine>`_ all have a
different way of mapping the URLs, for more information consult the docs for
the library of your choosing.

In general, the resource definitions (not models) should be easy to move when
you change the underlying libraries framewroks, but the mapping of those
resources onto URL fully depends on the underlying library and thus can be very
different.


.. literalinclude:: /examples/01_basic/main.py
    :lines: 21-37
    :emphasize-lines: 6-8
    :linenos:


Next steps
==========


In the :doc:`next section </tutorial/02_models>` we will reimplement the same
app, but this time we will use `ModelResource` instead of `RestResource`.
