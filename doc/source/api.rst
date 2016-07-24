.. _api:

API
===

Extension
---------

.. module:: flask_ember

.. autofunction:: get_ember

.. autoclass:: FlaskEmber
   :members:
   :inherited-members:

Resource
--------

.. module:: flask_ember.resource

.. autoclass:: ResourceBase

.. autoclass:: ResourcePropertyBase
   :members:

.. autoclass:: ResourceDescriptor
   :members:

Fields
^^^^^^

.. module:: flask_ember.resource.fields

.. autoclass:: FieldBase
   :show-inheritance:
   :members:
   :inherited-members:

Database
--------

.. module:: flask_ember.database

.. autoclass:: FlaskEmberDatabase
   :show-inheritance:
   :members:
   :inherited-members:

DSL
---

.. module:: flask_ember.dsl

.. autoclass:: ClassMutatorBase
   :members:

Model
-----

.. module:: flask_ember.model

.. autoclass:: PropertyBuilderBase
   :members:

.. autoclass:: FieldBuilder
   :show-inheritance:
   :members:

Utilities
---------

Collections
^^^^^^^^^^^

.. module:: flask_ember.util.collections

.. autofunction:: merge_dicts
