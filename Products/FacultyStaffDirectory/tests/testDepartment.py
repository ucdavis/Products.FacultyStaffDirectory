# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) Committee
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone
from Products.CMFCore.utils import getToolByName

class testDepartment(testPlone):
    """Test-cases for class(es) Department."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.directory.invokeFactory(type_name="FSDDepartment", id="test-department-inside", title="Inside Department") 
        self.portal.invokeFactory(type_name="FSDDepartment", id="test-department-outside", title="Outside Department") 
        self.inDept = self.directory['test-department-inside']
        self.outDept = self.portal['test-department-outside']
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.person2 = self.getPerson(id='def456', firstName="Testy", lastName="Person")

    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDDepartment'].Title() != "AT Content Type")
        self.failUnless(self.portal.portal_types['FSDDepartmentalMembership'].Title() != "AT Content Type")

    def testCreateDepartment(self): 
        # Make sure Departments can be added within FSDs
        self.failUnless('test-department-inside' in self.directory.contentIds())
        # getDirectoryRoot() should return the FSD location

    def testGetDepartmentMetadataField(self):
        self.outDept.setMembers((self.person, self.person2))
        self.failIf(self.person2.getRawDepartments() == [])
        self.failIf(self.person2.getDepartmentNames() == [])

    ## membrane tests
    def testDepartmentIsGroup(self):
        """Verify that a department is acting as a group
        """
        
        # For Departments within FSDs
        self.failUnless(self.portal.portal_groups.getGroupById(self.inDept.id),"unable to find group with id of this department: %s" % self.inDept.id)
        
    def testIGroupAdapter(self):
        """Verify all methods of the IGroup adapter to the Classification content type
        """
        from Products.membrane.interfaces import IGroup
        from Products.CMFCore.utils import getToolByName
        
        wf = getToolByName(self.directory,'portal_workflow')
        
        #adapt to IGroup
        ing = IGroup(self.inDept)
        
        #group title is the content object title
        self.inDept.setTitle('New Title')
        self.failUnless(ing.Title()=='New Title',"IGroup.getTitle is not finding the correct title:\nexpected: %s\nfound: %s" % (self.inDept.Title(),ing.Title()))
        
        # group id is set on content object, uniqueness is enforced elsewhere
        self.failUnless(ing.getGroupId()==self.inDept.getId(),"getGroupId returning incorrect value:\nExpected: %s\nReceived: %s" % (self.inDept.getId(), ing.getGroupId()))
        
        #members are obtained correctly, regardless of how the classification was added
        #added from person object
        self.person.setDepartments((self.inDept,))
        self.person2.setDepartments((self.inDept,))
        members = list(ing.getGroupMembers())
        members.sort()
        self.failUnless(members == ['abc123','def456'],"incorrect member list: %s" % members)
        #clear the list
        self.inDept.setMembers(());
        self.failIf(self.inDept.getMembers(),"there are still people listed in this classification: %s" % self.inDept.getPeople())
        #added from classification object
        self.inDept.setMembers((self.person,self.person2))
        members = list(ing.getGroupMembers())
        members.sort()
        self.failUnless(members == ['abc123','def456'],"incorrect member list: %s" % members)
        #deactivate group and verify emptiness
        wf.doActionFor(self.inDept,'deactivate')
        members = list(ing.getGroupMembers())
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
        self.failUnless(self.inDept.validate_id('foo')==None,"failed to validate_id 'foo': %s" % self.inDept.validate_id('foo'))
        # allow current object id
        self.failUnless(self.inDept.validate_id(self.inDept.getId())==None,"Failed to validate current id of classification object: %s" % self.inDept.id)
        # deny id of other object in site
        self.failUnless('doc1' in self.inDept.validate_id('doc1'),"Allowed id 'doc1', even though there is an object with that id in the portal: %s" % self.inDept.validate_id('doc1'))
        # deny id of other group for site
        self.failUnless('group1' in self.inDept.validate_id('group1'),"Allowed id 'doc1', even though there is a group with that id in the portal: %s" % self.inDept.validate_id('group1'))

    # def testGroupTitle(self):
    #     """ Verify that group titles are being set properly.
    #     """
    #     acl = getToolByName(self.portal, 'acl_users')
    #     ind = acl.getGroupById('test-department-inside')
    #     self.failUnless(ind.getGroupName() == 'Inside Department', "KnownFailure: Unexpected value for Title for group 'faculty'. Got '%s', expected 'Inside Department'." % ind.Title())
        

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testDepartment))
    return suite
