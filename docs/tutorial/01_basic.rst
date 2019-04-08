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

.. contents:: Table of Contents
    :local:


1. Start with an empty Flask app
================================

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 1-31,127-130
    :linenos:


2. ``BlogPost`` model
=====================

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 38-52
    :linenos:


3. Create REST Resource for ``BlogPost``
========================================

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 60-62
    :linenos:

This is the REST resource associated with the BlogPost model. We're using
`restible.RestResource` which comes with least amount of functionality built-in.
Everything has to be done manually. There are more base resource classes
provided by restible and third party libraries.

Here we just want to kick things of with the simplest one (rarely used in real
apps).


3.1 Query blog posts
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 63,70
    :linenos:

This route will allow to get the list of all existing blog posts. In
real app, this will probably also support some filtering of the results
and possibly pagination as well.


3.2 Get single post
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 72-78
    :linenos:


3.3 Create new blog post
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 80-91
    :linenos:


3.4 Update blog post
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 93-113
    :linenos:


3.5 Delete blog post
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 115-125
    :linenos:


4. Setup Flask URLs
===================

.. literalinclude:: /../examples/01_basic/main.py
    :lines: 27-34
    :emphasize-lines: 6-8
    :linenos:


Putting it all together
=======================

.. literalinclude:: /../examples/01_basic/main.py
    :linenos:
