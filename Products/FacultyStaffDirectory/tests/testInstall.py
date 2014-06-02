# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Test-cases for product install/uninstall/reinstall
#

from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone

originalMyFolderActionId = "mystuff"
newMyFolderActionId = "fsdmystuff"
originalProfileActionId = "MemberPrefs"
newProfileActionId = "fsdMemberPrefs"
linkableKupuTypes = ['FSDPerson', 'FSDCourse', 'FSDClassification', 'FSDDepartment', 'FSDCommittee', 'FSDCommitteesFolder', 'FSDSpecialty', 'FSDSpecialtiesFolder']
mediaKupuTypes = ['FSDPerson']
collectionKupuTypes = ['FSDFacultyStaffDirectory']

def checkKupuResourceList(tool, resourceType, portalTypeList):
    missingList = []
    resourceList = list(tool.getPortalTypesForResourceType(resourceType))
    for type in portalTypeList:
        if type not in resourceList:
            missingList.append(type)
    return missingList

class testInstall(testPlone):
    def afterSetUp(self):
        migrationTool = getToolByName(self.portal, 'portal_migration')
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.isPlone3OrBetter = migrationTool.getInstanceVersion() >= '3.0'
        self.pc = getToolByName(self.portal, 'portal_catalog')
        self.atct_tool = getToolByName(self.portal, 'portal_atct')
        self.has_kupu = False
        if installer.isProductInstalled('kupu'):
            self.has_kupu = True
            self.ktool = getToolByName(self.portal, 'kupu_library_tool')
        
    def testMemberProfileSetup(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        actions = cp.listActions()
        hasfsdmemberprofile = False
        for action in actions:
            if action.id == originalProfileActionId:
                self.failIf(action.visible, "Original MemberPrefs action is still visible.")
            if action.id == newProfileActionId:
                hasfsdmemberprofile = True
        self.failUnless(hasfsdmemberprofile, "New MemberPrefs action failed to install.")

    def testCatalogIndexesAdded(self):
        missingindexes = []
        for indexName in ['getSortableName', 'getRawClassifications', 'getRawSpecialties', 'getRawCommittees', 'getRawDepartments', 'getRawPeople']:
            if indexName not in self.pc.indexes():
                missingindexes.append(indexName)
        self.failIf(missingindexes, 'Catalog is missing the following indexes: %s' % missingindexes)
        
    def testCatalogMetadataAdded(self):
        missingmetadata = []
        for fieldName in ["getCommitteeNames", "getDepartmentNames", "getSpecialtyNames", "getClassificationNames", "getResearchTopics"]:
            if fieldName not in self.pc.schema():
                missingmetadata.append(fieldName)
        self.failIf(missingmetadata, 'Catalog is missing the following metadata fields: %s' % missingmetadata)
        
    def testTopicIndexesAdded(self):
        missingindexes = []
        for index in ["getRawClassifications","getRawSpecialties","getRawCommittees","getRawPeople","getRawDepartments","getSortableName"]:
            idx = self.atct_tool.getIndex(index)
            if not idx or not idx.enabled:
                missingindexes.append(index)
        self.failIf(missingindexes, 'ATCT Tool is missing the following indexes: %s' % missingindexes)
        
    def testTopicMetadataAdded(self):
        missingmetadata = []
        for fieldName in ["getCommitteeNames","getDepartmentNames","getSpecialtyNames","getClassificationNames","getResearchTopics"]:
            md = self.atct_tool.getMetadata(fieldName)
            if not md or not md.enabled:
                missingmetadata.append(fieldName)
        self.failIf(missingmetadata, 'ATCT Tool is missing the following metadata fields: %s' % missingmetadata)
        
    def testNavTreeSetup(self):
        missingmetatypes = []
        for mType in ['FSDCourse', 'FSDPerson', 'FSDFacultyStaffDirectoryTool']: 
            if not mType in list(self.portal.portal_properties.navtree_properties.metaTypesNotToList):
                missingmetatypes.append(mType)
        self.failIf(missingmetatypes, "The following FSD Types are still visible in the navtree and shouldn't be %s" % missingmetatypes)
        
    def testConfigletAdded(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        self.failIf("FacultyStaffDirectory" not in [ c.id for c in cp._actions ], 'FacultyStaffDirectory configlet has not been registered with the portal controlpanel')
        
    def testVersioningSetup(self):
        missingversionable = []
        pr = getToolByName(self.portal, "portal_repository")
        versionedTypes = ['FSDPerson', 'FSDCommittee', 'FSDSpecialty']
        for t in versionedTypes:
            if t not in pr.getVersionableContentTypes():
                missingversionable.append(t)
        self.failIf(missingversionable, "%s are not listed as versionable and they should be" % missingversionable)
        
        pMap = pr.getPolicyMap()
        for t in versionedTypes:
            self.failUnless(t in pMap)
            self.failUnless(pMap[t], [u'at_edit_autoversion', u'version_on_revert'])
            
    def testKupuLinkableTypesSetup(self):
        if self.has_kupu:
            missingltypes = checkKupuResourceList(self.ktool, 'linkable', linkableKupuTypes)
            self.failIf(missingltypes, '%s not listed as linkable by Kupu' % missingltypes)

    def testKupuMediaTypesSetup(self):
        if self.has_kupu:
            missingmtypes = checkKupuResourceList(self.ktool, 'mediaobject', mediaKupuTypes)
            self.failIf(missingmtypes, '%s not listed as media by Kupu' % missingmtypes)

    def testKupuCollectionTypesSetup(self):        
        if self.has_kupu:
            missingctypes = checkKupuResourceList(self.ktool, 'collection', collectionKupuTypes)
            self.failIf(missingctypes, '%s not listed as collection by Kupu' % missingctypes)

        
class testUninstall(testPlone):
    def afterSetUp(self):
        migrationTool = getToolByName(self.portal, 'portal_migration')
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.isPlone3OrBetter = migrationTool.getInstanceVersion() >= '3.0'
        self.pc = getToolByName(self.portal, 'portal_catalog')
        self.atct_tool = getToolByName(self.portal, 'portal_atct')
        self.has_kupu = False
        if installer.isProductInstalled('kupu'):
            self.has_kupu = True
            self.ktool = getToolByName(self.portal, 'kupu_library_tool')
        self.loginAsPortalOwner()
        installer.uninstallProducts(products=['FacultyStaffDirectory'])
        
    def testMemberProfileTeardown(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        actions = cp.listActions()
        hasfsdmemberprofile = False
        for action in actions:
            if action.id == originalProfileActionId:
                self.failUnless(action.visible, "original MemberPrefs action is not visible")
            if action.id == newMyFolderActionId:
                hasfsdmemberprofile = True
        self.failIf(hasfsdmemberprofile, "new MemberPrefs action failed to uninstall")

    def testMembraneUninstall(self):
        """Test issue #397, where logging in after uninstalling results in an AttributeError."""
        username = 'joe'
        try:
            # Make a user:
            self.portal.acl_users._doAddUser(username, 'passw0rd', ['Member'], [])
            # Log in:
            self.login(name=username)  # Oddly enough, during testing, it fails as soon as you make a user, so this is unnecessary. *shrug*
        except AttributeError:
            self.fail(msg="Had the membrane crash described at https://weblion.psu.edu/trac/weblion/ticket/397.")

    def testNavTreeTeardown(self):
        presentmetatypes = []
        for mType in ['FSDCourse', 'FSDPerson', 'FSDFacultyStaffDirectoryTool']: 
            if mType in list(self.portal.portal_properties.navtree_properties.metaTypesNotToList):
                presentmetatypes.append(mType)
        self.failIf(presentmetatypes, "The following FSD Types are still listed in the navtree metatypesNotToList and they shouldn't be" % presentmetatypes)
        
    def testActionIconsTeardown(self):
        ai = getToolByName(self.portal, 'portal_actionicons')
        try:
            ai.getActionInfo('plone','vcard')
            self.fail('FSD vcard action icon still present in portal_actionicons')
        except KeyError:
            pass

    def testCatalogIndexesTeardown(self):
        presentindexes = []
        for indexName in ['getSortableName', 'getRawClassifications', 'getRawSpecialties', 'getRawCommittees', 'getRawDepartments', 'getRawPeople']:
            if indexName in self.pc.indexes():
                presentindexes.append(indexName)
        self.failIf(presentindexes, 'Catalog still holds the following indexes: %s' % presentindexes)
        
    def testCatalogMetadataTeardown(self):
        presentmetadata = []
        for fieldName in ["getCommitteeNames", "getDepartmentNames", "getSpecialtyNames", "getClassificationNames", "getResearchTopics"]:
            if fieldName in self.pc.schema():
                presentmetadata.append(fieldName)
        self.failIf(presentmetadata, 'Catalog still holds the following metadata fields: %s' % presentmetadata)
        
    def testTopicIndexesTeardown(self):
        presentindexes = []
        allindexes = self.atct_tool.getIndexes()
        for index in ["getRawClassifications","getRawSpecialties","getRawCommittees","getRawPeople","getRawDepartments","getSortableName"]:
            if index in allindexes:
                presentindexes.append(index)
        self.failIf(presentindexes, 'ATCT Tool still has the following indexes: %s' % presentindexes)
        
    def testTopicMetadataTeardown(self):
        presentmetadata = []
        allmetadata = self.atct_tool.getAllMetadata()
        for fieldName in ["getCommitteeNames","getDepartmentNames","getSpecialtyNames","getClassificationNames","getResearchTopics"]:
            if fieldName in allmetadata:
                presentmetadata.append(fieldName)
        self.failIf(presentmetadata, 'ATCT Tool is missing the following metadata fields: %s' % presentmetadata)
    
    def testConfigletTeardown(self):
        cp = getToolByName(self.portal, 'portal_controlpanel')
        self.failIf("FacultyStaffDirectory" in [ c.id for c in cp._actions ], 'FacultyStaffDirectory configlet is still registered with the portal controlpanel')
        
    def testKupuLinkableTypesSetup(self):
        if self.has_kupu:
            missingltypes = checkKupuResourceList(self.ktool, 'linkable', linkableKupuTypes)
            self.failUnlessEqual(missingltypes, linkableKupuTypes, '%s not listed as linkable by Kupu' % missingltypes)

    def testKupuMediaTypesSetup(self):
        if self.has_kupu:
            missingmtypes = checkKupuResourceList(self.ktool, 'mediaobject', mediaKupuTypes)
            self.failUnlessEqual(missingmtypes, mediaKupuTypes, '%s not listed as media by Kupu' % missingmtypes)

    def testKupuCollectionTypesSetup(self):        
        if self.has_kupu:
            missingctypes = checkKupuResourceList(self.ktool, 'collection', collectionKupuTypes)
            self.failUnlessEqual(missingctypes, collectionKupuTypes, '%s not listed as collection by Kupu' % missingctypes)

    def testSkinLayerTeardown(self):
        skins = getToolByName(self.portal, 'portal_skins')
        for layerName in skins.getSkinSelections():
            self.failIf('FacultyStaffDirectory' in skins.selections[layerName], 'Skin layer not unregistered in layer %s' % layerName)
        
    def testStepsUnregistered(self):
        setup = getToolByName(self.portal, 'portal_setup')
        registry = setup.getImportStepRegistry()
        remainingIds = [a['id'] for a in registry.listStepMetadata() if 'Products.FacultyStaffDirectory' in a['handler']]
        self.failIf(remainingIds, "The following import steps were not unregistered: %s" % remainingIds)

        
class testReinstall(testPlone):
    def afterSetUp(self):
        migrationTool = getToolByName(self.portal, 'portal_migration')
        self.isPlone3OrBetter = migrationTool.getInstanceVersion() >= '3.0'
        self.loginAsPortalOwner()
        self.directory = self.getPopulatedDirectory()
        self.person = self.getPerson(id='abc123', firstName="Test", lastName="Person")
        
    def testUsersExistOnReinstall(self):
        
        # Person/Member abc123 should exist in acl_users as a membrane user object
        acl = getToolByName(self.portal, 'acl_users')
        self.failUnless(acl.getUserById(id='abc123'))

        # Reinstall the product
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        #qi.installProduct('FacultyStaffDirectory', reinstall=True)
        qi.reinstallProducts(products='FacultyStaffDirectory')
        
        # abc123 should still exist in acl_users
        self.failUnless(acl.getUserById(id='abc123'))
        
class testLargeDirectory(testPlone):
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.numPeople = 60
        self.directory = self.getPopulatedDirectory()
        self.person_ids = self.getLargeDirectory(self.directory, self.numPeople)
        
    def testLargeDirSetup(self):
        numPeople = len(self.directory.getPeople())
        self.failUnlessEqual(numPeople, self.numPeople, "wrong number of people in the directory (%d), something is wrong" % numPeople)
        
    def testLargeDirReinstall(self):
        """Benchmark and test reinstalling FSD with a directory holding a large number of people"""
        from time import time
        from random import choice
        
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        acl = getToolByName(self.portal, 'acl_users')
        
        # pick a user and make sure they exist in acl_users before we start
        user_id = choice(self.person_ids)
        person = self.directory[user_id]
        self.failUnless(acl.getUserById(id=user_id),"Problem:  person is not listed in acl_users")
        self.failUnless(person.UID(),"Problem: expected person object %s to have a UID.  It does not" % person)
        
        # how long does it take to reinstall FSD?
        import time
        start_time = time.time()
        qi.reinstallProducts(products='FacultyStaffDirectory')
        end_time = time.time()
        elapsed_time = end_time-start_time
        reinstall_report = "\nreinstalling FSD with a directory containing %s people took %s seconds\n" % (self.numPeople, elapsed_time)
        print "\n" + ("*" * 20) + reinstall_report + ("*" * 20)
        
        # test that a person in the FSD is still a user
        self.failUnless(acl.getUserById(id=user_id),"Problem:  after reinstall person is not listed in acl_users")
        self.failUnless(person.UID(),"Problem: after reinstall expected person object %s to have a UID.  It does not" % person)
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testInstall))
    suite.addTest(makeSuite(testUninstall))
    suite.addTest(makeSuite(testReinstall))
    suite.addTest(makeSuite(testLargeDirectory))
    
    return suite
