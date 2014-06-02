from zope.interface import implements, Interface
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.workflow.interfaces import ISharingPageRole as interfaceToImplement

class PersonnelManagerRole(object):
    implements(interfaceToImplement)
    title = _(u"title_can_manage_personnel", default=u"Can manage personnel")
    required_permission = 'Manage portal'
