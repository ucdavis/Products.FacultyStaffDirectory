import csv
import os
from io import BytesIO
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName


class CSVExport(BrowserView):
  
    def __call__(self):
        buffer = BytesIO()
        encoding = self.request.get('encoding')
        writer = csv.writer(buffer)
        header = [
            'login',
            'field_sf_first_name',
            'field_sf_middle_initial',
            'field_sf_last_name',
            'suffix',
            'field_sf_emails',
            'field_sf_position_title',
            'field_sf_office_location',
            'officeCity',
            'officeState',
            'officePostalCode',
            'field_sf_phone_numbers',
            'body',
            'field_sf_education_and_degrees',
            'field_sf_websites',
            'field_sf_honors_and_awards',
            'field_sf_publications',
            'field_sf_research_interests',
            'field_sf_courses'
            'image',
            'lab name',
            'lab url'

        ]

        writer.writerow(header)	

        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')

        
        targetDeptID = "blue-cluster-staff"
        department = catalog(portal_type='FSDDepartment', id=targetDeptID)
        #for multiple departments, don't use this next part
        deptobj = department[0].getObject()
        duid = deptobj.UID()
        people = catalog(getRawDepartments=duid, portal_type="FSDPerson")
        
        

        for person in people:
            
                pobj = person.getObject()
                memberinfo = deptobj.getMembershipInformation(pobj)
                #this image url won't work for staff - consider running against cortex
                imageurl = "https://%s.ucdavis.edu/people/%s/image"%(targetDeptID, pobj.id)
                
                row = []
                row.append(pobj.id)
                row.append(pobj.firstName)
                row.append(pobj.middleName)
                row.append(pobj.lastName)
                row.append(pobj.suffix)
                row.append(pobj.email)
                row.append(memberinfo.getPosition())
                row.append(memberinfo.getDept_officeAddress())
                row.append(pobj.officeCity)
                row.append(pobj.officeState)
                row.append(pobj.officePostalCode)
                row.append(memberinfo.getDept_officePhone())
                row.append(pobj.biography)
                row.append(pobj.education)
                row.append(pobj.websites)
                row.append(pobj.awards)
                row.append(pobj.publications)
                row.append(pobj.research)
                row.append(pobj.teaching)
                row.append(imageurl)
                row.append(pobj.getLabs[0])
                row.append(pobj.getLabs[0].absolute_url())
                
                writer.writerow(row)
        value = buffer.getvalue()

        if not encoding:
            encoding = 'UTF-8'
        self.request.response.setHeader('Content-type',
                        'text/csv;charset='+encoding)
        self.request.response.setHeader('Content-Disposition',
                        'attachment; filename=export.csv')

        return value