from Products.CMFCore.utils import getToolByName

def uninstall(self, reinstall=False):
    if not reinstall:
        setup_tool = getToolByName(self, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.FacultyStaffDirectory:uninstall')
        registry = setup_tool.getImportStepRegistry()
        fsdSteps = [a['id'] for a in registry.listStepMetadata() if 'Products.FacultyStaffDirectory' in a['handler']]
        for step in fsdSteps:
            registry.unregisterStep(step)