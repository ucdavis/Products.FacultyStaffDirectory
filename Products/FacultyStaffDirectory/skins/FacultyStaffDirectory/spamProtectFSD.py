##parameters=email

# Implement a different email obfuscating approach than the standard Plone spam
# protection.  Dots, @ etc. will be replaced with a string representation.

from Products.CMFCore.utils import getToolByName
fsd = getToolByName(context, 'facultystaffdirectory_tool')

if fsd.getObfuscateEmailAddresses():
    email = email.replace('.', ' [ DOT ] ')
    email = email.replace('@', ' [ AT ] ')
    email = email.replace('-', ' [ DASH ] ')
    email = email.replace('_', ' [ UNDERSCORE ] ')
    return email
else:
    return context.spamProtect(email)
