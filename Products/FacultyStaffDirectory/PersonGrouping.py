# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces.facultystaffdirectory import IFacultyStaffDirectory
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.FacultyStaffDirectory import FSDMessageFactory as _

schema =  ATContentTypeSchema.copy() + Schema((

    TextField(
        name='text',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=_(u"FacultyStaffDirectory_label_text", default=u"Body Text"),
            i18n_domain='FacultyStaffDirectory',
        ),
        default_output_type="text/x-html-safe",
        searchable=True,
        validators=('isTidyHtmlWithCleanup',)
    ),

),
)

PersonGrouping_schema = OrderedBaseFolderSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy

class PersonGrouping(OrderedBaseFolder, ATCTContent):
    """"""
    security = ClassSecurityInfo()
    meta_type = portal_type = 'FSDPersonGrouping'

    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although, 
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' not in PersonGrouping_schema.getSchemataNames():
        PersonGrouping_schema.changeSchemataForField('relatedItems', 'metadata')
        
    _at_rename_after_creation = True
    schema = PersonGrouping_schema

    security.declareProtected(View, 'getClassifications')
    def getClassifications(self):
        """ Ignore the default FacultyStaffDirectory getClassifications so that we can use
            PersonGrouping subclasses outside of a FacultyStaffDirectory object. Making the assumption that there
            will only be one FacultyStaffDirectory and that all Person objects will be created
            inside of it (see the README for some justification for this).
        """
        
        if self.getPeople():
            fsdTool = getToolByName(self, 'facultystaffdirectory_tool')
            return fsdTool.getDirectoryRoot().getClassifications()
        else:
            return []

    security.declareProtected(View, 'getSortedPeople')
    def getSortedPeople(self):
        """ Return a list of peoplele, sorted by SortableName
        """
        people = self.getPeople()
        return sorted(people, cmp=lambda x,y: cmp(x.getSortableName(), y.getSortableName()))

    security.declareProtected(ModifyPortalContent, '_get_parent_fsd_path')
    def _get_parent_fsd_path(self, relative=True):
        """ given an object of an FSD type, return the path to the parent FSD of that object
        """
        url_tool = getToolByName(self, 'portal_url')
        # Walk up the tree until you find an FSD
        parent = aq_parent(aq_inner(self))
        while not IPloneSiteRoot.providedBy(parent):
            if IFacultyStaffDirectory.providedBy(parent):
                if relative:
                    # get the path relative to the portal root
                    path = '/'.join(url_tool.getRelativeContentPath(parent))
                else:
                    # return the path starting with the portal root
                    path = '/'.join(parent.getPhysicalPath())
                return path
            else:
                parent = aq_parent(aq_inner(parent))

        return ""

    security.declareProtected(ModifyPortalContent, '_search_people_in_this_fsd')
    def _search_people_in_this_fsd(self):
        """ search only parent FSD for only people
        """
        path = self._get_parent_fsd_path(relative=False)
        return {'portal_type': 'FSDPerson',
                'sort_on': 'sortable_title',
                'path': {'query': path}}

registerType(PersonGrouping, PROJECTNAME)

