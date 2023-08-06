"""
Testing that grokcore annotation work under Zope2:

  >>> from five.grok.tests.annotation import *
  >>> grok.testing.grok('five.grok.tests.annotation')

We can adapt a model to an annotation interface and obtain a
persistent annotation storage:

  >>> manfred = Mammoth('manfred')
  >>> branding = IBranding(manfred)
  >>> branding.addBrand('mine')
  >>> branding.addBrand('yours')

Regetting the adapter will yield the same annotation storage:

  >>> brands = IBranding(manfred).getBrands()
  >>> brands.sort()
  >>> brands
  ['mine', 'yours']

"""

from BTrees.OOBTree import OOTreeSet
from grokcore.annotation.components import Model
from zope import interface

from five import grok


class Mammoth(Model):
    def __init__(self, name):
        self.name = name


class IBranding(interface.Interface):

    def addBrand(brand):
        """Brand an animal with ``brand``, a string."""

    def getBrands():
        """Return a list of brands."""


@interface.implementer(IBranding)
class Branding(grok.Annotation):
    grok.context(Mammoth)

    def __init__(self):
        self._brands = OOTreeSet()

    def addBrand(self, brand):
        self._brands.insert(brand)

    def getBrands(self):
        return list(self._brands)
