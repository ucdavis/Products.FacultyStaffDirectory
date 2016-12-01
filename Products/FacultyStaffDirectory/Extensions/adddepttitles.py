from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
import transaction

def updateStuff( self ):
        site = getSite()	
        people = site.people.listFolderContents(contentFilter={"portal_type" : "FSDPerson"})
        newDeptTitle = 'Graduate Student'
        searchDepartment = 'Department of Political Science'
        searchClass = "Graduate Students"
        
       
   
        for person in people:
           for classification in person.getClassifications():
              if searchClass in classification.title:
                 for department in person.getDepartments(): 
	                 if searchDepartment in department.title: 	
                           deptmember = department.getMembershipInformation(person)
                           if not deptmember.getPosition():
                              deptmember.position = newDeptTitle
                              print "processed " % person
                              transaction.commit()