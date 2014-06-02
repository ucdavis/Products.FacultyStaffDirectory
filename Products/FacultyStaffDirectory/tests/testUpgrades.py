# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.tests.testPlone import testPlone, PACKAGE_HOME
import os
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.upgrade import listUpgradeSteps

class testUpgrades(testPlone):
    """Test-cases for FacultyStaffDirectory migration."""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getToolByName(self.portal,'portal_quickinstaller')
        self.ps = getToolByName(self.portal,'portal_setup')
        self.wf = getToolByName(self.portal,'portal_workflow')
        self.wf.setChainForPortalTypes(['FSDFacultyStaffDirectory'],'simple_publication_workflow')
        

    def installZexp(self,zexpfile):
        filename = os.path.join(PACKAGE_HOME, 'input',zexpfile)
        self.portal._importObjectFromFile(filename, verify=0)
        self.directory = self.portal['personnel']
        
    def runUpgradeStep(self, source, dest):
        usd = listUpgradeSteps(self.ps,'Products.FacultyStaffDirectory:default',None)
        ourstepdict = [step for step in usd if source in step['source'] and dest in step['dest']][0]
        ourstep = ourstepdict['step']
        ourstep.doStep(self.ps)

    def test_2_to_3_upgrade_private(self):
        try:
            self.installZexp('FSD2dot1dot4_private.zexp')
        except Exception,detail:
            print detail
        self.runUpgradeStep('1', '2')
        self.assertEquals(self.wf.getInfoFor(self.directory,'review_state'),'private')
        
    def test_2_to_3_upgrade_public(self):
        try:
            self.installZexp('FSD2dot1dot4_public.zexp')
        except Exception,detail:
            print detail
        self.runUpgradeStep('1', '2')
        self.assertEquals(self.wf.getInfoFor(self.directory,'review_state'),'private')

    def test_2_to_3_upgrade_draft(self):
        try:
            self.installZexp('FSD2dot1dot4_draft.zexp')
        except Exception,detail:
            print detail
        self.runUpgradeStep('1', '2')
        self.assertEquals(self.wf.getInfoFor(self.directory,'review_state'),'private')
        
    def test_30_to_301_upgrade(self):
        tool = getToolByName(self.portal, 'facultystaffdirectory_tool')
        tool.setActiveMembraneStates([])

        self.runUpgradeStep('4', '5')

        self.assertTrue('published' in tool.getActiveMembraneStates())
            
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUpgrades))
    return suite
