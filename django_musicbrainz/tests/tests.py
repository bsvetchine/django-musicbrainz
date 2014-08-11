from django.test import TestCase
from django.db import models
from django.db import connection

from django_musicbrainz import models as mb_models


def db_table(django_model):
    return django_model._meta.db_table


def get_field_type(db_code):
        try:
            field_type = connection.introspection.get_field_type(
                db_code, "django_musicbrainz tests")
        except KeyError:
            # if the db_code is not listed in
            # django.db.backens.postgresql_psycopg2.introspection.\
            # DatabaseIntrospection.data_types_reverse we guess that
            # the db type is a TextField
            field_type = 'TextField'
        return field_type


class DjangoMusicbrainzTest(TestCase):

    def setUp(self):
        self.cursor = connection.cursor()
        self.mb_model_list = models.get_models(mb_models)
        self.db_table_list = connection.introspection.get_table_list(
            self.cursor)

    def test_database_connection(self):
        """ Test that django app is correctly connected to musicbrainz."""

        # test that all models are "querysable"
        for model in self.mb_model_list:
            self.assertTrue(model.objects.count() >= 0)

        # test that main tables are filled
        self.assertTrue(mb_models.Artist.objects.count() > 0)
        self.assertTrue(mb_models.ReleaseGroup.objects.count() > 0)
        self.assertTrue(mb_models.Release.objects.count() > 0)
        self.assertTrue(mb_models.Track.objects.count() > 0)

    def test_matching_schema_db(self):
        """ Test that musicbrainz models matches musicbrainz db."""

        # test that nb models = nb tables in database
        self.assertEqual(
            len(self.mb_model_list),
            len(self.db_table_list)
        )

        # test that all db tables are represented by a django model
        nb_unrepresented_tables = 0
        for table in self.db_table_list:
            if not table in map(db_table, self.mb_model_list):
                nb_unrepresented_tables += 1
        self.assertEqual(nb_unrepresented_tables, 0)

        # test that all models are related to a db table that exists
        nb_unlinked_models = 0
        for table in map(db_table, self.mb_model_list):
            if not table in self.db_table_list:
                nb_unlinked_models += 1
        self.assertEqual(nb_unlinked_models, 0)

    def test_table_fields(self):
        """ Test that model fields are set accordingly to db table descr """

        for mb_model in self.mb_model_list:
            mb_fields = mb_model._meta.fields
            db_cols = connection.introspection.get_table_description(
                self.cursor, mb_model._meta.db_table)

            # test that the number of fields matches the number of table cols
            self.assertEqual(
                len(mb_fields),
                len(db_cols)
            )

            for i in range(0, len(mb_model._meta.fields)):
                # test that the field name corresponds to the col name
                self.assertEqual(
                    mb_fields[i].column,
                    db_cols[i].name
                )
                # test that the field type corresponds to the col type
                mb_field_type = mb_fields[i].get_internal_type()
                # small hack for ForeignKey field
                if mb_field_type == 'ForeignKey':
                    mb_field_type = u'IntegerField'
                self.assertEqual(
                    mb_field_type,
                    get_field_type(db_cols[i].type_code)
                )
