##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
import doctest
import re
import unittest

from pkg_resources import resource_listdir

from Testing.ZopeTestCase import FunctionalDocTestSuite
from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase.zopedoctest.functional import getRootFolder
from Testing.ZopeTestCase.zopedoctest.functional import sync
from zope.testing import renormalizing

from five.grok.testing import FunctionalLayer


installProduct('PageTemplates')

checker = renormalizing.RENormalizing([
    (re.compile(r'urllib.error.HTTPError:', re.M), 'HTTPError:'), ])


def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        if filename[0] in ('.', '#'):
            # Some editor create temporary files which can be
            # annoying.
            continue

        dottedname = 'five.grok.ftests.{}.{}'.format(name, filename[:-3])
        test = FunctionalDocTestSuite(
            dottedname,
            checker=checker,
            extraglobs=dict(getRootFolder=getRootFolder,
                            sync=sync),
            optionflags=(doctest.ELLIPSIS +
                         doctest.NORMALIZE_WHITESPACE +
                         doctest.REPORT_NDIFF))
        test.layer = FunctionalLayer

        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['directoryresource', 'view', 'viewlet', 'form', 'site']:
        suite.addTest(suiteFromPackage(name))
    return suite
