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
    BooleanField(
        name='primary_department',
        widget=BooleanWidget(
            label=_(u"FacultyStaffDirectory_label_primary_deparment", default=u"Primary Department"),
            description=_(u"FacultyStaffDirectory_description_primary_departmentdescription", default=u"Check if primary/home department."),
                    i18n_domain='FacultyStaffDirectory',
                ),
                default=False,
            ),
    
    StringField(
        name='dept_officeAddress',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_officeAddress", default=u"Office Location Building and Room"),
            i18n_domain='FacultyStaffDirectory',
            searchable=True,
        
        )
    ),
    StringField(
        name='dept_streetAddress',
        default='1 Shields Avenue',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_streetAddress", default=u"Street Address"),
            i18n_domain='FacultyStaffDirectory',
            
            searchable=True,
        
        )
    ),
    StringField(
        name='dept_city',
        default='Davis',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_city", default=u"City"),
            i18n_domain='FacultyStaffDirectory',
            
            searchable=True,
        
        )
    ),
    StringField(
        name='dept_state',
        default='CA',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_State", default=u"State"),
            i18n_domain='FacultyStaffDirectory',
            
            searchable=True,
        
        )
    ),
    StringField(
        name='dept_zip',
        default='95616',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_zip", default=u"Zip Code"),
            i18n_domain='FacultyStaffDirectory',
            
            searchable=True,
        
        )
    ),
    StringField(
        name='dept_officePhone',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_officePhone", default=u"Office Phone"),
            description=_(u"FacultyStaffDirectory_description_officePhone", default=u""),
            i18n_domain='FacultyStaffDirectory',
            searchable=True,
        )
    ),
    
    StringField(
         name='quarter',
         widget=StringWidget(
             label=_(u"FacultyStaffDirectory_label_Quarter", default=u"Quarter"),
             description=_(u"FacultyStaffDirectory_description_Quarter", default=u"Quarter and year, aka Fall 2012"),
             i18n_domain='FacultyStaffDirectory',
          ),
          ),
    LinesField('officeHours',
          required=False,
          searchable=True,
          widget=LinesWidget(
               label=_(u"FacultyStaffDirectory", default=u"Office Hours"),
               description=_(u"FacultyStaffDirectory", default=u"One entry per line, aka Tuesday 8:00am - 10:00 am"),
               i18n_domain='FacultyStaffDirectory',
    )    
    
),
    TextField(
        name='summarybio',
        widget=RichWidget(
            label=_(u"FacultyStaffDirectory_label_summarybio", default=u"Summary Bio"),
            description=_(u"FacultyStaffDirectory_description_summarybio", default=u""),
            i18n_domain='FacultyStaffDirectory',
            searchable=True,
            validators=('isTidyHtmlWithCleanup',),
            default_output_type='text/x-html-safe',
        )
    )
))

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
