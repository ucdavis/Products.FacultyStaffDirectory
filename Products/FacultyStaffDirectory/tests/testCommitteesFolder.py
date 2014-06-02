# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) CommitteesFolder
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone

class testCommitteesFolder(testPlone):
    """Test-cases for class(es) CommitteesFolder."""

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDCommitteesFolder'].Title() != "AT Content Type")

    def testCommitteeCreation(self):
        """Make sure we can add CommitteesFolders in FacultyStaffDirectories and Committees in CommitteesFolders.
        
        Implicitly makes sure CommitteesFolders can be added within a FacultyStaffDirectory."""
        fsd = self.getPopulatedDirectory()
        self.failUnless('committees' in fsd.contentIds(), "Failed to create a CommitteesFolder in the FacultyStaffDirectory.")
        comm = fsd['committees']
        comm.invokeFactory(type_name="FSDCommittee", id="test_committee")
        self.failUnless('test_committee' in comm.contentIds(), "Failed to create a Committee in the CommitteesFolder.")

    def testObjectReorder(self):
        """ Make sure we can reorder objects within this folderish content type. """
        fsd = self.getPopulatedDirectory()
        comm = fsd['committees']
        comm.invokeFactory(type_name="FSDCommittee", id="o1") 
        comm.invokeFactory(type_name="FSDCommittee", id="o2") 
        comm.invokeFactory(type_name="FSDCommittee", id="o3") 
        comm.moveObjectsByDelta(['o3'], -100)
        self.failUnless(comm.getObjectPosition('o3') == 0, "FSDCommittee Subobject 'o3' should be at position 0.")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCommitteesFolder))
    return suite
