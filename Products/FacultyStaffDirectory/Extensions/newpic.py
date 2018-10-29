from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
import transaction
import os
import re
import PIL
from PIL import Image



def updatePics( self ):
          site = getSite()
          catalog = site.portal_catalog	
          path = r'/Users/carolm/Desktop/boxphotos/Photos/JPEG'
          for dirpath, subdirs, files in os.walk(path):
              for x in (y for y in files if y != ".DS_Store"):
                  xname = x.split("-")
                  personid = xname[2]
                  person = site.people.get(personid)
                  print person
                  if person:
                      self.plone_log("working on " + person.id)
                      newimage = (os.path.join(path, x))
                      
                      person.setImage(newimage.read())
            #               person.image = newimage
            #                  PIL.Image.open(newimage)
                      person.image = newimage
                      transaction.commit()
              
              print "Photos Updated" 
