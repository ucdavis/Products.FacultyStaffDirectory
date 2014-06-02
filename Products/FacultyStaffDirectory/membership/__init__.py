"""Membership adapters for FacultyStaffDirectory
"""
import person
import facultystaffdirectory
import committee
import classification
import department


def not_a_user_object(obj):
    """
    Unfortunately IMembraneUserProperties inherits from IMembraneUserObject
    causing group property providers to also be registered as user providers.
    Register this as a more specific adapter on affected classes.
    """
    return None
