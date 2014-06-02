# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

import os
import os.path
import sys

import Products
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase

from Products.FacultyStaffDirectory.tests.testPlone import testPlone, PRODUCTS
from Products.FacultyStaffDirectory.extenderInstallation import localAdaptersAreSupported


_extenderName = 'MobilePhoneExtender'

# Install the example extender, even if it's not in the Products folder.
# This has to be out in module space because ZopeLite.py says PloneTestCase.installProduct has to be called from module level.
if not PloneTestCase.hasProduct(_extenderName):
    def _pretendExtenderIsInProductsFolder():
        """Let it be as if MobilePhoneExtender is in the Products folder, even if it isn't."""
        
        _productsNamespacePackage = os.path.join(*([os.sep] + __file__.split(os.sep)[:-2] + ['examples', 'Products.MobilePhoneExtender', 'Products']))  # yeeeeehaw!
        Products.__path__.append(_productsNamespacePackage)  # Stick the "Products" dir within the egg onto the end of the folders Zope searches for products so it can find MobilePhoneExtender.
    
    _pretendExtenderIsInProductsFolder()

PloneTestCase.installProduct(_extenderName)
PloneTestCase.setupPloneSite(id='anotherPortal', products=PRODUCTS)  # a site into which the extender is *not* installed, just to make sure installation doesn't accidentally leak across Plone sites

def _personIsExtended(person):
    return person.Schema().get('mobilePhone') is not None


class TestExtensibilityBase(testPlone):
    def afterSetUp(self):
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.installer.installProducts([_extenderName])
        self.loginAsPortalOwner()  # so getPerson() can make people and stuff


class TestExtensibility(TestExtensibilityBase):
    """Integration tests to make sure the schema extensibility infrastructure works"""
        
    def testSchemaExtension(self):
        """Make sure basic modification of the schema works but doesn't spread to other Plone sites than the one the extender is installed in."""
        # Make sure extension works:
        person = self.getPerson()
        self.failUnless(_personIsExtended(person), "%s failed to append a Mobile Phone field to the Person." % _extenderName)
    
    if localAdaptersAreSupported:  # If they aren't, this isn't even supposed to work.
        def testScopedInstallation(self):
            """Make sure installing the extender didn't install it on the other Plone site by accident; make sure the local adapters really are local."""
            person = self.getPerson(portal=self.app.anotherPortal)
            self.failIf(_personIsExtended(person), "Installing %s on one Plone site caused it to leak over to another accidentally." % _extenderName)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    #suite.addTest(makeSuite(TestExtensibility))  # These tests are invalid (they don't test what they're supposed to). FIXME. (See https://weblion.psu.edu/trac/weblion/ticket/418.)
    if localAdaptersAreSupported:
        class TestUninstallation(TestExtensibilityBase):
            """Tests to ensure uninstalling the product reverts its schema changes"""
                
            def afterSetUp(self):
                TestExtensibilityBase.afterSetUp(self)
                self.installer.uninstallProducts([_extenderName])
            
            def testUninstallation(self):
                """Make sure the schema changes go away when the extender product is removed."""
                person = self.getPerson()
                self.failIf(_personIsExtended(person), "The Person is still extended, even though the extender has been uninstalled.")
        suite.addTest(makeSuite(TestUninstallation))
    return suite
