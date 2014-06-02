## Script (Python) "contextualClassification"
##title=
##parameters=classification
# Create a path that puts the request in the context of the directory root. Allows us to do subsetting of classifications (ie. some-department/faculty).
return context.restrictedTraverse('/'.join(context.portal_url.getRelativeContentPath(classification) + context.portal_url.getRelativeContentPath(context))).restrictedTraverse(classification.id)