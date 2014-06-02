from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IGroup
from Products.FacultyStaffDirectory.config import TOOLNAME as FSD_TOOL
from Products.FacultyStaffDirectory.interfaces.department import IDepartment
from Products.FacultyStaffDirectory.membership.person import UserRelated

class Group(object):
    """Allow a Department to act as a group for contained people
    """
    implements(IGroup)
    adapts(IDepartment)
    
    def __init__(self, context):
        self.context = context
        
    def Title(self):
        return self.context.Title()
    
    def getRoles(self):
        """We don't actually want a department to provide any global roles to it's members,
        so let's just return an empty list for this
        """
        return ()
    
    def getGroupId(self):
        return self.context.getId()

    def getGroupMembers(self):
        fsd_tool = getToolByName(self.context,FSD_TOOL)
        state = getToolByName(self.context, 'portal_workflow').getInfoFor(self.context, 'review_state')
        if state not in (fsd_tool.getActiveMembraneStates()):
            return ()

        members = self.context.getMembers()
        mlist = [UserRelated(m).getUserId() for m in members]
        return tuple(mlist)
