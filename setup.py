# Before releasing, make sure to update the translations:
# $ for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done
# # To build locally: python setup.py egg_info -RDb "" bdist_egg 
# To release: python setup.py egg_info -RD sdist bdist_egg register upload
# To create a named release: python setup.py egg_info -RDb "a1" sdist bdist_egg register upload
# To release a dev build: python setup.py egg_info -rD sdist bdist_egg register upload
# See http://peak.telecommunity.com/DevCenter/setuptools#release-tagging-options for more information.

from setuptools import setup, find_packages
import os

version = '3.1.3DS'

setup(name='Products.FacultyStaffDirectory',
      version=version,
      description="Provides content types for creating and organizing personnel directories within educational institutions. Integrates with Plone's users and groups infrastructure and supports an extensibility framework for custom requirements.",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='WebLion Group, The Pennsylvania State University',
      author_email='support@weblion.psu.edu',
      url='https://weblion.psu.edu/svn/weblion/weblion/Products.FacultyStaffDirectory',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Plone>=4.0',
          'archetypes.schemaextender',
          'Products.Relations>=0.9b1',
          'Products.membrane>=2.1.4',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
