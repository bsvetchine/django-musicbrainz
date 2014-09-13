class MusicbrainzRouter(object):
    """Database router for musicbrainz database.

    You should add MusicbrainzRouter in your DATABASE_ROUTERS argument list in
    your settings file.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'django_musicbrainz':
            return 'musicbrainz'
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
        if model._meta.app_label == 'django_musicbrainz':
            return False
        return None
