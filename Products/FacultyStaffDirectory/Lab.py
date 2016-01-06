# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import View
from Products.FacultyStaffDirectory.PersonGrouping import PersonGrouping
from Products.Relations.field import RelationField
from Products.FacultyStaffDirectory.config import *
from Products.CMFCore.utils import getToolByName
from Products.FacultyStaffDirectory.interfaces.lab import ILab
from zope.interface import implements
from Products.FacultyStaffDirectory.permissions import ASSIGN_LABS_TO_PEOPLE
from Products.FacultyStaffDirectory import FSDMessageFactory as _

schema = Schema((
    StringField(
        name="lab_short_name",
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_labshort", default=u"Lab Short Name"),
            description=_(u"FacultyStaffDirectory_description_labshort", default=u""),
            i18n_domain='FacultyStaffDirectory',
            ),
            required=False,
            allow_search=1,
            
        ),
    StringField(
        name='dept_url',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_labUrl", default=u"Primary Lab URL"),
            description=_(u"FacultyStaffDirectory_description_laburl", default=u""),
            i18n_domain='FacultyStaffDirectory',
        ),
        validators = ('isURL')
     
    ),
    ImageField(
        name='image',
        widget=ImageWidget(
            label=_(u"FacultyStaffDirectory_label_image", default=u"Image"),
            i18n_domain='FacultyStaffDirectory',
            default_content_type='image/gif',
        ),
        storage=AttributeStorage(),
        original_size=(400, 500),
        sizes={'thumb': (100, 125), 'normal': (200, 250)},
        default_output_type='image/jpeg',
        allowable_content_types=('image/gif','image/jpeg','image/png'),
    ),
    RelationField(
            name='pi',
            widget=ReferenceBrowserWidget(
                label=_(u"FacultyStaffDirectory_label_pi", default=u"Principal Investigator"),
                i18n_domain='FacultyStaffDirectory',
                allow_browse=0,
                allow_search=1,
                show_results_without_query=1,
                base_query="_search_people_in_this_fsd",
                startup_directory_method="_get_parent_fsd_path",  
            ),
            write_permission=ASSIGN_LABS_TO_PEOPLE,
            allowed_types=('FSDPerson',),
            multiValued=0,
            relationship='lab_pi'
        ),

    RelationField(
        name='members',
        widget=ReferenceBrowserWidget(
            label=_(u"FacultyStaffDirectory_label_members", default=u"Members"),
            i18n_domain='FacultyStaffDirectory',
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
            base_query="_search_people_in_this_fsd",
            startup_directory_method="_get_parent_fsd_path",  
        ),
        write_permission=ASSIGN_LABS_TO_PEOPLE,
        allowed_types=('FSDPerson',),
        multiValued=1,
        relationship='lab_members'
    ),
 ),

)

Lab_schema = getattr(PersonGrouping, 'schema', Schema(())).copy() + schema.copy()

class Lab(PersonGrouping):
    """
    """
    security = ClassSecurityInfo()
    implements(ILab)
    _at_rename_after_creation = True
    meta_type = portal_type="FSDLab"
    schema = Lab_schema   
    # Methods
    security.declareProtected(View, 'getMembershipInformation')
    def getMembershipInformation(self, person):
        """ Get the lab membership information for a specific person
        """
        refCatalog = getToolByName(self, 'reference_catalog')
        refs = refCatalog.getReferences(self, 'lab_members', person)

        if not refs:
            return None
        else:
            return refs[0].getContentObject()

    security.declareProtected(View, 'getPeople')
    def getPeople(self):
        """ Return the people in this lab.
            Mainly for context-sensitive classifications
        """
        return self.getMembers()
        
    security.declareProtected(View, 'getRawPeople')
    def getRawPeople(self):
        """ Return the people associations associated with this lab
        """
        return self.getRawMembers()
    
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
        
registerType(Lab, PROJECTNAME)
# end of class Lab
