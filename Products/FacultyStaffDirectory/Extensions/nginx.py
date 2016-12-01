from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView



def getLists(self):
    catalog = getToolByName(self, 'portal_catalog')
    departments = catalog.searchResults ({'portal_type': 'FSDDepartment'})
    classifications = catalog.searchResults ({'portal_type': 'FSDClassification'})
    
    for department in departments:
        deptId = department.id
        print deptId
        
    for classification in classifications:
        classId = classification.id
        print classId