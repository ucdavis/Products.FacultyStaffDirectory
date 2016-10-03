# External Method for importing FSD People from a CSV file
#
# instructions: CSV expects titles on first line. Use classification short name (typically has dashes)


from Products.CMFCore.utils import getToolByName
from Products.Relations.processor import process


def ImportFSDPeople(self):
  print "FSD People Importing Script"
  print ""
  
  # define the file that will be imported
  file = self['fsd-import.csv']
  print "CSV input file set"
  
  # define who will be the personal assistant for these people
#  asstId = ""
#  if asstId <> "":
#    asstUID = self.people[asstId].UID()


  # define the specialty to set for EVERYONE on the list
#  specialtyId = ""
#  if specialtyId <> "":
#    specialtyUID = self.portal_catalog(id=specialtyId, portal_type="FSDSpecialty")[0].UID
#    specialtyRulesetId = getToolByName(self, 'relations_library').getRuleset('people_specialties').getId()
  
  # set the location of the FSD
  directory = self.people
  print "Found FSD directory: ", directory.Title()
  
  # loop through all the lines in the CSV file except the first (it has headers)
  for line in file.data.split("\n")[1:]:
    if line.strip() <> "":
      # define all the values in the line
      rawId, firstname, middlename, lastname, classification, email = line.split(',')
      id = rawId.strip()

      # make sure the ID field is not blank
      if id <> "":
        print "user: ", id 
        # see if the user exists in FSD
        if not id in directory.objectIds():
          # the user does not exist
      
          if classification.strip() <> "":
	          # get the classification UID for this user's classification
	          print "Looking up the classification"
	          classificationUID = self.portal_catalog(Title=classification, portal_type="FSDClassification")[0].UID
	      
	          # create the FSD person
	          print "Creating a FSD person object with a classification"
	          directory.invokeFactory(type_name='FSDPerson', id=id, firstName=firstname.strip(), middleName=middlename.strip(), lastName=lastname.strip(), classifications=[classificationUID], email=email.strip())
	          directory[id].at_post_create_script()
	          
	  else:
	          # create the FSD person
	          print "Creating a FSD person object"
	          directory.invokeFactory(type_name='FSDPerson', id=id, firstName=firstname.strip(), middleName=middlename.strip(), lastName=lastname.strip(), email=email.strip())
	          directory[id].at_post_create_script()
      
     
        # see if a personal assistant was specified
        #if asstId <> "":
        #  # do not add the personal assistant if it's the person
        #  if id <> asstId: 
        #    # get the personal assistants for this person
        #    currentAssistants = directory[id].getAssistants()
      
            # if the personal assistant is not assigned to this person, assign them
          #  if not asstUID in currentAssistants:
          #    currentAssistants.extend([asstUID])
          #    directory[id].setAssistants(currentAssistants)


        # see if we need to set a specialty
        #if specialtyId <> "":
          # get all the specialties assigned to this person
         # specialtiesTuple = directory[id].getSpecialties()
         # specialties = [eachSpecialtiesTuple[0].getObject().UID() for eachSpecialtiesTuple in specialtiesTuple]

          # see if the specialty we are assigning is already assigned
         # if specialtyUID not in specialties:
         #   print "Specialty not assigned, assigning it"

            # You mustmustmust use the Relations API to add references, sayeth Relations/doc/Overview.txt.
          #  process(self, connect=((directory[id].UID(), specialtyUID, specialtyRulesetId),))

  print "Done!"
