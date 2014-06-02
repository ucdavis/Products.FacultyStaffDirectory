from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

class FSDNonInstallable(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [u'Products.FacultyStaffDirectory:uninstall']
