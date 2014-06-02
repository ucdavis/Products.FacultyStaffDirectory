from Products.CMFCore.utils import getToolByName

def relationModified(event):
    """ Reindex each end of the relationship in portal_catalog to prevent #325. """
    catalog = getToolByName(event.context, 'portal_catalog')
    for ref in event.references:
        catalog.reindexObject(ref.getSourceObject())
        catalog.reindexObject(ref.getTargetObject())