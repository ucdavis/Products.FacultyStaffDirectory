import logging

from Products.CMFCore.utils import getToolByName
from plone.app.workflow.remap import remap_workflow


def from_2_x_to_3_0(context):
    log = logging.getLogger('FacultyStaffDirectory')
    
    context.runImportStepFromProfile('profile-Products.FacultyStaffDirectory:default','workflow')
    try:
        remap_workflow(context,
                       ('FSDFacultyStaffDirectory',),
                       ('fsd_directory_workflow',),
                       {})
    except Exception, message:
        log.error(message)
        raise

    # log it
    log = logging.getLogger("FacultyStaffDirectory")
    log.info("Upgraded version 2 to version 3.0b1")

def from_3_0b1_to_3_0b3(context):
    log = logging.getLogger("FacultyStaffDirectory")
    membrane_upgrade = context.upgradeInfo('membrane')
    if membrane_upgrade['required'] == True and membrane_upgrade['available'] == True:
        log.info("Upgrading membrane")
        context.upgradeProduct('membrane')
        
    context.runImportStepFromProfile('profile-Products.FacultyStaffDirectory:default','FacultyStaffDirectory-reindexFSDObjects')
    log.info("Upgraded version 3.0b1 to version 3.0b3")
    
def from_3_0b3_to_3_0b4(context):
    log = logging.getLogger("FacultyStaffDirectory")
    registry = context.getImportStepRegistry()
    
    # drop legacy import steps, if they exist
    LEGACY_IMPORT_STEPS = [u'upgrade_2_to_3', u'hideMemberPrefs', u'installKupuResources', u'installVersionedTypes', u'installRelationsRules', u'unindexFSDTool']
    for step in LEGACY_IMPORT_STEPS:
        if step in registry.listSteps() and registry.getStepMetadata(step)['handler'] == ('Products.FacultyStaffDirectory.setuphandlers.%s' % step):
            registry.unregisterStep(step)        
            log.info("Unregistered import step: %s" % step)

    context.runImportStepFromProfile('profile-Products.FacultyStaffDirectory:default','typeinfo')
    
    log.info("Upgraded version 3.0b3 to version 3.0b4")

def from_3_0_to_3_0_1(context):
    log = logging.getLogger("FacultyStaffDirectory")

    tool = getToolByName(context, 'facultystaffdirectory_tool')
    states = list(tool.getActiveMembraneStates())
    states.append('published')
    tool.setActiveMembraneStates(tuple(states))
    
    log.info("Upgraded version 3.0 to version 3.0.1")


def from_3_0_1_to_3_1(context):
    log = logging.getLogger("FacultyStaffDirectory")

    context.runImportStepFromProfile('profile-Products.FacultyStaffDirectory:default','typeinfo')
    try:
        context.runImportStepFromProfile('profile-Products.FacultyStaffDirectory:default','repositorytool')
    except ValueError:
        context.runImportStepFromProfile('profile-Products.FacultyStaffDirectory:default','FacultyStaffDirectory-installVersionedTypes')
    
    # Remove the vCard action
    ttool = getToolByName(context, 'portal_types')
    personType = ttool['FSDPerson']
    actions = personType.listActions()
    try:
        vcardindex = actions.index(personType.getActionObject('document_actions/vcard'))
    except ValueError:
        pass
    else:
        personType.deleteActions([vcardindex])
    
    log.info("Upgraded version 3.0.1 to version 3.1")
    