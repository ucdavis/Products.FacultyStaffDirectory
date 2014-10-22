.. contents::

Description
===========

FacultyStaffDirectory is a personnel directory, a provider of shared workspaces
for committees, a way of keeping track of people's areas of expertise, a floor
wax, and a dessert topping. It integrates with Plone's users and groups
infrastructure and supports an extensibility framework for custom requirements.


Dependencies
============
    
FacultyStaffDirectory depends on Products.membrane and Products.Relations


Installation
============

FacultyStaffDirectory 3 requires Plone 4.0 or greater.

1.  Add the following to buildout.cfg

::

    [buildout]
    eggs =
    . . .(other eggs). . .
        Products.FacultyStaffDirectory

2.  Re-run buildout (typically 'bin/buildout').

3.  Restart Zope (typically 'bin/instance restart').

4.  Install the FacultyStaffDirectory product using
    portal_quickinstaller or the Plone Add/Remove Products tool
    under Site Setup. The necessary dependencies will install
    themselves automatically. (Membrane remains in the 'available'
    column, but is in fact installed.)


Upgrading
=========

From FacultyStaffDirectory 1.x
------------------------------

To upgrade from 1.x, first upgrade to a 2.x release thusly:

Use the migration script in the Extensions folder of
FacultyStaffDirectory. Follow the instructions inside
migrate1dot0to2dot0.py. To perform the migration under Plone
3, you'll need the `contentmigration product`_.

.. _contentmigration product: 
   http://svn.plone.org/svn/collective/Products.contentmigration

From FacultyStaffDirectory 2.x
------------------------------

To upgrade from 2.x to 3.0 use the "Upgrade" button on the 'Add-on Products'
page. (in Plone 4.0, this is called "Add-Ons").

**Be sure** to check the workflow and publication state of your Faculty/Staff
directory. It has probably been changed to 'private'.

If your Faculty/Staff directory was using a custom workflow, it is now in a new
workflow which comes with FacultyStaffDirectory 3.0. You'll need to change your
custom workflow to manage the "FacultyStaffDirectory: Provides Roles" permission
before you go back to it. Check out the 'fsd_directory_workflow' to see how it's
done.

Special Note for users upgrading to Plone 4:
--------------------------------------------

Because FacultyStaffDirectory 2.x is not compatible with Plone 4, you must first
upgrade FacultyStaffDirectory to version 3 then upgrade Plone.



Using FacultyStaffDirectory
===========================

Adding a Faculty/Staff Directory
--------------------------------

From the "add" dropdown menu in Plone, select "Faculty/Staff Directory". A
Faculty/Staff Directory will be created as well as several default items inside:

* Faculty (a Classification)

* Staff (a Classification)

* Graduate Students (a Classification)

* Committees (a Committees Folder, which can hold only Committees)

* Specialties (a Specialties Folder, which can hold only Specialties)

Any or all of these default items may be safely deleted as needed.

Working with your directory
---------------------------

FacultyStaffDirectory provides content types for creating and organizing details
of people. It has principally been developed for personnel directories in
educational institutions but can be repurposed for use in a variety of settings.

The core content type is Person. This has a variety of fields (email, telephone
number, job title, and so on). You can also easily add your own.

Out of the box, FacultyStaffDirectory offers 3 Classifications that can be
assigned to Person objects: Faculty, Staff and Graduate Student. If these don't
work for you, you can add your own Classifications (e.g. Administrators,
Technicians, Board Members, or whatever you like).

FacultyStaffDirectory also provides several content types for grouping people:
Departments, Specialties and Committees. If these labels don't make sense in
your organization, you can easily relabel them. In each case, the association
between the Person and the grouping (e.g. the Person-Specialty relationship) can
be given a description. So, for example, if Person Jane Doe is in the Artificial
Intelligence Specialty, you could give the Jane Doe-Artificial Intelligence
relationship a description (e.g. "Interested in the cultural impacts of machine
thinkers").

FacultyStaffDirectory can be configured so people added to the directory
automatically become Members of your Plone site and each person can edit his or
her own page. It also adds some new roles, to facilitate management of people.
For instance, the PersonnelManager role can create new Specialties and assign
people to them.

Membership integration
----------------------

Out of the box, FacultyStaffDirectory offers the following integration with
Plone users and groups:

The Faculty/Staff Directory itself acts as a group.
  All Person objectscreated in the Faculty/Staff Directory are automatically 
  considered members of this group. This group also provides the option of 
  assigning a global role to all Persons in the Directory. This option should be 
  handled with care. It is generally best to select only the 'Member' role, as 
  this is the most restrictive option.

Departments, Classifications and Committees act as groups.
  Global role assignment is not available for these
  content types, but the groups they define may be granted
  local roles throughout the Plone site.  For complex
  academic units, this can be a great time-saver, since
  personnel management can be tied closely to site
  security management.

Person objects act as users.
  The Faculty/Staff Directory configlet in Site Setup
  allows you to choose whether Person objects provide
  passwords for authentication. If you are using some
  other PAS plugin for authentication, such as PloneLDAP,
  WebServerAuth, PubcookiePAS or CAS4PAS, you will want to
  disable password provision so that authentication will
  cascade to these other systems.

Persons own their own profiles.
  Users defined by Person objects are automatically granted the
  Owner role locally for that object and its contents.  This
  allows users to add to and edit their own biographies, contact
  information, etc.  They also control sharing rights to their
  object and can thus allow assistants to edit content on their
  behalf without sharing their own passwords or user
  preferences.

My Folder action.
  The 'My Folder' action, found on the personal toolbar, is
  altered by the Faculty/Staff Directory product to take users
  defined by Person objects directly to them. Users defined
  through the standard Plone UI will be taken to the usual
  location (portal/Members/<userid>).  Likewise, the personal
  preferences link found in the personal toolbar and on the
  plone_memberprefs_panel or dashboard will take Person users to
  their Person objects.

Restrictions on group membership.
  Owners are not granted the rights to add or remove their
  Person object from Departments, Committees, Classifications
  and Specialties, since these collections are used as
  authorization groups. Instead, this right is reserved for site
  managers and for the newly-created 'Personnel Manager' role,
  installed with the Faculty/Staff Directory product. The
  Personnel Manager is likewise not granted access to the ZMI or
  to personal preferences for Persons. This allows for
  fine-grained separation of management concerns.

Configurable integration.
  Membership integration for Person, Department, Classification
  and Committee objects is configurable.  A switch to turn the    
  function on or off is in the Faculty/Staff Directory
  configuration panel in Site Setup.  It may be necessary to
  disable membership integration for Person objects in systems
  that have established user bases built on LDAP systems, for
  instance.

Configuring the product
-----------------------

Several global settings, such as phone number and user ID formats, can be
controlled through the Faculty/Staff Directory configuration panel within Site
Setup.

Extensibility

Because every organization has a few unique requirements, FacultyStaffDirectory
supports an extension mechanism based on the archetypes.schemaextender library.
Using it, you can write plugin products which add fields to or otherwise modify
our content types. For an example, see the FacultyStaffDirectoryExtender product
and `its readme`_.

.. _its readme:
   https://weblion.psu.edu/svn/weblion/weblion/Products.FacultyStaffDirectory/tags/3.0/src/Products/FacultyStaffDirectory/examples/FacultyStaffDirectoryExtender/README.txt.


Design Rationale & Thoughts
===========================

Why the push for just one Directory in a site? Why not just add people to Departments?
  The main thought behind this was that People could be members
  of multiple departments (i.e., faculty member John Smith
  teaches courses in both MSIS and Computer Science). So where
  do we put the Person object?  We'd like to refrain from making
  two Persons if possible, and the alternative of making a
  Department both a container and a referenced object could be
  nightmarish.

Why add membrane?
  We wanted a relatively simple way to let members modify their own
  profiles. With membrane, we get that right out of the box since that
  profile *is* the member. We also get nifty groups like "Faculty" and
  "Chemistry Department" and "Some Useless Committee".

How do I manage People across multiple Plone sites?
  We wish we knew. We suspect it will have something to do with LDAP.
  Suggestions?


Authorship
==========

This product was developed by the WebLion group at Penn State University.

membrane integration by Cris Ewing at the University of Washington.

Special thanks to Andreas Jung for his early testing, code contributions, and
reminding us that, yes, people do live outside the United States.


Support
=======

* Report bugs to support@weblion.psu.edu

* More documentation at the `WebLion wiki`_.

.. _weblion wiki: https://weblion.psu.edu/trac/weblion/wiki/FacultyStaffDirectory


* Contact us::

    WebLion Project Team
    Penn State University
    304 The 300 Building
    University Park, PA 16802
    support@weblion.psu.edu
    814-863-4574


License
=======

Copyright (c) 2006-2011 The Pennsylvania State University. WebLion is developed
and maintained by the WebLion Project Team, its partners, and members of the
Penn State Zope Users Group.

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA.
