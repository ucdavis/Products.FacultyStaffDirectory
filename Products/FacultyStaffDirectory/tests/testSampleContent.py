# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for product install/uninstall/reinstall
#

from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone


class SampleContentTestCase(testPlone):

    def afterSetUp(self):
        self.portal_setup = getToolByName(self.portal, 'portal_setup')


    def testRun(self):
        self.loginAsPortalOwner()
        self.portal_setup.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:sample-content')
        self.logout()

    def testRunTwice(self):
        self.loginAsPortalOwner()
        self.portal_setup.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:sample-content')
        self.portal_setup.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:sample-content')
        self.logout()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(SampleContentTestCase))
    return suite
