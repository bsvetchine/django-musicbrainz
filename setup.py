"""Setup file for easy installation"""
from setuptools import setup, find_packages

VERSION = __import__("django_musicbrainz").__version__
LONG_DESCRIPTION = """
Django Musicbrainz is a small app that allows browsing data from a local musicibrainz database within your django project.

It contains a models.py file describing the musicbrainz database organization and a router.py file allowing read access to the musicbrainz database.
""" 

setup(
	name="django-musicbrainz",
	version=VERSION,
	description="Django connector app to musicbrainz database",
	long_description=LONG_DESCRIPTION,
	author="Bertrand Svetchine",
	author_email="bertrand.svetchine@gmail.com",
	url="https://github.com/bsvetchine/django-musicbrainz",
	packages=find_packages(),
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Web Environment",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Framework :: Django",
	],
	include_package_data=True,
	zip_safe=False,
)
