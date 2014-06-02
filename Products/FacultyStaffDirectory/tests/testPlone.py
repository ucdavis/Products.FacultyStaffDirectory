# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

#
# Base TestCase for FacultyStaffDirectory
#

import code
from random import choice, sample

from Globals import package_home
from Products.PloneTestCase import PloneTestCase
from Testing import ZopeTestCase

from Products.FacultyStaffDirectory.config import PRODUCT_DEPENDENCIES, DEPENDENCIES
PACKAGE_HOME = package_home(globals())
    
# Add common dependencies
DEPENDENCIES.append('Archetypes')
PRODUCT_DEPENDENCIES.append('MimetypesRegistry')
PRODUCT_DEPENDENCIES.append('PortalTransforms')

# from Products.Five import zcml, fiveconfigure
# from Products.PloneTestCase.layer import onsetup
# from Testing.ZopeTestCase import installPackage
# 
# @onsetup
# def setupPackage():
#     """ set up the package and its dependencies """
#     # Install all (product-) dependencies, install them too
#     for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
#         ZopeTestCase.installProduct(dependency)
#         
#     ZopeTestCase.installProduct('membrane')
#     ZopeTestCase.installProduct('FacultyStaffDirectory')
#     
#     fiveconfigure.debug_mode = True
#     import Products.FacultyStaffDirectory
#     zcml.load_config('configure.zcml', Products.FacultyStaffDirectory)
#     fiveconfigure.debug_mode = False
#     #installPackage('Products.FacultyStaffDirectory')  # Should be unnecessary for a Zope 2-style product
# setupPackage()

PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('FacultyStaffDirectory')

def load_package_products():
    # Install all (product-) dependencies, install them too
    for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
        ZopeTestCase.installProduct(dependency)
        
    ZopeTestCase.installProduct('membrane')
    ZopeTestCase.installProduct('FacultyStaffDirectory')
    
    PloneTestCase.setupPloneSite(products=PRODUCTS)
    
load_package_products()

class testPlone(PloneTestCase.PloneTestCase):
    """Base TestCase for FacultyStaffDirectory."""
    
    #Utility methods
    def getEmptyDirectory(self, id="facstaffdirectory", portal=None):
        """Return a FacultyStaffDirectory (creating it first if necessary)."""
        portal = portal or self.portal
        if 'facstaffdirectory' not in portal.contentIds():
            portal.invokeFactory(type_name="FSDFacultyStaffDirectory", id=id)
        return portal[id]

    def getPopulatedDirectory(self, id="facstaffdirectory"):
        """Create a FSD containing some stuff, including...
            * A CommitteesFolder with id "committees"
            * A SpecialtiesFolder with id "specialties"
        """
        fsd = self.getEmptyDirectory(id)
        # Run the post-create script for some auto-generated content:
        fsd.at_post_create_script()
        return fsd

    def getPerson(self, directory=None, id="abc123", firstName="Test", lastName="Person", portal=None):
        """Create a Person, using only the required fields."""
        portal = portal or self.portal
        if not directory:
            directory = self.getEmptyDirectory(portal=portal)
        directory.invokeFactory(type_name="FSDPerson", id=id, firstName=firstName, lastName=lastName)
        return directory[id]

    def interact(self, locals=None):
        """Provides an interactive shell aka console inside your testcase.

        It looks exact like in a doctestcase and you can copy and paste
        code from the shell into your doctest. The locals in the testcase are
        available, because you are in the testcase.

        In your testcase or doctest you can invoke the shell at any point by
        calling::

            >>> self.interact( locals() )

        locals -- passed to InteractiveInterpreter.__init__()
        """
        savestdout = sys.stdout
        sys.stdout = sys.stderr
        sys.stderr.write('='*70)
        console = code.InteractiveConsole(locals)
        console.interact("""
ZopeTestCase Interactive Console
(c) BlueDynamics Alliance, Austria - 2005

Note: You have the same locals available as in your test-case.
""")
        sys.stdout.write('\nend of ZopeTestCase Interactive Console session\n')
        sys.stdout.write('='*70+'\n')
        sys.stdout = savestdout
        
    def getLargeDirectory(self, directory=None, numPersons=100):
        """generate a large number of persons in a directory"""
        
        firstNames = ("Jacob","Michael","Ethan","Joshua","Daniel","Christopher","Anthony","William",
                      "Matthew","Andrew","Alexander","David","Joseph","Noah","James","Ryan",
                      "Logan","Jayden","John","Nicholas","Tyler","Christian","Jonathan","Nathan",
                      "Samuel","Benjamin","Aiden","Gabriel","Dylan","Elijah","Brandon","Gavin",
                      "Jackson","Angel","Jose","Caleb","Mason","Jack","Kevin","Evan",
                      "Isaac","Zachary","Isaiah","Justin","Jordan","Luke","Robert","Austin",
                      "Landon","Cameron","Thomas","Aaron","Lucas","Aidan","Connor","Owen",
                      "Hunter","Diego","Jason","Luis","Adrian","Charles","Juan","Brayden",
                      "Adam","Julian","Jeremiah","Xavier","Wyatt","Carlos","Hayden","Sebastian",
                      "Alex","Ian","Sean","Jaden","Jesus","Bryan","Chase","Carter",
                      "Brian","Nathaniel","Eric","Cole","Dominic","Kyle","Tristan","Blake",
                      "Liam","Carson","Henry","Caden","Brady","Miguel","Cooper","Antonio",
                      "Steven","Kaden","Richard","Timothy","Girls","Name","Emily","Isabella",
                      "Emma","Ava","Madison","Sophia","Olivia","Abigail","Hannah","Elizabeth",
                      "Addison","Samantha","Ashley","Alyssa","Mia","Chloe","Natalie","Sarah",
                      "Alexis","Grace","Ella","Brianna","Hailey","Taylor","Anna","Kayla",
                      "Lily","Lauren","Victoria","Savannah","Nevaeh","Jasmine","Lillian","Julia",
                      "Sofia","Kaylee","Sydney","Gabriella","Katherine","Alexa","Destiny","Jessica",
                      "Morgan","Kaitlyn","Brooke","Allison","Makayla","Avery","Alexandra","Jocelyn",
                      "Audrey","Riley","Kimberly","Maria","Evelyn","Zoe","Brooklyn","Angelina",
                      "Andrea","Rachel","Madeline","Maya","Kylie","Jennifer","Mackenzie","Claire",
                      "Gabrielle","Leah","Aubrey","Arianna","Vanessa","Trinity","Ariana","Faith",
                      "Katelyn","Haley","Amelia","Megan","Isabelle","Melanie","Sara","Sophie",
                      "Bailey","Aaliyah","Layla","Isabel","Nicole","Stephanie","Paige","Gianna",
                      "Autumn","Mariah","Mary","Michelle","Jada","Gracie","Molly","Valeria",
                      "Caroline","Jordan",)
        
        lastNames = ("Smith","Johnson","Williams","Jones","Brown","Davis","Miller","Wilson",
                     "Moore","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin",
                     "Thompson","Garcia","Martinez","Robinson","Clark","Rodriguez","Lewis","Lee",
                     "Walker","Hall","Allen","Young","Hernandez","King","Wright","Lopez",
                     "Hill","Scott","Green","Adams","Baker","Gonzalez","Nelson","Carter",
                     "Mitchell","Perez","Roberts","Turner","Phillips","Campbell","Parker","Evans",
                     "Edwards","Collins","Stewart","Sanchez","Morris","Rogers","Reed","Cook",
                     "Morgan","Bell","Murphy","Bailey","Rivera","Cooper","Richardson","Cox",
                     "Howard","Ward","Torres","Peterson","Gray","Ramirez","James","Watson",
                     "Brooks","Kelly","Sanders","Price","Bennett","Wood","Barnes","Ross",
                     "Henderson","Coleman","Jenkins","Perry","Powell","Long","Patterson","Hughes",
                     "Flores","Washington","Butler","Simmons","Foster","Gonzales","Bryant","Alexander",
                     "Russell","Griffin","Diaz","Hayes",)
                     
        lcLetters = [chr(x) for x in range(ord('a'), ord('z'))]
        ucLetters = [chr(x) for x in range(ord('A'), ord('Z'))]
        digits = [chr(x) for x in range(ord('0'), ord('9'))]
        
        if not directory:
            portal = portal or self.portal
            directory = self.getEmptyDirectory(portal=portal)
               
        generated_ids = []
        i = 0
        while i < numPersons:
            i += 1
            
            #build an id, make sure it is unique
            good_id = None
            while not good_id:
                candidate_id = "".join(sample(lcLetters + ucLetters + digits, 8))
                if candidate_id not in generated_ids:
                    generated_ids.append(candidate_id)
                    good_id = candidate_id
            
            fn = choice(firstNames)
            ln = choice(lastNames)
            
            directory.invokeFactory(type_name="FSDPerson", id=good_id, firstName=fn, lastName=ln)
            
        return generated_ids


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
#    suite.addTest(makeSuite(testPlone))
    return suite
