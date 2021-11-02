#start the file
##event export code
import csv
import os
from io import BytesIO
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode
import unicodedata
from Products.CMFCore.utils import getToolByName

class CSVNewsExport(BrowserView):
    def __call__(self):
        buffer = BytesIO()
        encoding = self.request.get('encoding')
        writer = csv.writer(buffer)
        
        header = [
            'url',
            'field_sf_title',
            'created',
            'field sf_body',
            'tags'

        ]

        writer.writerow(header)
        site = getSite()
        #catalog = getToolByName(site, 'portal_catalog')
        attendees = """<strong>Who is Invited?</strong>"""
        contactInfoHead = """<strong>Contact</strong>"""
        contactOpen = """<ul class="list--arrow">"""
        contactClose = """</ul>"""
        targetDeptID = "mindbrain"
        newsPath = site[targetDeptID]['news'] 
        allNews = newsPath.listFolderContents(contentFilter={"portal_type" : "News Item"})
        
        def listToString(somelist):
            newString = " "
            return(newString.join(somelist))
            
        for news in allNews:
            
            if news.Description():
                body = news.Description()
            else:
                body = ""
            
            if news.getText():
                body = (" ".join([body,news.getText()]))
            
            row = []
            row.append(news.id)
            row.append(news.Title())
            row.append(news.creation_date.ISO())
            row.append(body)
            row.append(news.Subject())

            writer.writerow(row)
        value = buffer.getvalue()

        if not encoding:
            encoding = 'UTF-8'
        self.request.response.setHeader('Content-type',
            'text/csv;charset='+encoding)
        self.request.response.setHeader('Content-Disposition',
            'attachment; filename=news_export.csv')

        return value
          
  
        
            