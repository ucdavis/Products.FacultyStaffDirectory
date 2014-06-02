# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute
from zope import schema

class IFacultyStaffDirectoryContent(Interface):
    """Marker interface for FacultyStaffDirectory content objects"""
    
class IFacultyStaffDirectory(IFacultyStaffDirectoryContent):
    """A FacultyStaffDirectory.
    """
                               
class IFacultyStaffDirectoryModifiedEvent(Interface):
    """An event fired when an FacultyStaffDirectory object is saved.
    """
    
    context = Attribute("The content object that was saved.")
    
class IFacultyStaffDirectoryAddable(Interface):
    """A content type to be set as an addable_type within a FacultyStaffDirectory.
    """
