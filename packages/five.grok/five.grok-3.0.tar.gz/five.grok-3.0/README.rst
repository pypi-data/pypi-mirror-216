five.grok
=========

.. contents::

Introduction
------------

`five.grok` is a development layer for Zope, based on Grok framework
concepts.

The development techniques are similar to the ones used with Grok
framework.

It is based on `grokcore` namespace packages that were factored out of Grok
framework.

Implemented features
--------------------

Coming from Grok, the following components are available to Zope
developers:

- Zope 3 Component (Adapter, Global utilities, Subscribers),

- Permissions,

- Views and Viewlets,

- Skins and resources directories,

- Page Templates (using the Zope Page Templates),

- Formlib forms (optional, you need to include the extra ``form``),

- Local sites and local utilities,

- Annotations,

- Layout (optional, you need to include the extra ``layout``).

All those components are available with exactly the same syntax than
in grok. You just have to do::

  from five import grok

Instead of::

  import grok

Installation
------------

After adding the dependency to ``five.grok`` in your project, you have
to load the following ZCML::

  <include package="five.grok" />


More information
----------------

You can refer to the Grok website: http://grok.zope.org/, and the Grok
documentation: http://grok.zope.org/documentation/.

You can check the doctest included in sources as well.
