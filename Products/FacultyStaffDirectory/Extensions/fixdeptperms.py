from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserObject
from zope.component.hooks import getSite
from plone import api


def bounceDepartment(self):
    site = getSite()
    directory = site.people
    people = directory.listFolderContents(contentFilter={"portal_type": "FSDPerson"})
    for person in people:
        userID = person.getId()
        pUID = person.UID()
        refs = person.at_references.items()
        depts = self.getDepartments
        for dept in depts:
            
        for ref in refs:
            if ref.relationship == "DepartmentalMembership":
            
                 
                
        rc = getToolByName(context, 'reference_catalog')
        deptrels = rc.searchResults({'sourceUID' : pUID, 'relationship' : 'DepartmentalMembership'})
        for rel in deptrels:
            reltid = rel.targetUID
            dept = self.reference_catalog.lookupObject(reltid)
            relboj = rel.getObject()
            # membership content object
            cobj = relobj.getContentObject()
            position = cobj.position
            title = cobj.title
            primary = cobj.primary_department
            deptadd = cobj.dept_officeAddress
            deptstreet = cobj.dept_streetAddress
            deptcity = cobj.dept_city
            deptstate = cobj.dept_state
            deptzip  = cobj.dept_zip
            deptphone = cobj.dept_officePhone
            quarter = cobj.quarter
            offhours = cobj.officeHours
            sumbio = cobj.summarybio
            
            api.content.delete(obj=relobj)
            
            person.setDepartment(dept)
            
            
            
            
            get departmental membership and save although how is that different than the related record?
            delete relationship (use the api)
            create a new relationship with the membership info
            
                
                
def deptProcessing(self, person):
     depts = self.getDepartments(person)
     for dept in depts:
         membship = dept.getMembershipInformation(person)
         position = membship.position
         title = membship.title
         primary = membship.primary_department
         deptadd = membship.dept_officeAddress
         deptstreet = membship.dept_streetAddress
         deptcity = membship.dept_city
         deptstate = membship.dept_state
         deptzip  = membship.dept_zip
         deptphone = membship.dept_officePhone
         quarter = membship.quarter
         offhours = membship.officeHours
         sumbio = membship.summarybio
    return 
         
         

def AddEditRole(self):
     
     site = getSite()
     directory = site.people
     people = directory.listFolderContents(contentFilter={"portal_type" : "FSDPerson"})
     for person in people:
          userId = person.getId()
          departments = userId.getDepartments()
          for department in departments
              membership = getMembershipInformation(userId)
              roles = list()
          
          userfolder = directory[userId]
          membershipt = userId.getDepartmentalMembership
          roles = list(userfolder.get_local_roles_for_userid(userId))        
          roles.extend(['Owner', 'User Preferences Editor', u'Reviewer'])
            # eliminate duplicated roles
          roles = list(set(roles))
          userfolder.manage_setLocalRoles(userId, roles)
     return "done"
site.reference_catalog.lookupObject('ce380ef0f10a85beb864025928e1819b')


mtool = context.portal_membership
if not mtool.checkPermission('Relations: Manage content relations', context):
    state.set(status='failure',
              portal_status_message="Insufficient privileges.")
return state