# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Relations.field import RelationField
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.PersonGrouping import PersonGrouping
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.interfaces.specialty import ISpecialty
from Products.FacultyStaffDirectory.permissions import ASSIGN_SPECIALTIES_TO_PEOPLE

from zope.interface import implements
#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory('FacultyStaffDirectory')
from Products.FacultyStaffDirectory import FSDMessageFactory as _

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
        write_permission=ASSIGN_SPECIALTIES_TO_PEOPLE,
        allowed_types=('FSDPerson',),
        multiValued=True,
        relationship='SpecialtyInformation'  # weird relationship name is ArchGenXML's fault
    ),

    ImageField(
        name='overviewImage',
        schemata='Overview',
        widget=ImageWidget(
            label=_(u"FacultyStaffDirectory_label_overview_image", default=u"Overview image (used for specialty overview view)"),
            i18n_domain='FacultyStaffDirectory',
            default_content_type='image/gif',
        ),
        storage=AttributeStorage(),
        original_size=(200, 200),
        sizes={'normal': (200, 250)},
        default_output_type='image/jpeg',
        allowable_content_types=('image/gif','image/jpeg','image/png'),
    ),

    TextField(
        name='overviewText',
        schemata='Overview',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=_(u"FacultyStaffDirectory_label_overview_text", default=u"Overview text (used for specialty overview view)"),
            i18n_domain='FacultyStaffDirectory',
        ),
        default_output_type="text/x-html-safe",
        searchable=True,
        validators=('isTidyHtmlWithCleanup',)
    )

),
)

Specialty_schema = getattr(PersonGrouping, 'schema', Schema(())).copy() + schema.copy()

class Specialty(PersonGrouping):
    """
    """
    security = ClassSecurityInfo()
    implements(ISpecialty)
    meta_type = portal_type = 'FSDSpecialty'

    _at_rename_after_creation = True
    schema = Specialty_schema
    # Methods
    security.declareProtected(View, 'getSpecialtyInformation')
    def getSpecialtyInformation(self, person):
        """
        Get the specialty information for a specific person
        """
        refCatalog = getToolByName(self, 'reference_catalog')
        refs = refCatalog.getReferences(self, 'SpecialtyInformation', person)

        if refs:
            return refs[0].getContentObject()
        else:
            return None

registerType(Specialty, PROJECTNAME)
