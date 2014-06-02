# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces.departmentalmembership import IDepartmentalMembership
from zope.interface import implements
from Products.FacultyStaffDirectory import FSDMessageFactory as _

schema = Schema((

    StringField(
        name='position',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_position", default=u"Position"),
            i18n_domain='FacultyStaffDirectory',
        )
    ),

    StringField(
        name='title',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_title", default=u"Title"),
            i18n_domain='FacultyStaffDirectory',
            visible={'edit': 'invisible', 'view': 'invisible' },
        )
    ),
),
)

DepartmentalMembership_schema = BaseSchema.copy() + schema.copy()

class DepartmentalMembership(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    implements(IDepartmentalMembership)
    meta_type = portal_type = 'FSDDepartmentalMembership'
    _at_rename_after_creation = True
    schema = DepartmentalMembership_schema
       
    aliases = {
        '(Default)' : '(dynamic view)',
        'view' : '(selected layout)',
        'index.html' : '(dynamic view)',
        'edit' : 'departmentalmembership_edit',
    }

registerType(DepartmentalMembership, PROJECTNAME)
