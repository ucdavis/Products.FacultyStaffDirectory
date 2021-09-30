import csv
import os
from io import BytesIO
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode

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
            'field_sf_emails',
            'field_sf_position_title',
            'field_sf_office_location',
            'field_sf_street_address',
            'field_sf_office_city',
            'field_sf_office_state',
            'field_sf_office_zip',
            'field_sf_phone_numbers',
            'body',
            'field_sf_education_and_degrees',
            'field_sf_websites',
            'field_sf_research_interests'


        ]

        writer.writerow(header)

        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')

        targetDeptID = "mindbrain"
        department = catalog(portal_type='FSDDepartment', id=targetDeptID)
        #for multiple departments, don't use this next part
        deptobj = department[0].getObject()
        duid = deptobj.UID()
        people = catalog(getRawDepartments=duid, portal_type="FSDPerson")
        bioHead = """<div class="heading--secondary field__label">About</div>"""
        resHead = """div class="heading_secondary field__label">Research Focus</h3>"""
        labHead = """<div class="heading_secondary field__label">Lab</h3>"""
        pubHead = """<div class="heading_secondary field__label">>Publications</h3>"""
        teachHead = """<div class="heading_secondary field__label">>Teaching</h3>"""
        awdHead = """<div class="heading_secondary field__label">>Awards</h3>"""
        


        for person in people:

                pobj = person.getObject()
                memberinfo = deptobj.getMembershipInformation(pobj)
                #this image url won't work for staff - consider running against cortex
                #create bio
                
                if pobj.research:
                    bio = ("".join([bioHead,pobj.getBiography(),resHead,pobj.getResearch()]))
                
                if pobj.getLabs():
                    lab = pobj.getLabs()[0]
                    labname = pobj.getLabNames()[0]
                    if pobj.getWebsites()[0]:
                        laburl = pobj.getWebsites()[0]
                        hyperlink_format = '<a href="{link}">{text}</a>'
                        labLink = hyperlink_format.format(link=laburl, text=labname)
                        bio = ("".join([bio,labHead,labLink]))
                    else:
                        bio = ("".join([bio,labHead]))
               
                if pobj.getPublications():
                    bio = ("".join([bio,pubHead,pobj.getPublications()]))
                
                if pobj.getTeaching():
                    bio = ("".join([bio,teachHead,pobj.getTeaching()]))
                
                if pobj.getAwards():
                    bio = ("".join([bio,awdHead,pobj.getAwards()])) 

                
                row = []
                row.append(pobj.id)
                row.append(pobj.firstName)
                row.append(pobj.middleName)
                row.append(pobj.lastName)
                row.append(pobj.email)
                row.append(memberinfo.getPosition())
                row.append(memberinfo.getDept_officeAddress())
                row.append(memberinfo.getDept_streetAddress())
                row.append(memberinfo.getDept_city())
                row.append(memberinfo.getDept_state())
                row.append(memberinfo.getDept_zip())
                row.append(memberinfo.getDept_officePhone())
                row.append(bio)
                row.append(pobj.education)
                row.append(pobj.websites)
                row.append(pobj.getSpecialtyNames())
                
                writer.writerow(row)
        value = buffer.getvalue()

        if not encoding:
            encoding = 'UTF-8'
        self.request.response.setHeader('Content-type',
                        'text/csv;charset='+encoding)
        self.request.response.setHeader('Content-Disposition',
                        'attachment; filename=export.csv')

        return value
