"""
  >>> from five.grok.ftests.form.autofields import *
  >>> id = getRootFolder()._setObject("manfred", Mammoth(id='manfred'))

  >>> from Testing.testbrowser import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

  We can test the display form as default view:

  >>> browser.open("http://localhost/manfred/index")
  >>> print(browser.contents)
  <html>...
  ... Name ...
  ... Age ...
  </html>

  But we have an edition form:

  >>> browser.open("http://localhost/manfred/edit")
  >>> browser.getControl('Name').value = 'Arthur'
  >>> browser.getControl('Age').value = '325'
  >>> browser.getControl('Apply').click()
  >>> 'Updated' in browser.contents
  True

  And if we look back to the display form, we will see new values:

  >>> browser.open("http://localhost/manfred/index")
  >>> print(browser.contents)
  <html>...
  ... Name ...
  ... Arthur ...
  ... Age ...
  ... 325 ...
  </html>

"""

from zope import interface
from zope import schema
from zope.schema.fieldproperty import FieldProperty

from five import grok


class IMammoth(interface.Interface):

    name = schema.TextLine(title="Name")
    age = schema.Int(title="Age")


@grok.implementer(IMammoth)
class Mammoth(grok.Model):

    name = FieldProperty(IMammoth['name'])
    age = FieldProperty(IMammoth['age'])


class Edit(grok.EditForm):
    grok.context(Mammoth)


class Index(grok.DisplayForm):
    grok.context(Mammoth)
