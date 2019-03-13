# Find arbitrary HTML snippets on Plone content pages

# Collect script output as text/html, so that you can
# call this script conveniently by just typing its URL to a web browser


# We need to walk through all the content, as the
# links might not be indexed in any search catalog
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
import os
import os.path

def lsLinks(self):
  buffer = ""
  site = getSite()
  portal_catalog = getToolByName(site, 'portal_catalog')
  myText = "ls.ucdavis.edu"

  for brain in self.portal_catalog(): # This queries cataloged brain of every content object
      try:
          obj = brain.getObject()
          # Call to the content object will render its default view and return it as text
          # Note: this will be slow - it equals to load every page from your Plone site
          rendered = obj()
          if myText in rendered:
              # found old link in the rendered output
              buffer += "Found old links on <a href='%s'>%s</a><br>\n" % (obj.absolute_url(), obj.Title())
      except:
          pass # Something may fail here if the content object is broken

      writeBufferToFile(buffer)
  
def writeBufferToFile(buffer):
     save_path = '/Users/carolm/Downloads'
     file_name = 'buffer'
     fnamePath =  os.path.join(save_path, file_name+".txt" )
     file1 = open(fnamePath, "w")
     file1.write(buffer)
     file1.close()
     
     print "done"
     
     
     
     
