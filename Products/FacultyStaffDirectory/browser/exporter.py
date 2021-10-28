import csv
import os
from io import BytesIO
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode
import unicodedata
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
            'field_sf_websites',
            'field_sf_research_interests',
            'person_type'


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
        edHead = """<h3>Education</h3>"""
        eduHead = """<ul class="list--arrow">"""
        eduClose = """</ul>"""
        bioHead = """<h3>About</h3>"""
        resHead = """<h3>Research Focus</h3>"""
        labHead = """<h3>Lab</h3>"""
        pubHead = """<h3>Publications</h3>"""
        teachHead = """<h3>Teaching</h3>"""
        awdHead = """<h3>Awards</h3>"""
        
        

        def listToString(edList):
            edString = " "
            return(edString.join(edList))
            
        for person in people:

                pobj = person.getObject()
                memberinfo = deptobj.getMembershipInformation(pobj)
                
                #this image url won't work for staff - consider running against cortex
                #create bio
                if pobj.getEducation():
                    edList = []
                    for degree in pobj.getEducation():
                        Ed = "<li>" + degree + "</li>"
                        edList.append(Ed)
                    edString = listToString(edList)
                    bio = (" ".join([edHead,eduHead,edString,eduClose]))
                else:
                    bio = ""                      
                      
                if pobj.getBiography():
                    bio = ("".join([bio,bioHead,pobj.getBiography()]))
                
                if pobj.research:
                    bio = (" ".join([bio,resHead,pobj.getResearch()]))
                
                if pobj.getLabs():
                    lab = pobj.getLabs()[0]
                    labname = pobj.getLabNames()[0]
                    if pobj.getWebsites():
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
                row.append(pobj.websites)
                row.append(pobj.getSpecialtyNames())
                row.append(pobj.getClassificationNames())
                
                writer.writerow(row)
        value = buffer.getvalue()

        if not encoding:
            encoding = 'UTF-8'
        self.request.response.setHeader('Content-type',
                        'text/csv;charset='+encoding)
        self.request.response.setHeader('Content-Disposition',
                        'attachment; filename=export.csv')

        return value
