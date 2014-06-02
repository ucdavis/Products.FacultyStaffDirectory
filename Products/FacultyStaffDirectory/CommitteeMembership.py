# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces.committeemembership import ICommitteeMembership
from zope.interface import implements
from Products.FacultyStaffDirectory import FSDMessageFactory as _

schema = ATContentTypeSchema.copy() + Schema((

    StringField(
        name='position',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_position", default=u"Position"),
            i18n_domain='FacultyStaffDirectory',
        )
    ),

    StringField(
        name='title',
        default="Position",
        widget=StringWidget(
            visible={'edit':'invisible', 'view':'visible'},
            label=_(u"FacultyStaffDirectory_label_title", default=u"Title"),
            i18n_domain='FacultyStaffDirectory',
        ),
        accessor="Title"
    ),

),
)

CommitteeMembership_schema = BaseSchema.copy() + schema.copy()
finalizeATCTSchema(CommitteeMembership_schema)

class CommitteeMembership(BaseContent, ATCTContent):
    """
    """
    security = ClassSecurityInfo()
    implements(ICommitteeMembership)
    meta_type = portal_type = 'FSDCommitteeMembership'

    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although, 
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' in CommitteeMembership_schema.getSchemataNames():
        CommitteeMembership_schema.changeSchemataForField('description', 'categorization')
    else:
        CommitteeMembership_schema.changeSchemataForField('description', 'metadata')
        CommitteeMembership_schema.changeSchemataForField('relatedItems', 'metadata')


    _at_rename_after_creation = True

    schema = CommitteeMembership_schema

    # Methods
registerType(CommitteeMembership, PROJECTNAME)
# end of class CommitteeMembership

