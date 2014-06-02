# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces.specialtiesfolder import ISpecialtiesFolder
from zope.interface import implements

schema = ATContentTypeSchema.copy() + Schema((),)

SpecialtiesFolder_schema = OrderedBaseFolderSchema.copy() + schema.copy()
finalizeATCTSchema(SpecialtiesFolder_schema, folderish=True)

class SpecialtiesFolder(OrderedBaseFolder, ATCTContent):
    """
    """
    security = ClassSecurityInfo()
    implements(ISpecialtiesFolder)
    meta_type = portal_type = 'FSDSpecialtiesFolder'
    
    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although, 
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' in SpecialtiesFolder_schema.getSchemataNames():
        SpecialtiesFolder_schema.changeSchemataForField('description', 'categorization')
    else:
        SpecialtiesFolder_schema.changeSchemataForField('description', 'metadata')
        SpecialtiesFolder_schema.changeSchemataForField('relatedItems', 'metadata')

    _at_rename_after_creation = True
    schema = SpecialtiesFolder_schema
registerType(SpecialtiesFolder, PROJECTNAME)
