from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='APUTimeTable',
      version=version,
      description="A library to interact with and generate Timetables from A.P.U",
      long_description=open("README.rst").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ye Myat Kaung',
      author_email='jms@mavjs.org',
      url='https://github.com/mavjs/APUTimeTable',
      license='GNU GPLv3',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['apu'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pytz',
          'BeautifulSoup',
          'icalendar',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
