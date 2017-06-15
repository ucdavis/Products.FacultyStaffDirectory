import lxml.html
from lxml.html import parse
from lxml.html.clean import Cleaner
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
import fnmatch
import os
import random
import transaction
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
import re

site = getSite()



target = site.lingradfolder

# get all the siblings after summarytext
        


def parsePages(): 
         
	 
    # get the pagetitle
    path= r'/Users/carolm/mesa2/ir.ucdavis.edu_8081/mesa/faculty/me-sa-faculty'  
        
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            print x
            if fnmatch.fnmatch(x, '*.html'):
                item = os.path.join(dirpath, x)
                doc = parse(item).getroot()
                cleaner = Cleaner(style=True, links=False,)
                cleaned = cleaner.clean_html(doc)
                
                titles = cleaned.xpath('//h1[@id="parent-fieldname-title"]')
                if titles:
    # snag the page title - method returns list. . there's really only one
                    title = titles[0].text_content()
                    print title
                #else:
                #    try:
                #       titlesel = cleaned.xpath('//p[@class="Subhead"]')
                #       title = titlesel[0].text_content()
                #    except:
                #       pass  
      

    # get the description
                descrips = cleaned.xpath('//div[@id="parent-fieldname-description"]')
                if descrips:
                    descrip = descrips[0].text_content()
                    print descrip
                else:
                    descrip = "no description"
    #get the body
                bodies = cleaned.xpath('//div[@id="content-core"]')
                html = "".join([lxml.html.tostring(body, method='xml')for body in bodies])
                
                newbody = html
                print newbody
                
                                           
                           
                
            
    #Need to have temporary id
                id = str(random.randint(0, 99999999))

                target.invokeFactory("Document", id)
                obj = target[id]
                obj.setTitle(title)
                obj.setDescription(descrip)
                obj.setText(newbody)


# Will finish Archetypes content item creation process,
# rename-after-creation and such
                obj.processForm()
                transaction.savepoint(optimistic=True)

    # Need to perform manual normalization for id,
    # as we don't have title available during the creation time
                normalizer = getUtility(IIDNormalizer)
                new_id = normalizer.normalize(obj.Title())

                if new_id in target.objectIds():
                    raise RuntimeError("Item already exists:" + new_id + " in " + target.absolute_url())

                obj.aq_parent.manage_renameObject(id, new_id)
                transaction.commit()
                obj.reindexObject()
                  
