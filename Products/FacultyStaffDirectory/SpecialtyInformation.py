# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.FacultyStaffDirectory.config import *

from Products.FacultyStaffDirectory.interfaces.specialtyinformation import ISpecialtyInformation
from zope.interface import implements
from Products.FacultyStaffDirectory import FSDMessageFactory as _

schema = Schema((

    TextField(
        name='researchTopic',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',),
        widget=RichWidget(
            label=_(u"FacultyStaffDirectory_label_researchTopic", default=u"Research Topic"),
            i18n_domain='FacultyStaffDirectory',
            allow_file_upload=False,
            rows=5,
        ),
        default_output_type='text/x-html-safe'
    ),

    StringField(
        name='title',
        default="Research Topic",
        widget=StringWidget(
            visible={'edit': 'invisible', 'view': 'visible'},
            label=_(u"FacultyStaffDirectory_label_title", default=u"Title"),
            i18n_domain='FacultyStaffDirectory',
        ),
        accessor="Title"
    ),

),
)

SpecialtyInformation_schema = BaseSchema.copy() + schema.copy()

class SpecialtyInformation(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    implements(ISpecialtyInformation)
    meta_type = portal_type = 'FSDSpecialtyInformation'
    schema = SpecialtyInformation_schema
registerType(SpecialtyInformation, PROJECTNAME)
