django-musicbrainz
==================

Django connection app for musicbrainz database

## Description

Django Musicbrainz is a small app that allows browsing data from a local musicibrainz database within your django project.

It contains a models.py file describing the musicbrainz database organization and a router.py file allowing read access to the musicbrainz database.

# Install

	pip install https://github.com/bsvetchine/django-musicbrainz/zipball/master

Then you should add django_musicbrainz in your INSTALLED_APPS. To do so, edit the settings.py file of your django project :

	INSTALLED_APPS = (
    		...
    		'django_musicbrainz',
	)

You have to tell Django that you will use the musicbrainz database. In your settings.py file you have to specify to set up the musicbrainz database settings.

	DATABASES = {
    		# database settings for your django project
    		'default': {
			...
    		},
    		# database settings for your local musicbrainz database
    		'musicbrainz': {
        		'ENGINE': 'django.db.backends.postgresql_psycopg2',
        		'NAME': 'musicbrainz_db',
        		'USER': 'musicbrainz',
        		'PASSWORD': '',
       		 	'HOST': '',
        		'POST': '',
   	 	}
	}

Once you've set up the musicbrainz database, you have to tell django to use the MusicbrainzRooter for the django_musicbrainz app.

	DATABASE_ROUTERS = ['django_musicbrainz.router.MusicbrainzRouter',]
