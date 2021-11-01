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
        attendees = """<h3>Who is Invited?</h3>"""
        contactOpen = """<ul class="list--arrow">"""
        contactClose = """</ul>"""
        header = [
            'url',
            'field_sf_title',
            'field_sf_description',
            'field_sf_event_location',
            'start_date',
            'end_date',
            'field sf_body',
            'tags'
            
            text, attendees, eventUrl, contactName, contactEmail, contactPhone, subject,
            


        ]

        writer.writerow(header)
        site = getSite()
        #catalog = getToolByName(site, 'portal_catalog')
        targetDeptID = "mindbrain"
        eventsPath = site.targetDeptID.events
        items = eventsPath.contentItems()
        for item in items:
            if "Event" in item.getPortalTypeName():
                contactInfo = []
                    try:
                        contactInfo.append("<li>" + item.contactName + "<li>")
                    except:
                        pass
                    try:
                         contactInfo.append("<li>" + item.contactEmail + "<li>")
                    except:
                        pass
                    try: 
                        contactInfo.append("<li>" item.contactPhone + "<li>")
                        
                body = ""
                if item.Description:
                    body = item.Description
                if item.getText():
                    body = (" ".join([body,item.getText()]))
                if item.getAttendees():
                    body = (" ".join([body,attendees,item.getAttendees()]))
                    
                if contactInfo:
                    body = (" ".join([body,contactOpen,contactInfo,contactClose]))
                
              
                row = []
                row.append(item.id)
                row.append(item.Title())
                row.append(item.getLocation())
                row.append(item.startDate.ISO() )
                row.append(item.endDate.ISO())
                row.append(body)
                row.append(item.Subject())
        
                writer.writerow(row)
        value = buffer.getvalue()

        if not encoding:
            encoding = 'UTF-8'
        self.request.response.setHeader('Content-type',
                        'text/csv;charset='+encoding)
        self.request.response.setHeader('Content-Disposition',
                        'attachment; filename=events_export.csv')

        return value
                
        
        