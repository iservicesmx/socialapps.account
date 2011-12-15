from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='socialapps.account',
      version=version,
      description="Social app accounts manage",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='django social apps account',
      author='Erik Rivera',
      author_email='erik@iservices.mx',
      url='http://iservices.mx',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['socialapps'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
