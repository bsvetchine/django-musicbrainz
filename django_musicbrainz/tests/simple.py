from django.test import runner


class MusicbrainzTestSuiteRunner(runner.DiscoverRunner):

    def setup_databases(self, **kwargs):
        # We want to apply unit tests against the musicbrainz database
        pass

    def teardown_databases(self, old_config, **kwargs):
        # Do not destroy our beautiful musicbrainz database
        pass
