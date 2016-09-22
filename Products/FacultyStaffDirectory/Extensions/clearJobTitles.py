from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
import transaction

def synchronize( self ):
        site = getSite()	
        people = site.people.listFolderContents(contentFilter={"portal_type" : "FSDPerson"})
        newJobTitles = ''
       
   
        for person in people:
            person.getField('jobTitles').set(person, newJobTitles)
		  transaction.commit()
	