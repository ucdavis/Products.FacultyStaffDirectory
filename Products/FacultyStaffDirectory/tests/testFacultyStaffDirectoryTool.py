# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for Faculty/Staff Directory portal tool
#

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone
from Products.FacultyStaffDirectory.membership.person import UserAuthentication
from Products.CMFCore.utils import getToolByName
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL

class testFacultyStaffDirectoryTool(testPlone):
    """Test-cases for FacultyStaffDirectoryTool."""

    def afterSetUp(self):
        from Products.CMFCore.utils import getToolByName
        from Products.FacultyStaffDirectory.config import TOOLNAME
        
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        self.fsd_tool = getToolByName(self.person,TOOLNAME)
        # set up an additional, non-fsd user for testing folder and profile methods
        self.portal.acl_users._doAddUser('user1','secret',['Member'],[])
        self.mt = getToolByName(self.person,'portal_membership')
        
    def testUseInternalPasswordControlsAuth(self):
        from Products.membrane.at.interfaces import IUserAuthentication
        
        u = IUserAuthentication(self.person)
        self.person.setPassword("chewy1")
        if self.fsd_tool.getUseInternalPassword():
            self.failUnless(u.verifyCredentials({'login':'abc123','password':'chewy1'}),"useInternalPassword appears to be broken, failed to verify correct login and password: %s" % self.fsd_tool.getUseInternalPassword())
            self.fsd_tool.setUseInternalPassword(False)
            self.failIf(u.verifyCredentials({'login':'abc123','password':'chewy1'}), "useInternalPassword not toggled.  verification still allowed: %s" % self.fsd_tool.getUseInternalPassword())
        else:
            self.failIf(u.verifyCredentials({'login':'abc123','password':'chewy1'}),"verification allowed, but shouldn't have been: %s" % self.fsd_tool.getUseInternalPassword())
            self.fsd_tool.setUseInternalPassword(True)
            self.failUnless(u.verifyCredentials({'login':'abc123','password':'chewy1'}), "useInternalPassword not toggled.  verification still disallowed: %s" % self.fsd_tool.getUseInternalPassword())
            
    def testAttributeAccessToUseInternalPassword(self):
        try:
            # we expect this to throw an attribute error.  If it doesn't, fail and report
            # this exposes the bug reported here: 
            #     https://weblion.psu.edu/trac/weblion/ticket/1140
            self.fsd_tool.useInternalPassword
            self.fail('Attribute access to fsd_tool.useInternalPassword succeeded unexpectedly')
        except AttributeError:
            self.fsd_tool.getUseInternalPassword()
            self.failUnless(self.fsd_tool.useInternalPassword,
                            'after using the accessor, attribute access to fsd_tool.useInternalPassword should have succeeded, but did not')
            
    def testIdRegexDefault(self):
        """ Check to make sure the idRegex field is defaulting to the value set in portal_registration
        """
        # get the default value
        self.fsd_tool.pre_edit_setup()
        idRegex = self.fsd_tool.getIdRegex()
        # get the value from portal_registration
        pr = getToolByName(self.portal, 'portal_registration')
        regPattern = pr.getIDPattern() or pr.getDefaultIDPattern()
        self.failUnless(idRegex == regPattern)
        
    def testIdRegexChecking(self):
        """ Make sure the id regex validation is working
        """
        self.fsd_tool.setIdRegex('[A-Z]')
        self.fsd_tool.setIdRegexErrorMessage('Not even close.')
        message = self.person.validate_id('123456')
        self.failUnless(message == 'Not even close.')        
        self.failUnless(not self.person.validate_id('ABC'))        
        
    def testRegexValidation(self):
        """ Make sure the value entered is a valid regular expression
        """
        self.failUnless(self.fsd_tool.validate_idRegex(']['))
        self.failUnless(not self.fsd_tool.validate_idRegex('[A-Za-z]'))

    def testToolForm(self):
        """ We're overriding some things in the base form for this configlet. That causes some issues
            between Plone 2.5 and 3. Make sure it works properly for each. Mostly just AttributeErrors
        """
        self.failUnless(not self.fsd_tool.edit())
    
    def testNotInFolderContents(self):
        """ Make sure the tool isn't showing up in the folder contents at the root of the Plone site.
        """
        self.failUnless('facultystaffdirectory_tool' not in [o.id for o in self.portal.getFolderContents()], 'FacultyStaffDirectory_tool is listed in the folder contents of the portal.')

    def testFTISetup(self):
        """ Make sure the FTI is pulling info from the GS types profile """
        self.failUnless(self.portal.portal_types['FSDFacultyStaffDirectoryTool'].Title() != "AT Content Type")
    
    def testGetDirectoryRoot(self):
        """Make sure this returns the containing FSD."""
        self.failUnlessEqual(self.person.getDirectoryRoot(), self.directory)
        
    def testFsdMyFolder(self):
        """fsdMyFolder method should return the appropriate url for non-fsd users or 
        for fsd users
        """
        self.login(self.person.id)
        # logged in as an fsd user, the substring <directory_id/user_id> should be in the  return value for the function
        self.failUnless(self.fsd_tool.fsdMyFolder().find(self.directory.id + '/' + self.person.id), "bad url returned for %s: %s" % (self.person.id, self.fsd_tool.fsdMyFolder()))
        
        self.login('user1')
        # set up a memberarea
        if (not self.mt.getMemberareaCreationFlag()):
            self.mt.setMemberareaCreationFlag()
        self.mt.createMemberArea()
        try:
            self.failUnless(self.fsd_tool.fsdMyFolder().find(self.mt.getMembersFolder().id + '/user1'), "bad url returned for user1: %s" % self.fsd_tool.fsdMyFolder())
        except IndexError:
            self.fail("Index Error indicates that there are no search results from the membrane tool")
            
    def testFsdMemberProfile(self):
        """fsdMemberProfile should return the location of the editor for member profile information.
        This will change depending on whether the member is an fsd person or an acl_users member
        """
        self.login(self.person.id)
        # logged in as an fsd user, the substring <directory_id/user_id/edit> should be in the return value for the function
        self.failUnless(self.fsd_tool.fsdMemberProfile().find(self.directory.id + '/' + self.person.id), "bad url returned for %s: %s" % (self.person.id, self.fsd_tool.fsdMemberProfile()))
        
        # now as an acl_users user
        self.login('user1')
        try:
            self.failUnless(self.fsd_tool.fsdMemberProfile().find('/personalize_form'), "bad url returned for user1: %s" % self.fsd_tool.fsdMyFolder())
        except IndexError:
            self.fail("Index Error indicates that there are no search results from the membrane tool")
            
    def testFsdShowMyFolder(self):
        """fsdShowMyFolder tries to intelligently decide whether to show the 'my folder' action
        button or not.  It tests to see if a member is an fsd person, and acts accordingly
        """
        self.login(self.person.id)
        # logged in as an fsd user, the method should always return true
        self.failUnless(self.fsd_tool.fsdShowMyFolder(), "fsdShowMyFolder returning false for fsd user")
        
        # now as acl_users user
        self.login('user1')
        try:
            if (self.mt.getMemberareaCreationFlag() and (self.mt.getHomeFolder() is not None)):
                self.failUnless(self.fsd_tool.fsdShowMyFolder(), "should be showing my folder for acl_users, but we aren't")
            else:
                self.failIf(self.fsd_tool.fsdShowMyFolder(), "should not be showing my folder for acl_users, but we are")
        except IndexError:
            self.fail("Index Error indicates that there are no search results from the membrane tool")

    def testMembraneTypeDeactivation(self):
        """test that the fsd_tool's at_post_edit_script calls the modifyMembraneTypes event and
        that event correctly deals with membrane activation/deactivation
        """
        # Be sure that FSDPerson is still a membrane provider, or the test will be invalid
        self.failUnless('FSDPerson' in MEMBRANE_ABLE_TYPES, "test invalid, FSDPerson is not listed as membrane-able")

        mbt = getToolByName(self.person, MEMBRANE_TOOL)
        uf = getToolByName(self.person, 'acl_users')
        mtypes = mbt.listMembraneTypes()
        new_types_list = tuple(set(MEMBRANE_ABLE_TYPES) - set(('FSDPerson',)))

        # FSDPerson should be membrane-active at setup
        self.failUnless('FSDPerson' in self.fsd_tool.getEnableMembraneTypes() and 'FSDPerson' in mtypes, "FSDPerson should be in both lists: %s, %s" % (self.fsd_tool.getEnableMembraneTypes(), mtypes))
        self.failUnless(uf.getUserById('abc123'), "Person 'abc123' not registered as user via acl_users")
        
        # now, let's manually alter the list of types, and simulate editing the tool
        self.fsd_tool.setEnableMembraneTypes(new_types_list)
        self.fsd_tool.reindexObject()
        self.fsd_tool.at_post_edit_script()
        
        # FSDPerson should not be membrane-active
        mtypes = mbt.listMembraneTypes()
        self.failIf('FSDPerson' in self.fsd_tool.getEnableMembraneTypes() or 'FSDPerson' in mtypes, "FSDPerson should not be in either list: %s, %s" % (self.fsd_tool.getEnableMembraneTypes(), mtypes))
        self.failIf(uf.getUserById('abc123'), "Person 'abc123' active as a user after membrane de-activation")
        
        # now, put everything back!
        self.fsd_tool.setEnableMembraneTypes(MEMBRANE_ABLE_TYPES)
        self.fsd_tool.reindexObject()
        self.fsd_tool.at_post_edit_script()
        
        # FSDPerson should be membrane-active again
        mtypes = mbt.listMembraneTypes()
        self.failUnless('FSDPerson' in self.fsd_tool.getEnableMembraneTypes() and 'FSDPerson' in mtypes, "FSDPerson should be in both lists: %s, %s" % (self.fsd_tool.getEnableMembraneTypes(), mtypes))
        self.failUnless(uf.getUserById('abc123'), "Person 'abc123' not active as a user after membrane re-activation")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testFacultyStaffDirectoryTool))
    return suite
