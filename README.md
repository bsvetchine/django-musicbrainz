django-musicbrainz
==================

Django connector app for musicbrainz database.

## Description

django-musicbrainz is a small app that allows browsing data from a local musicibrainz database within your django project.

It contains a models.py file describing the musicbrainz database organization and a router.py file allowing read access to the musicbrainz database.

## Install

### Download project
	pip install https://github.com/bsvetchine/django-musicbrainz/zipball/master

### Update your settings.py
You should add django_musicbrainz to your INSTALLED_APPS. To do so, edit the settings.py file of your django project :

	INSTALLED_APPS = (
    		...
    		'django_musicbrainz',
	)

You have to tell Django that you will use the musicbrainz database. In your settings.py file you have to set up the musicbrainz database settings.

	DATABASES = {

    		# database settings for your django project
    		'default': {
			...
    		},

    		# database settings for your local musicbrainz database
    		'musicbrainz': {
        		'ENGINE': 'django.db.backends.postgresql_psycopg2', # Musicbrainz is a postgresql database
        		'NAME': 'musicbrainz_db', # The local musicbrainz database name
        		'USER': 'musicbrainz', # The system user accessing to musicbrainz database
        		'PASSWORD': '',
       		 	'HOST': '',
        		'POST': '',
   	 	}

	}

Once you've set up the Musicbrainz database, you have to tell Django to use the MusicbrainzRooter for the django_musicbrainz app.
The MusicbrainzRooter gives read only access to the musicbrainz database (it only applies for the django_musicbrainz app).

	DATABASE_ROUTERS = ['django_musicbrainz.router.MusicbrainzRouter',]

## Check setup

Launch the django shell of your application

	python manage.py shell

And start browsing musicbrainz database

	from django_musicbrainz.models import Artist
	Artist.objects.count()
	Artist.objects.filter(name="Metallica")

	from django_musicbrainz.models import ReleaseGroup
	ReleaseGroup.objects.filter(name="Nevermind")

	from django_musicbrainz.models import Track
	Track.objects.filter(name="Seek and Destroy")

For more information about the musicbrainz database structure, you can have a look on [the official musicbrainz documentation here](http://musicbrainz.org/doc/MusicBrainz_Database/Schema).	
