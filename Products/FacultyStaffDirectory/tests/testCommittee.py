# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for class(es) Committee
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone

class testCommittee(testPlone):
    """Test-cases for class(es) Committee."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.person2 = self.getPerson(id='def456', firstName="Testy", lastName="Person")
        cid = self.directory['committees'].invokeFactory('FSDCommittee',id='mycommittee',title="My Committee")
        self.committee = self.directory['committees'].mycommittee
        
    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDCommittee'].Title() != "AT Content Type")
        self.failUnless(self.portal.portal_types['FSDCommitteeMembership'].Title() != "AT Content Type")

    def testObjectReorder(self):
        """ Make sure we can reorder objects within this folderish content type. """
        self.committee.invokeFactory(type_name="Document", id="o1") 
        self.committee.invokeFactory(type_name="Document", id="o2") 
        self.committee.invokeFactory(type_name="Document", id="o3") 
        self.committee.moveObjectsByDelta(['o3'], -100)
        self.failUnless(self.committee.getObjectPosition('o3') == 0, "Document subobject 'o3' should be at position 0.")

        
    ## test membrane stuff
    def testCommitteeIsGroup(self):
        """Verify that a classification is acting as a group
        """
        self.failUnless(self.portal.portal_groups.getGroupById(self.committee.getId()),"unable to find group with id of this committee: %s" % self.committee.getId())
        
    def testIGroupAdapter(self):
        """Verify all methods of the IGroup adapter to the Classification content type
        """
        from Products.membrane.interfaces import IGroup
        from Products.CMFCore.utils import getToolByName
        
        wf = getToolByName(self.committee,'portal_workflow')
        
        #adapt to IGroup
        g = IGroup(self.committee)
        
        #group title is the content object title
        self.committee.setTitle('New Title')
        self.failUnless(g.Title()=='New Title',"IGroup.getTitle is not finding the correct title:\nexpected: %s\nfound: %s" % (self.committee.Title(),g.Title()))

        # group id is set on content object, uniqueness is enforced elsewhere
        self.failUnless(g.getGroupId()==self.committee.getId(),"getGroupId returning incorrect value:\nExpected: %s\nReceived: %s" % (self.committee.getId(), g.getGroupId()))
        
        #members are obtained correctly, regardless of how the classification was added
        #added from person object
        self.person.setCommittees((self.committee,))
        self.person2.setCommittees((self.committee,))
        members = list(g.getGroupMembers())
        members.sort()
        self.failUnless(members == ['abc123','def456'],
                        "incorrect member list: %s" % members)
        #clear the list
        self.committee.setMembers(());
        self.failIf(self.committee.getMembers(),
                    "there are still people listed in this committee: %s" % self.committee.getMembers())
        #added from classification object
        self.committee.setMembers((self.person,self.person2))
        members = list(g.getGroupMembers())
        members.sort()
        self.failUnless(members == ['abc123','def456'],
                        "incorrect member list: %s" % members)
        #deactivate group and verify emptiness
        wf.doActionFor(self.committee,'deactivate')
        members = list(g.getGroupMembers())
        members.sort()
        self.failUnless(members == [],"deactivated group has non-empty member list: %s" % members)
        
    def testValidateId(self):
        """Test that the validate_id validator works properly
        """
        from Products.CMFCore.utils import getToolByName
        
        # setup some content to test against
        self.directory['committees'].invokeFactory('FSDCommittee','com1')
        pg = getToolByName(self.directory,'portal_groups')
        pg.addGroup('group1');
        
        #allow unused id
        self.failUnless(self.committee.validate_id('foo')==None,
                        "failed to validate_id 'foo': %s" % self.committee.validate_id('foo'))
        # allow current object id
        self.failUnless(self.committee.validate_id(self.committee.getId())==None,
                        "Failed to validate current id of committee object: %s" % self.committee.getId())
        # deny id of other object in site
        self.failUnless('com1' in self.committee.validate_id('com1'),
                        "Allowed id 'com1', even though there is an object with that id in the committees folder: %s" % self.committee.validate_id('com1'))
        # deny id of other group for site
        self.failUnless('group1' in self.committee.validate_id('group1'),
                        "Allowed id 'group1', even though there is a group with that id in the portal: %s" % self.committee.validate_id('group1'))
        
    ## end test membrane stuff
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCommittee))
    return suite
