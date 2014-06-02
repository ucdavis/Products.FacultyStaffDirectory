# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'
# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. This will be included
# in this file if found.

from Products.CMFCore.permissions import setDefaultRoles 
PROJECTNAME = "FacultyStaffDirectory"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'Person': 'FacultyStaffDirectory: Add or Remove People',
}

setDefaultRoles('FacultyStaffDirectory: Add or Remove People', ('Manager','Owner', 'Personnel Manager'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
DEPENDENCIES = ["Relations"]

# Dependend products - not quick-installed - used in testcase
PRODUCT_DEPENDENCIES = []

# membrane stuff, roles we don't want groups to be able to use
INVALID_ROLES = ['Manager', 'Owner', 'Anonymous', 'Authenticated', 'User Preferences Editor']
# Annotation key used for passwords
PASSWORD_KEY = 'fsd.employee.password'
# what is the name of the tool for this product?
TOOLNAME = 'facultystaffdirectory_tool' 
# what content types are available for membrane functionality?
MEMBRANE_ABLE_TYPES_VOCAB = [('FSDPerson','People'),('FSDDepartment','Departments'),('FSDClassification','Classifications'),('FSDCommittee','Committees'),]
MEMBRANE_ABLE_TYPES = ('FSDPerson','FSDDepartment','FSDClassification','FSDCommittee')
MEMBRANE_ACTIVE_STATES = ('published','active','hiddenactive',)

# content-types
ALLOWABLE_CONTENT_TYPES = ('text/plain', 'text/structured', 'text/html', 'application/msword', 'text/x-rst')

