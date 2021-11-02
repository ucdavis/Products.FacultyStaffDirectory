##event export code
import csv
import os
from io import BytesIO
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode
import unicodedata
from Products.CMFCore.utils import getToolByName

class CSVEventExport(BrowserView):
    def __call__(self):
        buffer = BytesIO()
        encoding = self.request.get('encoding')
        writer = csv.writer(buffer)
        
        header = [
            'url',
            'field_sf_title',
            'field_sf_event_location',
            'start_date',
            'end_date',
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
        eventsPath = site[targetDeptID]['events'] 
        events = eventsPath.listFolderContents(contentFilter={"portal_type" : "Event"})
        
        def listToString(somelist):
            newString = " "
            return(newString.join(somelist))
            
        for event in events:
            contactInfo = []
            
            if event.contactName:
                contactInfo = ["<li>" + unicodedata.normalize('NFKD', event.contactName).encode('ascii', 'ignore') + "</li>"]

            if event.contactEmail:
                contactInfo.append("<li>" + unicodedata.normalize('NFKD', event.contactEmail).encode('ascii', 'ignore') + "</li>")
            
            if event.contactPhone: 
                contactInfo.append("<li>" + unicodedata.normalize('NFKD', event.contactPhone).encode('ascii', 'ignore') + "</li>")
                
            try:
                contactStr = listToString(contactInfo)
                #newContact = unicodedata.normalize('NFKD', contactStr).encode('ascii', 'ignore').decode('ascii')
                #print newContact
            except:
                pass
                    
            if event.Description():
                body = event.Description()
            else:
                body = ""
            if event.getText():
                body = (" ".join([body,event.getText()]))
                
            if event.getAttendees():
                attendeesStr = listToString(event.getAttendees())
                body = (" ".join([body,attendees,attendeesStr]))
                
            if contactStr:
                contactinfo = ""
                contactinfo = (" ".join([contactInfoHead,contactOpen,contactStr,contactClose]))
                
                body = (" ".join([body,contactinfo]))
            
          
            row = []
            row.append(event.id)
            row.append(event.Title())
            row.append(event.getLocation())
            row.append(event.startDate.ISO())
            row.append(event.endDate.ISO())
            row.append(body)
            row.append(event.Subject())
    
            writer.writerow(row)
        value = buffer.getvalue()

        if not encoding:
            encoding = 'UTF-8'
        self.request.response.setHeader('Content-type',
                        'text/csv;charset='+encoding)
        self.request.response.setHeader('Content-Disposition',
                        'attachment; filename=events_export.csv')

        return value
                
        
        