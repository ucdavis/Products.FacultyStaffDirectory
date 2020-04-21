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
            'firstName',
            'middleName',
            'lastName',
            'suffix',
            'email',
            'jobTitles',
            'officeAddress',
            'officeCity',
            'officeState',
            'officePostalCode',
            'officePhone',
            'biography',
            'education',
            'websites',
            'image',

        ]

        writer.writerow(header)	

        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')

        
        targetDeptID = "yellow-cluster-staff"
        department = catalog(portal_type='FSDDepartment', id=targetDeptID)
        #for multiple departments, don't use this next part
        deptobj = department[0].getObject()
        duid = deptobj.UID()
        people = catalog(getRawDepartments=duid, portal_type="FSDPerson")
        

        for person in people:
            
                pobj = person.getObject()
                imageurl = "https://it.dss.ucdavis.edu/people/%s/image_normal"%(pobj.id)
                row = []
                row.append(pobj.id)
                row.append(pobj.firstName)
                row.append(pobj.middleName)
                row.append(pobj.lastName)
                row.append(pobj.suffix)
                row.append(pobj.email)
                row.append(pobj.jobTitles)
                row.append(pobj.officeAddress)
                row.append(pobj.officeCity)
                row.append(pobj.officeState)
                row.append(pobj.officePostalCode)
                row.append(pobj.officePhone)
                row.append(pobj.biography)
                row.append(pobj.education)
                row.append(pobj.websites)
                row.append(imageurl)

                writer.writerow(row)
        value = buffer.getvalue()

        if not encoding:
            encoding = 'UTF-8'
        self.request.response.setHeader('Content-type',
                        'text/csv;charset='+encoding)
        self.request.response.setHeader('Content-Disposition',
                        'attachment; ilename=export.csv')

        return value