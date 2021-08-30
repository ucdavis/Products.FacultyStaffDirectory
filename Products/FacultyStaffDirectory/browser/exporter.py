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
            'field_sf_office_city',
            'field_sf_office_state',
            'field_sf_office_zip',
            'field_sf_phone_numbers',
            'body',
            'field_sf_education_and_degrees',
            'field_sf_websites',
            'field_sf_research_interests',

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
        bioHead = """<h3 class="heading--auxiliary">Biography</h3>"""
        resHead = """<h3 class="heading--auxiliary">Research Focus</h3>"""
        pubHead = """<h3 class="heading--auxiliary">Research Focus</h3>"""
        teachHead = """<h3 class="heading--auxiliary">Teaching</h3>"""
        awdHead = """<h3 class="heading--auxiliary">Awards</h3>"""



        for person in people:

                pobj = person.getObject()
                memberinfo = deptobj.getMembershipInformation(pobj)
                #this image url won't work for staff - consider running against cortex
                #create bio
                if pobj.research:
                    bio = ("".join(bioHead,pobj.biography,resHead,pobj.research))
                if pobj.publications:
                    bio = ("".join(bio,pubHead,pobj.publications))
                if pobj.teaching:
                    bio = ("".join(bio,teachHead,pobj.teaching))
                if pobj.awards:
                    bio = ("".join(bio,awdHead,pobj.awards))
                row = []
                row.append(pobj.id)
                row.append(pobj.firstName)
                row.append(pobj.middleName)
                row.append(pobj.lastName)
                row.append(pobj.email)
                row.append(memberinfo.getPosition())
                row.append(memberinfo.getDept_officeAddress())
                row.append(pobj.getDept_officeCity())
                row.append(pobj.getDept_officeState())
                row.append(pobj.getDept_officePostalCode())
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
~                                                                                