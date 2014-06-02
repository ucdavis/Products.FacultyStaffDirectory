# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from OFS.Image import Image
from cStringIO import StringIO
import logging
import re
from sha import sha

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from zope.event import notify
from zope.interface import implements, classImplements
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces import IMultiPageSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.ATContentTypes.lib.calendarsupport import n2rn, foldLine
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import View, ModifyPortalContent, SetOwnPassword, SetOwnProperties
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.navtree import buildFolderTree
from Products.CMFPlone.CatalogTool import getObjPositionInParent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode
from Products.membrane.at.interfaces import IUserAuthProvider, IPropertiesProvider, IGroupsProvider, IGroupAwareRolesProvider, IUserChanger
from Products.Relations.field import RelationField
from Products.validation import validation

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces.person import IPerson
from Products.FacultyStaffDirectory.interfaces.person import IPersonModifiedEvent
from Products.FacultyStaffDirectory.interfaces.facultystaffdirectory import IFacultyStaffDirectory
from Products.FacultyStaffDirectory.permissions import ASSIGN_CLASSIFICATIONS_TO_PEOPLE, ASSIGN_DEPARTMENTS_TO_PEOPLE, ASSIGN_COMMITTIES_TO_PEOPLE, ASSIGN_SPECIALTIES_TO_PEOPLE, CHANGE_PERSON_IDS
from Products.FacultyStaffDirectory.validators import SequenceValidator

from Products.FacultyStaffDirectory import FSDMessageFactory as _

logger = logging.getLogger('FacultyStaffDirectory')

schema = ATContentTypeSchema.copy() + Schema((
    
    StringField(
        name='firstName',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_firstName", default=u"First Name"),
            i18n_domain='FacultyStaffDirectory',
        ),
        required=True,
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='middleName',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_middleName", default=u"Middle Name"),
            i18n_domain='FacultyStaffDirectory',
        ),
        required=False,
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='lastName',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_lastName", default=u"Last Name"),
            i18n_domain='FacultyStaffDirectory',
        ),
        required=True,
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='suffix',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_suffix", default=u"Suffix"),
            description=_(u"FacultyStaffDirectory_description_suffix", default=u"Academic, professional, honorary, and social suffixes."),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='email',
        user_property=True,
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_email", default=u"Email"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True,
        validators=('isEmail',)
    ),
    
    LinesField(
        name='jobTitles',
        widget=LinesField._properties['widget'](
            label=_(u"FacultyStaffDirectory_label_jobTitles", default=u"Job Titles"),
            description=_(u"FacultyStaffDirectory_description_jobTitles", default=u"One per line"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        searchable=True
    ),
    
    StringField(
        name='officeAddress',
        widget=TextAreaWidget(
            label=_(u"FacultyStaffDirectory_label_officeAddress", default=u"Office Street Address"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True
    ),
    
    StringField(
        name='officeCity',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_officeCity", default=u"Office City"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True
    ),
    
    StringField(
        name='officeState',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_officeState", default=u"Office State"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information"
    ),
    
    StringField(
        name='officePostalCode',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_officePostalCode", default=u"Office Postal Code"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information"
    ),
    
    StringField(
        name='officePhone',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_officePhone", default=u"Office Phone"),
            description=_(u"FacultyStaffDirectory_description_officePhone", default=u""),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True,
    ),
    
    ImageField(
        name='image',
        schemata="Basic Information",
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
    
    TextField(
        name='biography',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=_(u"FacultyStaffDirectory_label_biography", default=u"Biography"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        searchable=True,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        user_property='description'
    ),
    
    LinesField(
        name='education',
        widget=LinesField._properties['widget'](
            label=_(u"FacultyStaffDirectory_label_education", default=u"Education"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        searchable=True
    ),
    
    LinesField(
        name='websites',
        widget=LinesField._properties['widget'](
            label=_(u"FacultyStaffDirectory_label_websites", default=u"Web Sites"),
            description=_(u"FacultyStaffDirectory_description_websites", default=u"One per line. Example: http://www.example.com/"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        validators = SequenceValidator('isURLs', validation.validatorFor('isURL'))
    ),
    
    StringField(
        name='id',
        widget=StringWidget(
            label=_(u"FacultyStaffDirectory_label_id", default=u"Access Account ID"),
            i18n_domain='FacultyStaffDirectory',
            description=_(u"FacultyStaffDirectory_description_id", default=u"Example: abc123"),
        ),
        required=True,
        user_property=True,
        schemata="Basic Information",
        write_permission=CHANGE_PERSON_IDS,
    ),
    
    ComputedField(
        name='title',
        widget=ComputedField._properties['widget'](
            label=_(u"FacultyStaffDirectory_label_fullName", default=u"Full Name"),
            visible={'edit': 'invisible', 'view': 'visible'},
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Basic Information",
        accessor="Title",
        user_property='fullname',
        searchable=True
    ),
    
    RelationField(
        name='classifications',
        vocabulary="_classificationReferences",
        widget=ReferenceWidget
        (
            label=_(u"FacultyStaffDirectory_label_classifications", default=u"Classifications"),
            i18n_domain='FacultyStaffDirectory',
        ),
        write_permission=ASSIGN_CLASSIFICATIONS_TO_PEOPLE,
        schemata="Basic Information",
        multiValued=True,
        relationship='people_classifications'
    ),
    
    RelationField(
        name='departments',
        widget=ReferenceBrowserWidget(
            label=_(u"FacultyStaffDirectory_label_departments", default=u"Departments"),
            i18n_domain='FacultyStaffDirectory',
            base_query="_search_departments_in_this_fsd",
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
            startup_directory_method="_get_parent_fsd_path",
        ),
        write_permission=ASSIGN_DEPARTMENTS_TO_PEOPLE,
        schemata="Basic Information",
        allowed_types=('FSDDepartment'),
        multiValued=True,
        relationship='DepartmentalMembership'
    ),
    
    RelationField(
        name='committees',
        widget=ReferenceBrowserWidget(
            visible={'edit': 'visible', 'view': 'visible'},
            label=_(u"FacultyStaffDirectory_label_committees", default=u"Committees"),
            i18n_domain='FacultyStaffDirectory',
            base_query="_search_committees_in_this_fsd",
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
            startup_directory_method="_get_parent_fsd_path",
        ),
        write_permission=ASSIGN_COMMITTIES_TO_PEOPLE,
        schemata="Professional Information",
        multiValued=True,
        relationship='members_committees',
        allowed_types=('Committee')
    ),
    
    RelationField(
        name='specialties',
        widget=ReferenceBrowserWidget(
            label=_(u"FacultyStaffDirectory_label_specialties", default=u"Specialties"),
            i18n_domain='FacultyStaffDirectory',
            base_query="_search_specialties_in_this_fsd",
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
            startup_directory_method="_get_parent_fsd_path"
        ),
        write_permission=ASSIGN_SPECIALTIES_TO_PEOPLE,
        schemata="Professional Information",
        multiValued=True,
        relationship='people_specialties',
        allowed_types=('FSDSpecialty')
    ),
    
    StringField('password',
        languageIndependent=True,
        required=False,
        mode='w',
        write_permission=SetOwnPassword,
        widget=PasswordWidget(
            label=_(u"FacultyStaffDirectory_label_password", default=u"Password"),
            description=_(u"FacultyStaffDirectory_description_password", default=u"Password for this person (Leave blank if you don't want to change the password.)"),
            i18n_domain='FacultyStaffDirectory',
            condition="python: modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getUseInternalPassword() and 'FSDPerson' in modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getEnableMembraneTypes()"
        ),
        schemata="Basic Information",
    ),
    
    StringField('confirmPassword',
        languageIndependent=True,
        required=False,
        mode='w',
        write_permission=SetOwnPassword,
        widget=PasswordWidget(
            label=_(u"FacultyStaffDirectory_label_confirmPassword", default=u"Confirm password"),
            description=_(u"FacultyStaffDirectory_description_confirmPassword", default=u"Please re-enter the password. (Leave blank if you don't want to change the password.)"),
            i18n_domain='FacultyStaffDirectory',
            condition="python: modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getUseInternalPassword() and 'FSDPerson' in modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getEnableMembraneTypes()"
        ),
        schemata="Basic Information",
    ),
    
    StringField('userpref_language',
        widget=SelectionWidget(
            label=_(u"label_language", default=u"Language"),
            description=_(u"help_preferred_language", default=u"Your preferred language."),
            i18n_domain='plone',
            condition="python:'FSDPerson' in modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getEnableMembraneTypes()"
        ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        vocabulary="_availableLanguages",
        user_property='language',
    ),
    
    StringField('userpref_wysiwyg_editor',
        widget=SelectionWidget(
            label=_(u"label_content_editor", default=u"Content editor"),
            description=_(u"help_content_editor", default=u"Select the content editor that you would like to use. Note that content editors often have specific browser requirements."),
            i18n_domain='plone',
            format="select",
            condition="python:'FSDPerson' in modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getEnableMembraneTypes()"
        ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        vocabulary="_availableEditors",
        user_property='wysiwyg_editor',
    ),
    
    BooleanField('userpref_ext_editor',
        widget=BooleanWidget(
            label=_(u"label_ext_editor", default=u"Enable external editing"),
            description=_(u"help_content_ext_editor", default=u"When checked, an icon will be made visible on each page which allows you to edit content with your favorite editor instead of using browser-based editors. This requires an additional application called ExternalEditor installed client-side. Ask your administrator for more information if needed."),
            i18n_domain='plone',
            condition="python:'FSDPerson' in modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getEnableMembraneTypes()",
            ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        user_property='ext_editor',
        default=False,
    ),
    
    StringField('userpref_portal_skin',
        widget=SelectionWidget(
            label=_(u"label_look", default=u"Look"),
            description=_(u"help_look", default=u"Appearance of the site."),
            i18n_domain='plone',
            format="select",
            condition="python:here.portal_skins.allow_any and 'FSDPerson' in modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getEnableMembraneTypes()",
        ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        vocabulary="_skinSelections",
        user_property='look',
    ),
    
    BooleanField('userpref_invisible_ids',
        widget=BooleanWidget(
            label=_(u"label_edit_short_names", default=u"Allow editing of Short Names"),
            description=_(u"help_display_names", default=u"Determines if Short Names (also known as IDs) are changable when editing items. If Short Names are not displayed, they will be generated automatically."),
            i18n_domain='plone',
            condition="python:here.portal_properties.site_properties.visible_ids and 'FSDPerson' in modules['Products.CMFCore.utils'].getToolByName(here, 'facultystaffdirectory_tool').getEnableMembraneTypes()"
            ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        user_property='invisible_ids',
    ),
    
    RelationField(
        name='assistants',
        widget=ReferenceBrowserWidget
        (
            label=_(u"FacultyStaffDirectory_label_assistants", default=u"Personal Assistant(s)"),
            description=_(u"FacultyStaffDirectory_description_assistants", default=u"Assistants can edit your directory entry."),
            i18n_domain='FacultyStaffDirectory',
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
            startup_directory_method="_get_parent_fsd_path",
            base_query="_search_people_in_this_fsd",
            restrict_browsing_to_startup_directory=True,
        ),
        write_permission="Modify portal content",
        schemata="Basic Information",
        multiValued=True,
        relationship='people_assistants',
        allowed_types=('FSDPerson'),
    ),
    
    TextField(
        name='terminationDetails',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=_(u"FacultyStaffDirectory_label_termination_details", default=u"Termination details"),
            description=_(u"FacultyStaffDirectory_description_termination_details", default=u"Message displayed to site visitors when the person's termination date has passed. Can be used to provide forwarding information or a link to someone who has taken over their responsibilities."),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Employment Information",
        searchable=False,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        user_property='description'
    ),
    ))

Person_schema = OrderedBaseFolderSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy

finalizeATCTSchema(Person_schema, folderish=True)

class PersonModifiedEvent(object):
    """Event that happens when edits to a Person have been saved"""
    implements(IPersonModifiedEvent)
    
    def __init__(self, context):
        self.context = context

class Person(OrderedBaseFolder, ATCTContent):
    """A person in the Faculty/Staff directory"""
    meta_type = portal_type = "FSDPerson"
    security = ClassSecurityInfo()
    # zope3 interfaces
    implements(IPerson,
               IUserAuthProvider,
               IPropertiesProvider,
               IGroupsProvider,
               IGroupAwareRolesProvider,
               IAttributeAnnotatable,
               IUserChanger)
    
    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although,
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' in Person_schema.getSchemataNames():
        Person_schema.changeSchemataForField('description', 'settings')
    else:
        Person_schema.changeSchemataForField('description', 'metadata')
        Person_schema.changeSchemataForField('relatedItems', 'metadata')
    
    # reorder the fields to move the dates into the employment information schemata along with the 
    # terminiation details field and rename the effective and expiration dates.
    Person_schema['effectiveDate'].schemata = 'Employment Information'
    Person_schema['effectiveDate'].widget.label = _(u"label_edit_hire_date", default=u"Hire Date")
    Person_schema['effectiveDate'].widget.description = _(u"description_edit_hire_date", default=u"The date when the person will be hired. If no date is selected the person will be considered hired immediately.")
    Person_schema['expirationDate'].schemata = 'Employment Information'
    Person_schema['expirationDate'].widget.label = _(u"label_edit_termination_date", default=u"Termination Date")
    Person_schema['expirationDate'].widget.description = _(u"description_edit_termination_date", default=u"The date when the person leaves the organization. This will automatically make the person invisible for others at the given date.")
    Person_schema.moveField('effectiveDate', after='specialties')
    Person_schema.moveField('expirationDate', after='effectiveDate')
    Person_schema.moveField('terminationDetails', after='expirationDate')
    
    _at_rename_after_creation = True
    schema = Person_schema
    # Methods
    security.declareProtected(View, 'at_post_create_script')
    def at_post_create_script(self):
        """Notify that the Person has been modified.
        """
        notify(PersonModifiedEvent(self))

    security.declareProtected(View, 'at_post_edit_script')
    def at_post_edit_script(self):
        """Notify that the Person has been modified.
        """
        notify(PersonModifiedEvent(self))
    
    def __call__(self, *args, **kwargs):
        return self.getId()
    
    security.declareProtected(View, 'vcard_view')
    def vcard_view(self, REQUEST, RESPONSE):
        """vCard 3.0 output
        """
        RESPONSE.setHeader('Content-Type', 'text/x-vcard')
        RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.vcf"' % self.getId())
        out = StringIO()
        
        # Get the fields using the accessors, so they're properly Unicode encoded.
        out.write("BEGIN:VCARD\nVERSION:3.0\n")
        out.write("FN:%s\n" % self.Title())
        out.write("N:%s;%s\n" % (self.getLastName(), self.getFirstName()))
        out.write(foldLine("TITLE:%s\n" % '\\n'.join(self.getJobTitles())))
        out.write(foldLine("ADR;TYPE=dom,postal,parcel,work:;;%s;%s;%s;%s\n" % (self.getOfficeAddress().replace('\r\n','\\n'), self.getOfficeCity(), self.getOfficeState(), self.getOfficePostalCode())))
        out.write("TEL;WORK:%s\n" % self.getOfficePhone())
        out.write("EMAIL;TYPE=internet:%s\n" % self.getEmail())
        
        #Add the Person page to the list of URLs
        urls = list(self.getWebsites())
        urls.append(self.absolute_url())
        for url in urls:
            out.write(foldLine("URL:%s\n" % url))
        if self.getImage():
            encData = self.image_thumb.data.encode('base-64')
            # indent the data block:
            indentedData = '\n  '.join(encData.strip().split('\n'))
            out.write("PHOTO;ENCODING=BASE64;TYPE=JPEG:\n  %s\n" % indentedData)
        out.write("REV:%s\n" % DateTime(self.ModificationDate()).ISO8601())
        out.write("PRODID:WebLion Faculty/Staff Directory\nEND:VCARD")
        return n2rn(out.getvalue())
    
    security.declareProtected(View, 'getSortableName')
    def getSortableName(self):
        """
        Return a tuple of the person's name. For sorting purposes
        Return them as lowercase so that names like 'von Whatever' sort properly
        """
        return (self.lastName.lower(), self.firstName.lower())
    
    security.declareProtected(View, 'Title')
    def Title(self):
        """Return the Title as firstName middleName(when available) lastName, suffix(when available)"""
        try:
            # Get the fields using the accessors, so they're properly Unicode encoded.
            # We also can't use the %s method of string concatentation for the same reason.
            # Is there another way to manage this?
            fn = self.getFirstName()
            ln = self.getLastName()
        except AttributeError:
            return u"new person" # YTF doesn't this display on the New Person page?  # Couldn't call superclass's Title() for some unknown reason
        
        if self.getMiddleName():
            mn = " " + self.getMiddleName() + " "
        else:
            mn = " "
        
        t = fn + mn + ln
        if self.getSuffix():
            t = t + ", " + self.getSuffix()
        
        return t
    
    security.declarePrivate('_classificationReferences')
    def _classificationReferences(self):
        """Return a list of Classifications this Person can be referenced to."""
        return [(c.UID, safe_unicode(c.Title)) for c in self.aq_parent.getFolderContents({'portal_type': 'FSDClassification'})]
    
    security.declarePrivate('_availableEditors')
    def _availableEditors(self):
        """ Return a list of the available WYSIWYG editors for the site. """
        props = getToolByName(self, 'portal_properties')
        editors = [('', 'Use site default')] + [
                   (e, e) for e in props['site_properties'].available_editors
                  ]
        return editors
    
    security.declarePrivate('_availableLanguages')
    def _availableLanguages(self):
        """ Return a list of the available languages for the site. """
        props = getToolByName(self, 'portal_properties')
        return props.availableLanguages()
    
    security.declarePrivate('_skinSelections')
    def _skinSelections(self):
        """ Return a list of the available skins for the site. """
        skins = getToolByName(self, 'portal_skins')
        return skins.getSkinSelections()
    
    security.declareProtected(View, 'getCourses')
    def getCourses(self):
        """Return a listing of Courses contained by this Person."""
        portal_catalog = getToolByName(self, 'portal_catalog')
        return portal_catalog(path='/'.join(self.getPhysicalPath()), portal_type='FSDCourse', depth=1, sort_on="getObjPositionInParent")
    
    security.declareProtected(View, 'getClassificationNames')
    def getClassificationNames(self):
        """ Returns a list of the titles of the classifications attached to this person.
            Mainly used for pretty-looking metadata in SmartFolder tables.
        """
        cList = [(getObjPositionInParent(c)() + 1, c.Title()) for c in self.getClassifications()]
        cList.sort()
        return [c[-1] for c in cList]
    
    security.declareProtected(View, 'getSpecialtyTree')
    def getSpecialtyTree(self):
        """Return a tree-shaped dict of catalog brains of this person's specialties. The topmost level of the tree consists of SpecialtiesFolders; the remainder, of Specialties.
        
        The format of the dict is a superset of what buildFolderTree() returns (see its docstring for details). Consequently you can use a recursive macro similar to portlet_navtree_macro to render the results.
        
        Even if a person is mapped to a specialty but not to a superspecialty of it, the superspecialty will be returned. However, it will lack a 'reference' key, where explicitly mapped specialties will have one set to the reference from the Person to the Specialty. (All SpecialtiesFolders also lack 'reference' keys.) Thus, the template author can decide whether to consider people to implicitly belong to superspecialties of their explicitly mapped specialties, simply by deciding how to present the results.
        """
        def buildSpecialtiesFolderTree():
            """Return a buildFolderTree-style tree representing every SpecialtiesFolder and its descendents.
            
            More specifically, do a buildFolderTree for each SpecialtiesFolder, then merge the results into one big tree.
            """
            portal_catalog = getToolByName(self, 'portal_catalog')
            tree = {'children': []}
            for specialtiesFolder in portal_catalog(portal_type='FSDSpecialtiesFolder'):
                subtree = buildFolderTree(self, query={'path': {'query': specialtiesFolder.getPath()}, 'portal_type': 'FSDSpecialty'})
                subtree['currentItem'] = False
                subtree['currentParent'] = False
                subtree['item'] = specialtiesFolder
                subtree['depth'] = 0  # Let's see if that drives the stylesheets crazy. Otherwise, I'm going to have to increment the 'depth' keys in the whole rest of the tree.
                tree['children'].append(subtree)
            return tree
        
        # Walk the tree, killing everything not in reffedUids, except for the ancestors of reffed things.
        reffedUids = dict([(ref.targetUID, ref) for ref in getToolByName(self, 'reference_catalog').getReferences(self, relationship='people_specialties')])
        def pruneUnreffed(tree):
            """Prune all subtrees from `tree` where no descendent is in `reffedUids`. Return whether `tree` itself should be pruned off. While we're at it, add 'reference' keys."""
            keptChildren = []
            for child in tree['children']:
                if not pruneUnreffed(child):  # If that child shouldn't be completely pruned away,
                    keptChildren.append(child)  # keep it.
            tree['children'] = keptChildren
            
            if 'item' in tree:  # 'item' is not in the root node.
                try:
                    ref = reffedUids.get(tree['item'].UID)
                except TypeError:
                    # Catch the 'unhashable type' error we're getting in rare cases (seems to be mostly on uninstall/reinstall when catalog reindexing goes awry).
                    ref = reffedUids.get(tree['item'].getObject().UID())
                if ref:
                    tree['reference'] = ref
                    return False  # I don't care if you pruned all my children off. I myself am reffed, so I'm staying.
            return not keptChildren  # My children are the only thing keeping me here. Prune me if there aren't any. (Sounds so dramatic, doesn't it?)
        
        tree = buildSpecialtiesFolderTree()
        pruneUnreffed(tree)
        return tree
    
    security.declareProtected(View, 'getSpecialties')
    def getSpecialties(self):
        """Return an iterable of tuples representing the specialties explicitly attached to this person. The first item of the tuple is a catalog brain of a specialty; the second, the reference pointing from the Person to the Specialty.
        
        Results are ordered by the position of the specialties in their containers (SpecialtiesFolders or other Specialties) and by the order of SpecialtiesFolders themselves if there is more than one.
        
        To get a Specialties object from a result, call result.getTargetObject(). To get a SpecialtyInformation object, call result.getContentObject().
        """
        items = []
        def depthFirst(tree):
            """Append, in depth-first pre order, a tuple of ('item' value, 'reference' value) from `tree` for every node that has a 'reference' value."""
            if 'reference' in tree:
                items.append((tree['item'], tree['reference']))  # There's always an 'item' key where there's a 'reference' key. How can you have a reference if there's no item to reference?
            for child in tree['children']:
                depthFirst(child)
        depthFirst(self.getSpecialtyTree())
        return items
    
    security.declareProtected(View, 'getSpecialtyNames')
    def getSpecialtyNames(self):
        """Return a list of the titles of the specialties explicitly attached to this person.
        
        Results are ordered as in getSpecialties().
        
        Mainly used for pretty-looking metadata in SmartFolder tables.
        """
        return [x.Title for x, _ in self.getSpecialties()]
    
    security.declareProtected(View, 'getResearchTopics')
    def getResearchTopics(self):
        """Return a list of the research topics of the specialties explicitly attached to this person.
        
        Results are ordered as in getSpecialties(). Specialties whose references have no content object (which doesn't happen) or where the content object has an empty research topic are omitted.
        
        Mainly used for pretty-looking metadata in SmartFolder tables.
        """
        topics = []
        for _, ref in self.getSpecialties():
            refContent = ref.getContentObject()  # TODO: probably slow: wakes up all those SpecialtyInformation objects
            if refContent:  # This is usually true, because reference-dwelling objects are always created when the reference is created. However, it's false sometimes; run testSpecialties for an example.
                researchTopic = refContent.getResearchTopic()
                if researchTopic:
                    topics.append(researchTopic)
        return topics
    
    security.declareProtected(View, 'getDepartmentNames')
    def getDepartmentNames(self):
        """ Returns a list of the titles of the departments attached to this person.
            Mainly used for pretty-looking metadata in SmartFolder tables. Returns an
            alphabetically-sorted list since Departments can be located anywhere within the site,
            which makes using any other sort order somewhat problematic.
        """
        dList = [d.Title() for d in self.getDepartments()]
        dList.sort()
        return dList
    
    security.declareProtected(View, 'getCommitteeNames')
    def getCommitteeNames(self):
        """ Returns a list of the titles of the committees attached to this person.
            Mainly used for pretty-looking metadata in SmartFolder tables. Returns an
            alphabetically-sorted list since Committees can be located throughout the site,
            which makes using any other sort order somewhat problematic.
        """
        dList = [d.Title() for d in self.getCommittees()]
        dList.sort()
        return dList
    
    security.declareProtected(ModifyPortalContent, 'pre_edit_setup')
    def pre_edit_setup(self):
        """ Some schema tweaking that needs to happen before viewing the edit page.
        """
        
        fsd_tool = getToolByName(self,TOOLNAME)
        if (fsd_tool.getPhoneNumberRegex()):
            self.schema['officePhone'].widget.description = u"Example: %s" % fsd_tool.getPhoneNumberDescription()
        if (fsd_tool.getIdLabel()):
            self.schema['id'].widget.label = u"%s" % fsd_tool.getIdLabel()

        # Make sure the default for the editor field is the same as the site defaut. No idea why this isn't being handled properly.
        memberProps = getToolByName(self, 'portal_memberdata')
        self.schema['userpref_wysiwyg_editor'].default = memberProps.wysiwyg_editor
        
        return self.base_edit()
    
    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Pass along the 'tag' method to the Person's image."""
        return self.getWrappedField('image').tag(self, **kwargs)
    
    security.declareProtected(View, 'getImageOfSize')
    def getImageOfSize(self, height, width, **kwargs):
        """Return the person's image sized to the given dimensions."""
        return self.getWrappedField('image').tag(self, width=width, height=height, **kwargs)
    
    security.declareProtected(View, 'getScaledImageByWidth')
    def getScaledImageByWidth(self, preferredWidth, **kwargs):
        """Return the person's image sized to the given width and a height scaled according to the original image ratio. Fail nicely, returning no image tag. This seems to occur when TIFF images are used."""
        if not (self.image.height or self.image.width):
            logger.error("There was an error resizing the image for person %s" % self)
            return ''
        hwratio = float(self.image.height)/float(self.image.width)
        calcHeight = int(preferredWidth * hwratio)
        return self.getImageOfSize(calcHeight, preferredWidth, **kwargs)
    
    security.declareProtected(ModifyPortalContent, 'setImage')
    def setImage(self, value, **kwargs):
        field = self.getField('image')
        
        # If the image exists in portal memberdata's portraits folder, delete it
        md = getToolByName(self, 'portal_memberdata')
        if md.portraits.has_key(self.id):
            md.portraits._delObject(self.id)
        
        # Assign the image to the field
        field.set(self, value)
        
        # If there is an image value (not the empty string that seems to get sent on object creation)
        # and it's not a delete command, create a member portrait
        if value and value != 'DELETE_IMAGE':
            # Add the new portrait
            #md.portraits._setObject(id=self.id, object=self.getImage())
            raw_image = StringIO()
            raw_image.write( str(self.getRawImage().data) )
            raw_image.seek(0)
            md.portraits._setObject(id=self.id, object=Image(id=self.id, file=raw_image, title=''))
            raw_image.close()

    
    security.declareProtected(SetOwnPassword, 'setPassword')
    def setPassword(self, value):
        """"""
        if value:
            annotations = IAnnotations(self)
            annotations[PASSWORD_KEY] = sha(value).digest()
    
    security.declareProtected(SetOwnPassword, 'setConfirmPassword')
    def setConfirmPassword(self, value):
        """"""
        # Do nothing - this value is used for verification only
        pass

    
    security.declarePrivate('validate_id')
    def validate_id(self, value):
        """
        """
        # Ensure the ID is unique in this folder:
        if value != self.getId():
            parent = aq_parent(aq_inner(self))
            if value in parent.objectIds():
                return _(u"An object with ID '%s' already exists in this folder") % value
        
        # Make sure the ID fits the regex defined in the configuration:
        fsd_tool = getToolByName(self, TOOLNAME)
        regexString = fsd_tool.getIdRegex()
        if not re.match(regexString, value):
            return fsd_tool.getIdRegexErrorMessage()
    
    security.declarePrivate('validate_officePhone')
    def validate_officePhone(self, value=None):
        """ Make sure the phone number fits the regex defined in the configuration. """
        if value:
            fsd_tool = getToolByName(self, TOOLNAME)
            regexString = fsd_tool.getPhoneNumberRegex()
            if regexString and not re.match(regexString, value):
                return _(u"Please provide the phone number in the format %s") % fsd_tool.getPhoneNumberDescription()

    
    security.declarePrivate('post_validate')
    def post_validate(self, REQUEST, errors):
        form = REQUEST.form
        if form.has_key('password') or form.has_key('confirmPassword'):
            password = form.get('password', None)
            confirm = form.get('confirmPassword', None)
            
            annotations = IAnnotations(self)
            passwordDigest = annotations.get(PASSWORD_KEY, None)
            
            if not passwordDigest:
                if not password and not confirm:
                    errors['password'] = _(u'An initial password must be set')
                    return
            if password or confirm:
                if password != confirm:
                    errors['password'] = errors['confirmPassword'] = _(u'Passwords do not match')
                    
    ###
    # Methods to limit the referenceBrowserWidget start directory and search results    
    # security.declareProtected(ModifyPortalContent, '_get_parent_fsd_path')
    # def _get_parent_fsd_path(self):
    #     """ wrap the utility method so we can use it in the context of an AT Schema declaration
    #     """
    #     parent = aq_parent(aq_inner(self))
    #     if IFacultyStaffDirectory.providedBy(parent):
    #         # we should pretty much always expect this to be true.  People can't be added anywhere but 
    #         #   inside an FSD, right at the FSD root, right?  Is this a safe assumption?
    #         return parent.absolute_url_path()
    #     else:
    #         return '/'
    
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
            
    security.declareProtected(ModifyPortalContent, '_limit_rbw_search_params')
    def _limit_rbw_search_params(self, portal_type="FSDPerson", sort_on="sortable_title"):
        """ return a query dictionary to limit the search parameters for a reference browser
            widget query.  Use as basis for more specific versions below
        """
        path = self._get_parent_fsd_path(relative=False)
        return {'portal_type': portal_type,
                'sort_on': sort_on,
                'path': {'query': path}}

    security.declareProtected(ModifyPortalContent, '_search_people_in_this_fsd')
    def _search_people_in_this_fsd(self):
        """ search only parent FSD for only people
        """
        return self._limit_rbw_search_params(portal_type="FSDPerson")

    security.declareProtected(ModifyPortalContent, '_search_departments_in_this_fsd')
    def _search_departments_in_this_fsd(self):
        """ search only parent FSD for only departments
        """
        return self._limit_rbw_search_params(portal_type="FSDDepartment")

    security.declareProtected(ModifyPortalContent, '_search_committees_in_this_fsd')
    def _search_committees_in_this_fsd(self):
        """ search only parent FSD for only committees
        """
        return self._limit_rbw_search_params(portal_type="FSDCommittee")

    security.declareProtected(ModifyPortalContent, '_search_specialties_in_this_fsd')
    def _search_specialties_in_this_fsd(self):
        """ search only parent FSD for only specialties
        """
        return self._limit_rbw_search_params(portal_type="FSDSpecialty")


# Implementing IMultiPageSchema forces the edit template to render in the more Plone 2.5-ish manner,
# with actual links at the top of the page instead of Javascript tabs. This allows us to direct people
# immediately to a specific fieldset with a ?fieldset=somethingorother query string. Plus, it also
# gives the next/previous links at the bottom of the form.
classImplements(Person, IMultiPageSchema)

registerType(Person, PROJECTNAME)  # generates accessor and mutators, among other things
