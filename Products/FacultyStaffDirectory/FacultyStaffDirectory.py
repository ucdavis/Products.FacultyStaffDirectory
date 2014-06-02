# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.FacultyStaffDirectory.interfaces.facultystaffdirectory import IFacultyStaffDirectory
from Products.FacultyStaffDirectory.config import *
from Products.CMFCore.permissions import View, ManageUsers
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.membrane.at.interfaces import IPropertiesProvider
from Products.membrane.utils import getFilteredValidRolesForPortal
from Acquisition import aq_inner, aq_parent
from Products.FacultyStaffDirectory import FSDMessageFactory as _

schema = ATContentTypeSchema.copy() + Schema((
    LinesField('roles_',
        accessor='getRoles',
        mutator='setRoles',
        edit_accessor='getRawRoles',
        vocabulary='getRoleSet',
        default = ['Member'], 
        multiValued=1,
        write_permission=ManageUsers,
        widget=MultiSelectionWidget(
            label=_(u"FacultyStaffDirectory_label_FacultyStaffDirectoryRoles", default=u"Roles"),
            description=_(u"FacultyStaffDirectory_description_FacultyStaffDirectoryRoles", default=u"The roles all people in this directory will be granted site-wide"),
            i18n_domain="FacultyStaffDirectory",
            ),
        ),
    IntegerField('personClassificationViewThumbnailWidth',
        accessor='getClassificationViewThumbnailWidth',
        mutator='setClassificationViewThumbnailWidth',
        schemata='Display',
        default=100,
        write_permission=ManageUsers,
        widget=IntegerWidget(
            label=_(u"FacultyStaffDirectory_label_personClassificationViewThumbnailWidth", default=u"Width for thumbnails in classification view"),
            description=_(u"FacultyStaffDirectory_description_personClassificationViewThumbnailWidth", default=u"Show all person thumbnails with a fixed width (in pixels) within the classification view"),
            i18n_domain="FacultyStaffDirectory",
            ),
        ),
    ))

FacultyStaffDirectory_schema = OrderedBaseFolderSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy
finalizeATCTSchema(FacultyStaffDirectory_schema, folderish=True)

class FacultyStaffDirectory(OrderedBaseFolder, ATCTContent):
    """
    """
    security = ClassSecurityInfo()
    implements(IFacultyStaffDirectory, IPropertiesProvider)
    meta_type = portal_type = 'FSDFacultyStaffDirectory'

    # Make this permission show up on every containery object in the Zope instance. This is a Good Thing, because it easy to factor up permissions. The Zope Developer's Guide says to put this here, not in the install procedure (http://www.zope.org/Documentation/Books/ZDG/current/Security.stx). This is because it isn't "sticky", in the sense of being persisted through the ZODB. Thus, it has to run every time Zope starts up. Thus, when you uninstall the product, the permission doesn't stop showing up, but when you actually remove it from the Products folder, it does.
    security.setPermissionDefault('FacultyStaffDirectory: Add or Remove People', ['Manager', 'Owner'])

    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although, 
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' in FacultyStaffDirectory_schema.getSchemataNames():
        FacultyStaffDirectory_schema.changeSchemataForField('description', 'categorization')
    else:
        FacultyStaffDirectory_schema.changeSchemataForField('description', 'metadata')
        FacultyStaffDirectory_schema.changeSchemataForField('relatedItems', 'metadata')
    
    _at_rename_after_creation = True
    schema = FacultyStaffDirectory_schema
    
    # Methods
    security.declarePrivate('at_post_create_script')
    def at_post_create_script(self):
        """Actions to perform after a FacultyStaffDirectory is added to a Plone site"""
        # Create some default contents
        # Create some base classifications
        self.invokeFactory('FSDClassification', id='faculty', title='Faculty')
        self.invokeFactory('FSDClassification', id='staff', title='Staff')
        self.invokeFactory('FSDClassification', id='grad-students', title='Graduate Students')
        # Create a committees folder
        self.invokeFactory('FSDCommitteesFolder', id='committees', title='Committees')
        # Create a specialties folder
        self.invokeFactory('FSDSpecialtiesFolder', id='specialties', title='Specialties')

    security.declareProtected(View, 'getDirectoryRoot')
    def getDirectoryRoot(self):
        """Return the current FSD object through acquisition."""
        return self

    security.declareProtected(View, 'getClassifications')
    def getClassifications(self):
        """Return the classifications (in brains form) within this FacultyStaffDirectory."""
        portal_catalog = getToolByName(self, 'portal_catalog')
        return portal_catalog(path='/'.join(self.getPhysicalPath()), portal_type='FSDClassification', depth=1, sort_on='getObjPositionInParent')
        
    security.declareProtected(View, 'getSpecialtiesFolder')
    def getSpecialtiesFolder(self):
        """Return a random SpecialtiesFolder contained in this FacultyStaffDirectory.
           If none exists, return None."""
        specialtiesFolders = self.getFolderContents({'portal_type': 'FSDSpecialtiesFolder'})
        if specialtiesFolders:
            return specialtiesFolders[0].getObject()
        else:
            return None

    security.declareProtected(View, 'getPeople')
    def getPeople(self):
        """Return a list of people contained within this FacultyStaffDirectory."""
        portal_catalog = getToolByName(self, 'portal_catalog')
        results = portal_catalog(path='/'.join(self.getPhysicalPath()), portal_type='FSDPerson', depth=1)
        return [brain.getObject() for brain in results]

    security.declareProtected(View, 'getSortedPeople')
    def getSortedPeople(self):
        """ Return a list of people, sorted by SortableName
        """
        people = self.getPeople()
        return sorted(people, cmp=lambda x,y: cmp(x.getSortableName(), y.getSortableName()))

    security.declareProtected(View, 'getDepartments')
    def getDepartments(self):
        """Return a list of FSDDepartments contained within this site."""
        portal_catalog = getToolByName(self, 'portal_catalog')
        results = portal_catalog(portal_type='FSDDepartment')
        return [brain.getObject() for brain in results]

    security.declareProtected(View, 'getAddableInterfaceSubscribers')
    def getAddableInterfaceSubscribers():
        """Return a list of (names of) content types marked as addable using the
           IFacultyStaffDirectoryAddable interface."""
        return [type['name'] for type in listTypes() if IFacultyStaffDirectoryAddable.implementedBy(type['klass'])]

    security.declarePrivate('getRoleSet')
    def getRoleSet(self):
        """Get the roles vocabulary to use."""
        portal_roles = getFilteredValidRolesForPortal(self)
        allowed_roles = [r for r in portal_roles if r not in INVALID_ROLES]
        return allowed_roles

    #
    # Validators
    #
    security.declarePrivate('validate_id')
    def validate_id(self, value):
        """Ensure the id is unique, also among groups globally."""
        if value != self.getId():
            parent = aq_parent(aq_inner(self))
            if value in parent.objectIds():
                return _(u"An object with id '%s' already exists in this folder") % value
        
            groups = getToolByName(self, 'portal_groups')
            if groups.getGroupById(value) is not None:
                return _(u"A group with id '%s' already exists in the portal") % value
                
registerType(FacultyStaffDirectory, PROJECTNAME)
