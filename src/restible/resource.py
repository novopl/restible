# -*- coding: utf-8 -*-
# Copyright 2017-2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
'''

Working with resources
======================

**restible** resources implementation is divided into two classes:

    - `RestResource`
    - `ModelResource`

The `RestResource` class is a very basic wrapper around a REST resource where
everything has to be implemented manually. This is the most basic usage of
resitble and allows the maximum extensibility. The downside is that it requires
writing quite a lot of repetitive code in order to get it working. Because of
that, **restible** provides another base class that inherits from
`RestResource`: the `ModelResource` class.

Most of the time the REST resource will have some corresponding model class.
`ModelResource` contains code for most common operations that you would do on a
resource backed by model. It does not manipulate any model classes directly so
it's not DB dependant in any way. It only contains the code that would probably
have to be written for any model based resource, no matter what underlying
library you use to persist your models. There are separate libraries that
provide integration with most common frameworks/libraries:

:Django: `restible-django <https://github.com/novopl/restible-django>`_.
:SQLAlchemy: `restible-sqlalchemy <https://github.com/novopl/restible-sqlalchemy>`_.
:AppEngine NDB: `restible-appengine <https://github.com/novopl/restible-appengine>`_.


Simple app example
==================

In this section we will create a simple AppEngine application that uses
**restible** to build the REST API. We've chosen AppEngine as it comes with
everything needed (HTTP and ORM layers) and is easy to deploy without any
devops. The free AppEngine account let's you host 10 of your apps so that also
helps.

.. code-block:: python
    :linenos:

    import restible
    import webapp2
    from google.appengine.ext import ndb
    from restible_appengine.util import ndb_query_from_values

    class BlogPost(ndb.Model):
        title = ndb.StringProperty()
        content = ndb.TextProperty()
        created_at = ndb.DateTimeProperty(auto_now_add=True)


    class BlogPostResource(ndb.ModelResource):
        name = 'post'
        model = BlogPost
        spec = serafin.Fieldspec('*')
        route_params = [{"name": "user_id"}]

        def create_item(self, request, filters):
            """ Get a list of resources. """
            return ndb_query_from_values(models.Resource, filters)


    wsgi_app = webapp2.WSGIApplication(
        routes=[

        ],
        debug=constants.DEBUG,
        config=CONFIG
    )

'''
from __future__ import absolute_import, unicode_literals

# stdlib imports
import inspect
import re
from typing import Text

from .actions import api_action


class RestResource(object):
    """ Represents the operations available on the given resource.

    This class should not handle HTTP directly. Rather than that there should
    be a separate implementation that maps HTTP layer onto resources. This way
    we can swap the HTTP layer without reimplementing the resource. This also
    follows SRP.

    If the given `RestResource` subclass doesn't have one of the REST methods
    implemented, the endpoint should return 405 Method not allowed (or 404?)
    """

    _NAME_RE = re.compile(r'^[a-zA-Z_][\w\d_]*$')
    name = None
    parent = None

    def __init__(self):
        self._validate_name(self.name)

    def rest_actions(self):
        """ Return all actions defined on the current resource.

        :return List[function]:
            List of action handlers. To get the metadata for a given *action*
            just use ``api_action.get_meta(action)``
        """
        ATTR = '_actions'

        if not hasattr(self, ATTR):
            actions = []
            for _, method in inspect.getmembers(self, inspect.ismethod):
                if api_action.is_action(method):
                    actions.append(method)

            setattr(self, ATTR, actions)

        return getattr(self, ATTR)

    def get_pk(self, request):
        """ Read the current resource type PK from the request.

        :param HttpRequest request:
            An HTTP request. Must contain the ``.rest_keys`` dictionary injected
            by `RestEndpoint.dispatch()` method.
        :return:
            Primary key that is associated with this resource type. This is
            extracted from ``.rest_keys`` based on the resource name.
        """
        if hasattr(request, 'rest_keys'):

            if hasattr(self, 'route_params'):
                if len(self.route_params) == 1:
                    return request.rest_keys.get(self.route_params[0]['name'])
                else:
                    params = (
                        request.rest_keys.get(route_param['name'])
                        for route_param in self.route_params
                    )
                    return [x for x in params if x]
            else:
                return request.rest_keys.get('{name}_pk'.format(name=self.name))

    def _validate_name(self, name):
        """ Validate the name is a valid resource name. """
        if name is None or not self._NAME_RE.match(name):
            raise ValueError(
                'REST endpoint name contain only letters, digits and '
                'underscores and cannot start with a digit'
            )

    def implements(self, rest_verb):
        # type: (Text) -> bool
        """ Check whether this resource implements a given REST verb.

        Args:
            rest_verb (str):
                The REST verb you want to check. Possible values are *create*,
                *query*, *get*, *update* and *delete*.

        Returns:
            bool: **True** if the given REST verb is implemented, **False**
                otherwise.
        """
        test = {
            'create': lambda: self.rest_create(None, {}),
            'query': lambda: self.rest_query(None, {}),
            'get': lambda: self.rest_get(None, {}),
            'update': lambda: self.rest_update(None, {}),
            'delete': lambda: self.rest_delete(None),
        }.get(rest_verb)

        if test:
            try:
                test()
                return True
            except NotImplementedError:
                return False
            except:
                return True
        else:
            return False

    def rest_query(self, request, params):
        """ GET list. """
        raise NotImplementedError(".rest_query() not implemented".format(
            self.__class__.__name__
        ))

    def rest_get(self, request, params):
        """ GET detail. """
        raise NotImplementedError("{}.rest_get() not implemented".format(
            self.__class__.__name__
        ))

    def rest_create(self, request, data):
        """ POST list. """
        raise NotImplementedError("{}.rest_create() not implemented".format(
            self.__class__.__name__
        ))

    def rest_update(self, request, data):
        """ PUT detail. """
        raise NotImplementedError("{}.rest_update() not implemented".format(
            self.__class__.__name__
        ))

    def rest_delete(self, request):
        """ DELETE detail. """
        raise NotImplementedError("{}.rest_delete() not implemented".format(
            self.__class__.__name__
        ))

    def rest_options(self, request):
        """ OPTIONS list/detail. """
        raise NotImplementedError("{}.rest_options() not implemented".format(
            self.__class__.__name__
        ))

    def rest_head(self, request):
        """ OPTIONS list/detail. """
        raise NotImplementedError("{}.rest_head() not implemented".format(
            self.__class__.__name__
        ))


# Used only in type hint comments
del Text
