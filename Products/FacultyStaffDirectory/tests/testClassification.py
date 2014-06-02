# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) Classification
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone
from Products.CMFCore.utils import getToolByName

class testClassification(testPlone):
    """Test-cases for class(es) Classification."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.person2 = self.getPerson(id='def456', firstName="Testy", lastName="Person")
        self.classification = self.directory.getClassifications()[0].getObject()

    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDClassification'].Title() != "AT Content Type")

    ## membrane tests
    def testClassificationIsGroup(self):
        """Verify that a classification is acting as a group
        """
        cls = self.classification
        self.failUnless(self.portal.portal_groups.getGroupById(cls.id),"unable to find group with id of this fsd: %s" % cls.id)
        
    def testIGroupAdapter(self):
        """Verify all methods of the IGroup adapter to the Classification content type
        """
        from Products.membrane.interfaces import IGroup
        from Products.CMFCore.utils import getToolByName
        
        wf = getToolByName(self.classification,'portal_workflow')
        
        #adapt to IGroup
        g = IGroup(self.classification)
        
        #group title is the content object title
        self.classification.setTitle('New Title')
        self.failUnless(g.Title()=='New Title',"IGroup.getTitle is not finding the correct title:\nexpected: %s\nfound: %s" % (self.classification.Title(),g.Title()))
        
        # group id is set on content object, uniqueness is enforced elsewhere
        self.failUnless(g.getGroupId()==self.classification.getId(),"getGroupId returning incorrect value:\nExpected: %s\nReceived: %s" % (self.classification.getId(), g.getGroupId()))
        
        #members are obtained correctly, regardless of how the classification was added
        #added from person object
        self.person.setClassifications((self.classification,))
        self.person2.setClassifications((self.classification,))
        members = list(g.getGroupMembers())
        members.sort()
        self.failUnless(members == ['abc123','def456'],"incorrect member list: %s" % members)
        #clear the list
        self.classification.setPeople(());
        self.failIf(self.classification.getPeople(),"there are still people listed in this classification: %s" % self.classification.getPeople())
        #added from classification object
        self.classification.setPeople((self.person,self.person2))
        members = list(g.getGroupMembers())
        members.sort()
        self.failUnless(members == ['abc123','def456'],"incorrect member list: %s" % members)
        #deactivate group and verify emptiness
        wf.doActionFor(self.classification,'deactivate')
        members = list(g.getGroupMembers())
        members.sort()
        self.failUnless(members == [],"deactivated group has non-empty member list: %s" % members)        
        
    def testValidateId(self):
        """Test that the validate_id validator works properly
        """
        from Products.CMFCore.utils import getToolByName
        
        # setup some content to test against
        self.directory.invokeFactory('Document','doc1')
        pg = getToolByName(self.directory,'portal_groups')
        pg.addGroup('group1');
        
        #allow unused id
        self.failUnless(self.classification.validate_id('foo')==None,"failed to validate_id 'foo': %s" % self.classification.validate_id('foo'))
        # allow current object id
        self.failUnless(self.classification.validate_id(self.classification.getId())==None,"Failed to validate current id of classification object: %s" % self.classification.id)
        # deny id of other object in site
        self.failUnless('doc1' in self.classification.validate_id('doc1'),"Allowed id 'doc1', even though there is an object with that id in the portal: %s" % self.classification.validate_id('doc1'))
        # deny id of other group for site
        self.failUnless('group1' in self.classification.validate_id('group1'),"Allowed id 'doc1', even though there is a group with that id in the portal: %s" % self.classification.validate_id('group1'))

    def testInvalidRolesUnavailable(self):
        from Products.FacultyStaffDirectory.config import INVALID_ROLES
        my_roles = self.classification.getRoleSet()
        
        intersection = set(INVALID_ROLES).intersection(set(my_roles))
        
        self.failIf(intersection, "some invalid roles are available to classification: %s" % intersection)

    # def testGroupTitle(self):
    #     """ Verify that group titles are being set properly.
    #     """
    #     acl = getToolByName(self.portal, 'acl_users')
    #     fac = acl.getGroupById('faculty')
    #     self.failUnless(fac.getGroupName() == 'Faculty', "KnownFailure: Unexpected value for Title for group 'faculty'. Got '%s', expected 'Faculty'." % fac.Title())
        
    ## end membrane tests
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testClassification))
    return suite
