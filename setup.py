from setuptools import setup, find_packages


setup(
	name="django-musicbrainz",
	version=__import__("musicbrainz").__version__,
	description="Django connection app to musicbrainz database",
	long_description=open("readme.md").read(),
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
