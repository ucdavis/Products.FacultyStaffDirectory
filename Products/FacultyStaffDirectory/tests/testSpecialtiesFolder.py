# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) SpecialtiesFolder
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone

class testSpecialtiesFolder(testPlone):
    """Test-cases for class(es) SpecialtiesFolder."""

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDCommittee'].Title() != "AT Content Type")

    def testSpecialtyCreation(self):
        """Make sure we can add Specialty objects within the SpecialtiesFolder."""
        fsd = self.getPopulatedDirectory()
        self.failUnless('specialties' in fsd.contentIds(), "Failed to create a SpecialtiesFolder in the FacultyStaffDirectory.")
        specialty = fsd['specialties']
        specialty.invokeFactory(type_name="FSDSpecialty", id="test_specialty")
        self.failUnless('test_specialty' in specialty.contentIds(), "Failed to create a Specialty in the SpecialtiesFolder.")

    def testObjectReorder(self):
        """ Make sure we can reorder objects within this folderish content type. """
        fsd = self.getPopulatedDirectory()
        specialty = fsd['specialties']
        specialty.invokeFactory(type_name="FSDSpecialty", id="o1") 
        specialty.invokeFactory(type_name="FSDSpecialty", id="o2") 
        specialty.invokeFactory(type_name="FSDSpecialty", id="o3") 
        specialty.moveObjectsByDelta(['o3'], -100)
        self.failUnless(specialty.getObjectPosition('o3') == 0, "FSDSpecialty Subobject 'o3' should be at position 0.")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSpecialtiesFolder))
    return suite
