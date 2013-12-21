"""
Django Musicbrainz is a small app that allows browsing data from a local musicibrainz database within your django project.

It contains a models.py file describing the musicbrainz database organization and a router.py file allowing read access to the musicbrainz database.
"""
version = (0, 9, 0)
__version__ = '.'.join(map(str, version))
__author__  = u'Bertrand Svetchine'
