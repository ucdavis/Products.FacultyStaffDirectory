from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
import transaction
from Products.CMFPlone import PloneMessageFactory as _
from datetime import date
from datetime import datetime

def delete_spamUsers():
   site = getSite()
   txn = transaction.get()
   md = getToolByName(site, 'portal_memberdata')
   mt = getToolByName(site, 'portal_membership')

   memberIds = mt.listMemberIds()
   for id in memberIds:
      member = mt.getMemberById(id)
      username = member.getUserName
      lastlogin = member.getProperty('last_login_time')
      return datetime(lastlogin)