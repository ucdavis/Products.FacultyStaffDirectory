localAdaptersAreSupported = True

def installExtenderGloballyIfLocallyIsNotSupported(extenderClass, name):
    """If we're on a version of Plone that doesn't support local adapters, make it so merely putting the extender in the Products folder activates it across on all Plone sites."""
    raise Exception("installExtenderGloballyIfLocallyIsNotSupported is no longer a supported way to install FacultyStaffDirectory extenders, please implement IBrowserLayerAwareExtender and install by registering a browser layer.")

def installExtender(portal, extenderClass, name, required=None, provided=None):
    """Register a schema extender with a Plone site."""
    raise Exception("installExtender is no longer a supported way to install FacultyStaffDirectory extenders, please implement IBrowserLayerAwareExtender and install by registering a browser layer.")

def uninstallExtender(portal, extenderClass, name, required=None, provided=None):
    """Unregister a schema extender so its effect is no longer seen on a particular Plone site."""
    sm = portal.getSiteManager()
    sm.unregisterAdapter(extenderClass, required=required, provided=provided, name=name)
    return "Removed the extender from the root of the Plone site."

def declareInstallRoutines(globals_, extenderClass, name):
    """Called from an extender's Install.py, makes the extender installable via the Add-on Products control panel if and only if we're on a version of Plone that support local adapters (Plone 3 or better).
    
    If you want to do additional stuff on installation or uninstallation (like installing skin layers), don't call this; do what you have to do, and call installExtender() and uninstallExtender() yourself.
    """
    def install(portal):
        installExtender(portal, extenderClass, name)
    globals_['install'] = install
    
    def uninstall(portal):
        uninstallExtender(portal, extenderClass, name)
    globals_['uninstall'] = uninstall
