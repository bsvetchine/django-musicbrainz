class MusicbrainzRouter(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'musicbrainz':
			return 'musicbrainz'
		return None
	def db_for_write(self, model, **hints):
		return None
	def allow_relation(self, obj1, obj2, **hints):
		return None
	def allow_syncdb(self, db, model):
		if model._meta.app_label == 'musicbrainz':
			return False
		return None
