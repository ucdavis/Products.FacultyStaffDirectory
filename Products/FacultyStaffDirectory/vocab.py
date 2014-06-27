from five import grok
from zope import schema

from Products.CMFCore.interfaces import ISiteRoot, IFolderish
from Products.statusmessages.interfaces import IStatusMessage

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

#This file provides the vocabulary hooks to get FSD working with the eea.facetednavigation UI


def make_terms(items):
    """ Create zope.schema terms for vocab from tuples """
    terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
    return terms

@grok.provider(IContextSourceBinder)
def department_vocab(context):
    """
    Populate vocabulary with values from portal_catalog.

    @param context: z3c.form.Form context object (in our case site root)

    @return: SimpleVocabulary containing all areas as terms.
    """

    # Get site root from any content item using portal_url tool thru acquisition
    root = context.portal_url.getPortalObject()

    # Acquire portal catalog
    portal_catalog = root.portal_catalog

    # We need to get Plone site path relative to ZODB root
    # See traversing docs for more info about getPhysicalPath()
    #site_physical_path = '/'.join(root.getPhysicalPath())

    # Target path we are querying
    #folder_name = "people"

    # Query all folder like objects in the target path
    # These portal_catalog query conditions are AND
    # but inside keyword query they are OR (the different content types
    # we are looking for)
    brains = portal_catalog.searchResults({'portal_type':'FSDDepartment', 'review_state':'active'})

    # Create a list of tuples (UID, Title) of results
    result = [ (brain["UID"], brain["Title"]) for brain in brains ]

    # Convert tuples to SimpleTerm objects
    terms = make_terms(result)

    return SimpleVocabulary(terms)
    
def classification_vocab(context):
     # Get site root from any content item using portal_url tool thru acquisition
     root = context.portal_url.getPortalObject()

     # Acquire portal catalog
     portal_catalog = root.portal_catalog

     # Portal catalog query
     brains = portal_catalog.searchResults({'portal_type':'FSDClassification', 'review_state':'active'})

     # Create a list of tuples (UID, Title) of results
     result = [ (brain["UID"], brain["Title"]) for brain in brains ]

     # Convert tuples to SimpleTerm objects
     terms = make_terms(result)
     
     return SimpleVocabulary(terms)
     
def specialty_vocab(context):
     # Get site root from any content item using portal_url tool thru acquisition
     root = context.portal_url.getPortalObject()

     # Acquire portal catalog
     portal_catalog = root.portal_catalog

     #portal catalog query
     
     brains = portal_catalog.searchResults({'portal_type':'FSDSpecialty', 'review_state':'published'})

     # Create a list of tuples (UID, Title) of results
     result = [ (brain["UID"], brain["Title"]) for brain in brains ]

     # Convert tuples to SimpleTerm objects
     terms = make_terms(result)
     
     return SimpleVocabulary(terms)
     
     
