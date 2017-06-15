# methods to my madness
import lxml.html
from lxml.html import parse
from lxml.html.clean import Cleaner
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

site = getSite()


target = site.courses
source = site.import_html

# get all the siblings after summarytext
def getBodyText():
    bodies = cleaned.xpath('//p[@class="Pagetitle"]/following-sibling::p')
    # Smash them all back together because I suck at xml parsing
    body = ""
    for body in bodies:
        snatcher = lxml.html.tostring(body)
        newbody = snatcher + snatcher

        return newbody


def createPages():
    items = source.contentItems()
    for item in items:
        doc = parse(item).getroot()
        cleaner = Cleaner(style=True, links=False, page_structure=True, safe_attrs_only=False)
        cleaned = cleaner.clean_html(doc)
    # get the pagetitle

        titles = cleaned.find_class('Pagetitle')
    # snag the page title - method returns list. . there's really only one
        title = titles[0].text_content()

    # get the description
        descrips = cleaned.find_class('Summarytext')
        descrip = descrips[0].text_content()
    #Need to have temporary id
        id = str(random.randint(0, 99999999))

        target.invokeFactory("Document", id=uid)
        obj = target[uid]
        obj.setTitle(title)
        obj.setDescription(descrip)
        obj.setText.getBodyText()


# Will finish Archetypes content item creation process,
# rename-after-creation and such
        obj.processForm()

        return obj

