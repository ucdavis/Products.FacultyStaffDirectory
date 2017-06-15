from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
import transaction
import os
import re



def updatePics( self ):
        site = getSite()
        catalog = site.portal_catalog	
        path = r'/Users/carolm/Desktop/headspng'
        print path
        for dirpath, subdirs, files in os.walk(path):
          for x in files:
              print x
              if x != ".DS_Store":
                  xname = x.split("-")
                  personid = xname[2]
                  person = site.people.get(personid)
                  self.plone_log("working on " + person.id)
                  newimage = x
                  person.setImage(newimage)
                  transaction.commit()
                      
              print "Photos Updated"					 
