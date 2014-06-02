# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class IFacultyStaffDirectoryTool(Interface):
    """The FacultyStaffDirectoryTool
    """

class IFacultyStaffDirectoryToolModifiedEvent(Interface):
    """An event fired when the facultystaffdirectory_tool is saved.
    """
