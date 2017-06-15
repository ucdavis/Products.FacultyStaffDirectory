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
def getBodyText():
    bodies = doc.xpath('//p[@class="Pagetitle"]/following-sibling::p')
    # Smash them all back together because I suck at xml parsing
    body = ""
    for body in bodies:
        snatcher = lxml.html.tostring(body)
        newbody = snatcher + snatcher

        return newbody
        


def parsePages(): 
         
	 
    # get the pagetitle
    path= r'/Users/carolm/Desktop/lingrad'  
        
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            if fnmatch.fnmatch(x, '*.html'):
                item = os.path.join(dirpath, x)
                doc = parse(item).getroot()
                print doc.text_content()
                cleaner = Cleaner(style=True, links=False,)
                cleaned = cleaner.clean_html(doc)
                
                titles = cleaned.find_class('Pagetitle')
                if titles:
    # snag the page title - method returns list. . there's really only one
                    title = titles[0].text_content()
                else:
                    try:
                       titlesel = cleaned.xpath('//p[@class="Subhead"]')
                       title = titlesel[0].text_content()
                    except:
                       pass  
      

    # get the description
                descrips = cleaned.find_class('Summarytext')
                if descrips:
                    descrip = descrips[0].text_content()
                else:
                    descrip = "no description"
    #get the body
                if cleaned.find_class('Summarytext'):
                     bodies = cleaned.xpath('//p[@class="Summarytext"]/following-sibling::p')
                elif cleaned.find_class('Subhead'):
                     bodies = cleaned.xpath('//p[@class="Subhead"]//following-sibling::p')
                else:
                     bodies = cleaned.xpath('*//p')
                     
                
                
                
                     
                html = "".join([lxml.html.tostring(body, method='xml')for body in bodies])
                html = html.replace('\n', ' ').replace('\r', ' ')
                html = html.replace('&#10;', ' ').replace('&#13;', ' ')
                html = html.replace('&#xa;', ' ').replace('&#xd;', ' ')
                html = html.replace('&#8226;', '').replace('&#160;', '')
                html = html.replace('&nbsp', '')
                html = html.replace('class="msoNormal"','').replace('###','')
                html = html.replace('<span> </span>','')
              #  html = re.sub(r'<p.*?[.*?Body text:.*?].*?</p>', r'', html)
                html = re.sub(r'<p class="Bullettext">(.*?)</p>', r'<li>\1</li>', html)
                html = re.sub(r'<p class="Subhead1">(.*?)</p>', r'<h3>\1</h3>', html)
                    
                     
                newbody = html
                
                                           
                           
                
            
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
                  
