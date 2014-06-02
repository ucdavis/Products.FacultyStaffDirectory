#This script is tested and works

from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserObject
from zope.component.hooks import getSite


def AddReviewerRole(self):
     
     site = getSite()
     directory = site.people
     people = directory.listFolderContents(contentFilter={"portal_type" : "FSDPerson"})
     for person in people:
          userId = person.getId()
          userfolder = directory[userId]
          roles = list(userfolder.get_local_roles_for_userid(userId))        
          roles.extend(['Owner', 'User Preferences Editor', u'Reviewer'])
            # eliminate duplicated roles
          roles = list(set(roles))
          userfolder.manage_setLocalRoles(userId, roles)
     return "done"
