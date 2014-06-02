# -*- coding: utf-8 -*-
import os.path
import logging
from App.Common import package_home
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.FacultyStaffDirectory.config import product_globals as GLOBALS
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL

linkableKupuTypes = ['FSDPerson', 'FSDCourse', 'FSDClassification', 'FSDDepartment', 'FSDCommittee', 'FSDCommitteesFolder', 'FSDSpecialty', 'FSDSpecialtiesFolder']
mediaKupuTypes = ['FSDPerson']
collectionKupuTypes = ['FSDFacultyStaffDirectory']
logger = logging.getLogger("Products.FacultyStaffDirectory")

def addKupuResource(portal, resourceType, portalType):
    kupu = getToolByName(portal, 'kupu_library_tool')
    resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
    if portalType not in resourceList:
        resourceList.append(portalType)
        kupu.addResourceType(resourceType,tuple(resourceList))

def removeKupuResource(portal, resourceType, portalType):
    kupu = getToolByName(portal, 'kupu_library_tool')
    resourceList = list(kupu.getPortalTypesForResourceType(resourceType))
    if portalType in resourceList:
        resourceList.remove(portalType)
        kupu.addResourceType(resourceType,tuple(resourceList))

def installKupuResources(context):
    """ Add kupu resource types. Kupu's GS handling is broken/nonexistant."""
    if context.readDataFile('installKupuResources.txt') is None:
        return
    portal = context.getSite()
    quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    if quickinstaller.isProductInstalled('kupu'):
        for type in linkableKupuTypes:
            addKupuResource(portal, 'linkable', type)
        for type in mediaKupuTypes:
            addKupuResource(portal, 'mediaobject', type)
        for type in collectionKupuTypes:
            addKupuResource(portal, 'collection', type)

def installRelationsRules(context):
    if context.readDataFile('installRelationsRules.txt') is None:
        return
    portal = context.getSite()
    relations_tool = getToolByName(portal,'relations_library')
    xmlpath = os.path.join(package_home(GLOBALS),'relations.xml')
    f = open(xmlpath)
    xml = f.read()
    f.close()
    relations_tool.importXML(xml)

def uninstallKupuResources(context):
    """Remove Kupu customizations"""
    if context.readDataFile('uninstallKupuResources.txt') is None:
        return
    portal = context.getSite()
    quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    if quickinstaller.isProductInstalled('kupu'):
        for type in linkableKupuTypes:
            removeKupuResource(portal, 'linkable', type)
        for type in mediaKupuTypes:
            removeKupuResource(portal, 'mediaobject', type)
        for type in collectionKupuTypes:
            removeKupuResource(portal, 'collection', type)

TYPES_TO_VERSION = ('FSDPerson', 'FSDCommittee', 'FSDSpecialty')
def installVersionedTypes(context):
    if context.readDataFile('installVersionedTypes.txt') is None:
        return
    try:
        from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
    except ImportError:
        # Use repositorytool.xml instead (Plone 4.1 and above)
        pass
    else:
        portal = context.getSite()
        portal_repository = getToolByName(portal, 'portal_repository')
        versionable_types = list(portal_repository.getVersionableContentTypes())
        for type_id in TYPES_TO_VERSION:
            if type_id not in versionable_types:
                # use append() to make sure we don't overwrite any
                # content-types which may already be under version control
                versionable_types.append(type_id)
                for policy_id in DEFAULT_POLICIES:
                    portal_repository.addPolicyForContentType(type_id, policy_id)
        portal_repository.setVersionableContentTypes(versionable_types)

def uninstallNavTreeSettings(context):
    """Remove FSD classes from NavTree_properties since this isn't supported
       via GS."""
      
    if context.readDataFile('uninstallNavTreeSettings.txt') is None:
        return
    portal = context.getSite()
    pprops = getToolByName(portal, 'portal_properties')
    navprops = pprops.navtree_properties
    mtntl = list(navprops.metaTypesNotToList)
    for mType in ['FSDCourse', 'FSDPerson', 'FSDFacultyStaffDirectoryTool']:
        if mType in list(navprops.metaTypesNotToList):
            mtntl.remove(mType)
    navprops._p_changed=1
    navprops.metaTypesNotToList = tuple(mtntl)


def uninstallConfiglet(context):
    """ Remove the FSD control panel item"""

    if context.readDataFile('uninstallNavTreeSettings.txt') is None:
        return
    portal = context.getSite()
    cp = getToolByName(portal, 'portal_controlpanel')
    cp.unregisterApplication('FacultyStaffDirectory')

def unindexFSDTool(context):
    """ Unindex the FSD tool so it doesn't show up in folder contents"""
    if context.readDataFile('unindexFSDTool.txt') is None:
        return
    portal = context.getSite()
    fsdTool = getToolByName(portal, 'facultystaffdirectory_tool')
    fsdTool.unindexObject()

originalProfileActionId = "MemberPrefs"
newProfileActionId = "fsdMemberPrefs"
def hideMemberPrefs(context):
       # Fixing the 'MemberPrefs' action
       # massage the portal_controlpanel tool to make MemberPrefs invisible
       if context.readDataFile('hideMemberPrefs.txt') is None:
           return
       portal = context.getSite()
       cp = getToolByName(portal, 'portal_controlpanel')
       currentActions = cp.listActions()
       for action in currentActions:
           if action.id == originalProfileActionId:
               action.visible = False

def restoreMemberPrefs(context):
    """Massage the portal_controlpanel tool to make MemberPrefs visible
    at the same time, delete the action we created via GS Profile"""
    if context.readDataFile('restoreMemberPrefs.txt') is None:
        return
    portal = context.getSite()
    cp = getToolByName(portal, 'portal_controlpanel')
    currentActions = cp.listActions()
    index = 0
    for action in currentActions:
        if action.id == originalProfileActionId:
            action.visible = True
        if action.id == newProfileActionId:
            cp.deleteActions([index])
        index += 1

def reindexFSDObjects(context):
    """Update indexes relevant to FSD objects"""
    if context.readDataFile('reindexFSDObjects.txt') is None:
        return
    portal = context.getSite()
    catalog = getToolByName(portal, 'portal_catalog')

    INDEX_LIST = ['getSortableName', 'getRawClassifications',
                  'getRawSpecialties', 'getRawCommittees',
                  'getRawDepartments', 'getRawPeople']
    for index in INDEX_LIST:
        catalog.reindexIndex(index, None)
    membrane = getToolByName(portal, MEMBRANE_TOOL)
    membrane.refreshCatalog()

# ################## #
#   sample-content   #
# ################## #

def _getOrCreateObjectByType(id, type, container, **kwargs):
    """Gets the object by the given id and container. If the object doesn't
    exist, it will use the id, container and type as well as any keyword
    to create the object."""
    if id not in container:
        obj = _createObjectByType(type, container, id=id, **kwargs)
        info_msg = "Added a directory (%s)."
    else:
        obj = container[id]
        info_msg = "Using existing directory (%s)."
    logger.info(info_msg % obj)
    return obj

def _transitionWorkflowIfNecessary(obj, transition, end_state):
    """Transition the workflow to the given transition if it is not already
    in that state. Normally, calling portal_workflow.doActionFor will raise
    a WorkflowException if the object is already in the given state. This
    function is used to encapsulate the wrapping logic."""
    portal_workflow = getToolByName(obj, 'portal_workflow')
    if not portal_workflow.getInfoFor(obj, 'review_state') == end_state:
        portal_workflow.doActionFor(obj, transition)

def addSampleContent(portal):
    logger.info("Starting to add %s sample-content." % GLOBALS['PROJECTNAME'])
    # Gather up all our tools.
    portal_workflow = getToolByName(portal, 'portal_workflow')
    id_to_title = lambda id: id.replace('-', ' ').title()
    # Add a directory.
    directory_id = 'directory'
    directory = _getOrCreateObjectByType(
        directory_id,
        'FSDFacultyStaffDirectory', portal,
        title="Faculty and Staff Directory",
        )
    _transitionWorkflowIfNecessary(directory, 'publish', 'published')

    # Add classifications.
    classifications = {}
    classification_ids = ('faculty', 'staff', 'graduate-students',)
    for classification_id in classification_ids:
        classification = _getOrCreateObjectByType(
            classification_id,
            'FSDClassification', directory,
            title=id_to_title(classification_id),
            )
        # NOTE classifications are defaulted to an active state,
        #      therefore no workflow transition is necessary here.
        # Capture classification for later use with people.
        classifications[classification_id] = classification

    # Add departments.
    departments = {}
    department_ids = ('biological-research', 'mechanical-engineering',
                      'human-resources', 'information-technology-services',
                      )
    for department_id in department_ids:
        department = _getOrCreateObjectByType(
            department_id,
            'FSDDepartment', directory,
            title=id_to_title(department_id),
            )
        # Capture departments for later use with people.
        departments[department_id] = department

    # Add a committees container.
    committees_container_id = 'committees'
    committees_container = _getOrCreateObjectByType(
        committees_container_id,
        'FSDCommitteesFolder', directory,
        title=id_to_title(committees_container_id),
        )
    _transitionWorkflowIfNecessary(committees_container,
                                   'publish', 'published')
    # Add committees to the committee container.
    committees = {}
    committee_ids = ('climate-and-diversity', 'technology-roundtable',)
    for committee_id in committee_ids:
        committee = _getOrCreateObjectByType(
            committee_id,
            'FSDCommittee', committees_container,
            title=id_to_title(committee_id),
            )
        # Capture committee for later use with people.
        committees[committee_id] = committee

    # Add a specialties folder.
    specialties_container_id = 'specialties'
    specialties_container = _getOrCreateObjectByType(
        specialties_container_id,
        'FSDSpecialtiesFolder', directory,
        title=id_to_title(specialties_container_id),
        )
    _transitionWorkflowIfNecessary(specialties_container,
                                   'publish', 'published')
    # Add specialties to the specialties container.
    specialties = {}
    specialty_ids = ('home-brewer', 'snobbery', 'sql-junky', 'oop-guru',)
    for specialty_id in specialty_ids:
        specialty = _getOrCreateObjectByType(
            specialty_id,
            'FSDSpecialty', specialties_container,
            title=id_to_title(specialty_id),
            )
        _transitionWorkflowIfNecessary(specialty, 'publish', 'published')
        # Capture specialty for later use with people.
        specialties[specialty_id] = specialty

    # Person Groupings functions...
    def abc123_person_groupings(person):
        # Specialties 
        specialties = dict([(b.getId, ref.getContentObject()) for b, ref in person.getSpecialties()])
        specialties['home-brewer'].setResearchTopic("<p>Analyzing the Yeast between Thor's Toes</p>")
        specialties['snobbery'].setResearchTopic("<p>Snubbing the neighbors</p>")
        # Departments
        departments = dict([(dept.getId(), dept) for dept in person.getDepartments()])
        departments['biological-research'].getMembershipInformation(person).setPosition('Schmoozer')
        # Committees
        committees = dict([(c.getId(), c) for c in person.getCommittees()])
        committees['climate-and-diversity'].getMembershipInformation(person).setPosition('Big Cheese')        
    def def456_person_groupings(person):
        directory = person.getParentNode()  # Assumes the parent is the directory.
        # Assign def456 as abc123's assistant.
        abc123 = directory.abc123
        abc123.setAssistants([person.UID()])

    # Add people to the directory.
    # A three part tuple containing an id, dictionary of person information,
    # and a person grouping callable.
    people_info = (
        ('abc123',
         dict(firstName='Abe', middleName='Bob', lastName='Crumpt',
              suffix='Ph.D. EPT',
              password='abe',
              email='abe@example.com',
              classifications=(classifications['faculty'].UID(),),
              committees=(committees['climate-and-diversity'].UID(),),
              departments=(departments['biological-research'].UID(),),
              specialties=(specialties['home-brewer'].UID(),
                           specialties['snobbery'].UID(),
                           ),
              ),
         abc123_person_groupings,
         ),
        ('def456',
         dict(firstName='Dublin', middleName='Ender', lastName='Fondu',
              suffix='B.C.',
              password='dublin',
              email='dublin@example.com',
              classifications=(classifications['staff'].UID(),),
              ),
         def456_person_groupings,
         ),
        ('ghi789',
         dict(firstName=u'G\'oldë', middleName=u'Hatterǩ', lastName='Itoppi',
              password='itoppi',
              email='ghi789@example.com',
              classifications=(classifications['graduate-students'].UID(),),
              ),
         lambda p: None,
         ),
        # Arabic Name translation done by http://www.languages-of-the-world.us/YourNameIn/Arabic.html
        ('jkl110',
         dict(firstName=u'تخطط', middleName=u'نخا', lastName=u'جي',  # Ji Noa Touu
              password='110jkl',
              email='jkl110@example.com',
              classifications=(classifications['faculty'].UID(),),
              ),
         lambda p: None,
         ),
        ('mno111',
         dict(firstName=u'Mi', middleName=u'Nylon', lastName='O\'catta',
              password='mi',
              email='mi@example.com',
              classifications=(classifications['faculty'].UID(),
                               classifications['staff'].UID(),
                               ),
              committees=[c.UID() for c in committees.values()],
              departments=(departments['human-resources'].UID(),),
              ),
         lambda p: None,
         ),
        )
    for person_id, person_info, person_groupings_func in people_info:
        person = _getOrCreateObjectByType(
            person_id,
            'FSDPerson', directory,
            **person_info)
        # NOTE There is no reason to transition workflow on a person.
        #      By default people are initialized to a visable state.
        person_groupings_func(person)

    logger.info("Finished adding %s sample content." % GLOBALS['PROJECTNAME'])

def importSampleContent(context):
    # Only run step if a flag file is present
    if context.readDataFile('Products.FacultyStaffDirectory-sample-content.txt') is None:
        return
    addSampleContent(context.getSite())
