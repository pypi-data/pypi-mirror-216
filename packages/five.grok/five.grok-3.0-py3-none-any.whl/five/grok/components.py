#############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os.path
import sys

import grokcore.view
import martian
from AccessControl import getSecurityManager
from Acquisition import aq_get
from grokcore.component import implementer
from grokcore.component.interfaces import IContext
from grokcore.site.components import BaseSite
from grokcore.view.components import PageTemplate
from grokcore.viewlet.components import ViewletManager as BaseViewletManager
from OFS.Folder import Folder
from OFS.SimpleItem import SimpleItem
from Products.Five.browser import resource
from Products.Five.browser.pagetemplatefile import ViewMapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser.pagetemplatefile import getEngine
from Products.Five.viewlet.manager import \
    ViewletManagerBase as ZopeTwoBaseViewletManager
from Products.PageTemplates.Expressions import SecureModuleImporter
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component.interfaces import IPossibleSite
from zope.pagetemplate.pagetemplate import PageTemplate as ZopePageTemplate

from five.grok.interfaces import HAVE_FORMLIB


@implementer(IAttributeAnnotatable, IContext)
class Model(SimpleItem):

    def __init__(self, id):
        self._id = id

    def getId(self):
        return self._id


@implementer(IAttributeAnnotatable, IContext)
class Container(Folder):
    pass


@implementer(IPossibleSite)
class Site(Model, BaseSite):
    pass


@implementer(IAttributeAnnotatable, IContext)
class LocalUtility(SimpleItem):
    pass


class View(grokcore.view.View):
    martian.baseclass()

    def __init__(self, context, request):
        super().__init__(context, request)
        if self.static is not None:
            # Set parent so that we have an acquisition chain
            self.static.__parent__ = context

    def redirect(self, url, status=302, trusted=False):
        """ We don't need trusted in Zope2 """
        self.request.response.redirect(url, status=status)


class ViewAwareZopePageTemplate(ZopePageTemplate):

    def pt_getEngine(self):
        return getEngine()

    def pt_getContext(self, instance, request=None, **kw):
        namespace = super().pt_getContext(**kw)
        namespace['request'] = request
        namespace['view'] = instance
        namespace['context'] = context = instance.context
        namespace['views'] = ViewMapper(context, request)

        # get the root
        obj = context
        root = None
        meth = aq_get(obj, 'getPhysicalRoot', None)
        if meth is not None:
            root = meth()

        namespace.update(here=obj,
                         # philiKON thinks container should be the view,
                         # but BBB is more important than aesthetics.
                         container=obj,
                         root=root,
                         modules=SecureModuleImporter,
                         traverse_subpath=[],  # BBB, never really worked
                         user=getSecurityManager().getUser())
        return namespace


class ZopeTwoPageTemplate(PageTemplate):

    def setFromString(self, string):
        zpt = ViewAwareZopePageTemplate()
        if martian.util.not_unicode_or_ascii(string):
            raise ValueError("Invalid page template. Page templates must be "
                             "unicode or ASCII.")
        zpt.write(string)
        self._template = zpt

    def setFromFilename(self, filename, _prefix=None):
        self._template = ViewPageTemplateFile(filename, _prefix)

    def render(self, view):
        template = self._template
        namespace = template.pt_getContext(view, view.request)
        namespace.update(self.getNamespace(view))
        return template.pt_render(namespace)


class ZopeTwoPageTemplateFile(ZopeTwoPageTemplate):

    def __init__(self, filename, _prefix=None):
        self.__grok_module__ = martian.util.caller_module()
        if _prefix is None:
            module = sys.modules[self.__grok_module__]
            _prefix = os.path.dirname(module.__file__)
        self.setFromFilename(filename, _prefix)


class ZopeTwoDirectoryResource(resource.DirectoryResource):
    # We subclass this, because we want to override the default factories for
    # the resources so that .pt and .html do not get created as page
    # templates

    # Allow traversal to contained resources from protected code
    __allow_access_to_unprotected_subobjects__ = True

    # Allow subdirectories to work with restrictedTraverse() (in Zope >=
    # 2.12.6)
    __roles__ = None

    resource_factories = {}
    for type, factory in (
            resource.DirectoryResource.resource_factories.items()):
        if factory is resource.PageTemplateResourceFactory:
            continue
        resource_factories[type] = factory


class ZopeTwoDirectoryResourceFactory(resource.DirectoryResourceFactory):
    # __name__ is needed if you want to get url's of resources

    def __init__(self, name, path, resource_factory=None):
        self.__name = name
        self.__rsrc = self.factory(path, name)

    def __call__(self, request):
        resource = ZopeTwoDirectoryResource(self.__rsrc, request)
        resource.__name__ = self.__name  # We need to add name
        return resource


# Viewlet / Viewlet Manager


class ViewletManager(BaseViewletManager, ZopeTwoBaseViewletManager):

    martian.baseclass()

    def filter(self, viewlets):
        # XXX Need Zope 2 filter
        return ZopeTwoBaseViewletManager.filter(self, viewlets)

    def __getitem__(self, key):
        # XXX Need Zope 4 __getitem__
        return ZopeTwoBaseViewletManager.__getitem__(self, key)


if HAVE_FORMLIB:
    from five.formlib import formbase
    from grokcore.formlib.components import GrokForm as BaseGrokForm
    from grokcore.formlib.components import default_display_template
    from grokcore.formlib.components import default_form_template

    # forms from formlib

    class GrokForm(BaseGrokForm):

        def __init__(self, *args):
            super().__init__(*args)
            self.__name__ = self.__view_name__

    class Form(GrokForm, formbase.PageForm, View):
        martian.baseclass()
        template = default_form_template

    class AddForm(GrokForm, formbase.AddForm, View):
        martian.baseclass()
        template = default_form_template

    class EditForm(GrokForm, formbase.EditForm, View):
        martian.baseclass()
        template = default_form_template

        # grokcore.formlib defines empty actions since 1.1. Restore save
        # option here.
        actions = formbase.EditForm.actions

    class DisplayForm(GrokForm, formbase.DisplayForm, View):
        martian.baseclass()
        template = default_display_template
