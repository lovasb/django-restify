Serializers
===========

Data serialization is two phase method in Restify framework. Firstly - flatten method - brings
complex data to native python types. After that simple data will be converted to serialized string (json, xml, etc).


Built in serializers
--------------------

BaseSerializer
^^^^^^^^^^^^^^
Flatten complex structure with fields parameter:

.. doctest::

   >>> import pprint
   >>> from restify.serializers import BaseSerializer
   >>> class Structure(object):
   ...     a = 7
   ...     c = [1,2,3]
   >>> serializer = BaseSerializer(fields=['a', 'c'])
   >>> simple = serializer.flatten({'data': Structure()})
   >>> pprint.pprint(simple)
   {'data': {'a': 7, 'c': [1, 2, 3]}}


Flatten complex structure with built in object method:

.. doctest::

   >>> import pprint
   >>> from restify.serializers import BaseSerializer
   >>> class Structure(object):
   ...     a = 7
   ...     c = [1,2,3]
   ...
   ...     def flatten(self):
   ...         return {'a': self.a, 'c': self.c}
   >>> serializer = BaseSerializer()
   >>> simple = serializer.flatten({'data': Structure()})
   >>> pprint.pprint(simple)
   {'data': {'a': 7, 'c': [1, 2, 3]}}


ModelSerializer
^^^^^^^^^^^^^^^
Serializing django model objects and querysets.

.. doctest::

    >>> from pprint import pprint
    >>> from tests.models import Person
    >>> from restify.serializers import ModelSerializer
    >>> Person.objects.create_test_data()
    >>> field_names = ['first_name', 'last_name', 'age', ('instrument', ('id', 'name'))] #id field is automatically added
    >>> serializer = ModelSerializer(fields=field_names)
    >>> simple = serializer.flatten(Person.objects.first())
    >>> pprint(simple)
    {'age': 30,
     'first_name': 'Fred',
     'id': 1,
     'instrument': {'id': 1, 'name': 'guitar'},
     'last_name': 'Flintstone'}


.. doctest::

    >>> from pprint import pprint
    >>> from tests.models import Person
    >>> from restify.serializers import ModelSerializer
    >>> Person.objects.create_test_data()
    >>> field_names = ['first_name', 'last_name', 'age']
    >>> serializer = ModelSerializer(fields=field_names)
    >>> simple = serializer.flatten(Person.objects.all()[:2])
    >>> pprint(simple)
    [{'age': 30, 'first_name': 'Fred', 'id': 1, 'last_name': 'Flintstone'},
     {'age': 28, 'first_name': 'Wilma', 'id': 2, 'last_name': 'Flintstone'}]



Implementing Your Own Serializer
--------------------------------
If the built in serializers doesn't matches your needs, it's enough to override the flatten method.