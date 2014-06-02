# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.Permissions import view as View
from Products.Archetypes.atapi import *
from Products.FacultyStaffDirectory.PersonGrouping import PersonGrouping
from Products.Relations.field import RelationField
from Products.FacultyStaffDirectory.config import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import View, ManageProperties, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.CMFCore.permissions import ManageUsers
from Products.membrane.at.interfaces import IPropertiesProvider
from Products.FacultyStaffDirectory.interfaces.classification import IClassification
from Acquisition import aq_inner, aq_parent
from Products.FacultyStaffDirectory.permissions import ASSIGN_CLASSIFICATIONS_TO_PEOPLE
from Products.FacultyStaffDirectory import FSDMessageFactory as _
from DateTime import DateTime

schema = Schema((

    RelationField(
        name='people',
        widget=ReferenceBrowserWidget(
            label=_(u"FacultyStaffDirectory_label_people", default=u"People"),
            i18n_domain='FacultyStaffDirectory',
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
            base_query="_search_people_in_this_fsd",
            startup_directory_method="_get_parent_fsd_path",
        ),
        write_permission=ASSIGN_CLASSIFICATIONS_TO_PEOPLE,
        allowed_types=('FSDPerson',),
        multiValued=1,
        relationship='classifications_people'
    ),
),
)

Classification_schema = getattr(PersonGrouping, 'schema', Schema(())).copy() + schema.copy()

class Classification(PersonGrouping):
    """
    """
    security = ClassSecurityInfo()
    meta_type = portal_type = "FSDClassification"
    # zope3 interfaces
    implements(IClassification, IPropertiesProvider)
    _at_rename_after_creation = True
    schema = Classification_schema
    # Methods
    security.declareProtected(View, 'getPeople')
    def getPeople(self):
        """ Return a list of people in this classification, filtered by the current context
        """

        secman = getSecurityManager()
        
        #There *has* to be a better way to do this...
        localPeople = self.getReferences()

        #Get the intersection of people referenced to this classification and people within/referenced to the parent
        classificationPeople = list(set(localPeople) & set(self.aq_parent.getPeople()))
        
        #Determine the valid people to show
        visiblePeople = []
        currentDateTime = DateTime()
        for person in classificationPeople:
            if currentDateTime >= person.getEffectiveDate() and (currentDateTime < person.getExpirationDate() or person.getExpirationDate() is None):
                if secman.checkPermission(View, person):
                    visiblePeople.append(person)
                
        #Return only the visible people
        return visiblePeople

    security.declareProtected(View, 'getSortedPeople')
    def getSortedPeople(self):
        """ Return a list of people, sorted by SortableName
        """
        people = self.getPeople()
        return sorted(people, cmp=lambda x,y: cmp(x.getSortableName(), y.getSortableName()))
    

    #
    # Validators
    #
    security.declarePrivate('validate_id')
    def validate_id(self, value):
        """Ensure the id is unique, also among groups globally
        """
        if value != self.getId():
            parent = aq_parent(aq_inner(self))
            if value in parent.objectIds():
                return "An object with id '%s' already exists in this folder" % value
        
            groups = getToolByName(self, 'portal_groups')
            if groups.getGroupById(value) is not None:
                return "A group with id '%s' already exists in the portal" % value

registerType(Classification, PROJECTNAME)
