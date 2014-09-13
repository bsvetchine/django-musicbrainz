"""
Test file for django_musicbrainz app.

Do not forget to use the custom the MusicbrainzTestSuiteRunner ! In your
django settings file add :
TEST_RUNNER = 'django_musicbrainz.tests.simple.MusicbrainzTestSuiteRunner'"""
import itertools

from django.test import TestCase
from django.db import models
from django.db import connection

from django_musicbrainz import models as mb_models


postgresql_views = (
    u'area_containment',
    u'recording_series',
    u'release_event',
    u'release_group_series',
    u'release_series',
    u'work_series'
)


def is_db_view(db_table):
    """ Musicbrainz_db uses postgresql views."""
    if db_table in postgresql_views:
        return True
    return False


def get_db_table(django_model):
    return django_model._meta.db_table


def get_field_type(db_code):
        """ Returns the Django field type according to one db_code."""
        try:
            field_type = connection.introspection.get_field_type(
                db_code, 'django_musicbrainz tests')
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
        for db_view in postgresql_views:
            self.db_table_list.remove(db_view)

    def test_database_connection(self):
        """Test that django app is correctly connected to musicbrainz db."""

        # test that all models are "querysable"
        for model in self.mb_model_list:
            model.objects.all()

        # test that main tables are filled
        self.assertTrue(mb_models.Artist.objects.count() > 0)
        self.assertTrue(mb_models.ReleaseGroup.objects.count() > 0)
        self.assertTrue(mb_models.Release.objects.count() > 0)
        self.assertTrue(mb_models.Track.objects.count() > 0)

    def test_db_models_correspondance(self):
        """Test that all db tables are represented by a django model."""

        # test that nb models = nb tables in database
        self.assertEqual(
            len(self.mb_model_list),
            len(self.db_table_list)
        )

        # test that all db tables are represented by a django model
        nb_unrepresented_tables = 0
        for table in self.db_table_list:
            if table not in map(get_db_table, self.mb_model_list):
                nb_unrepresented_tables += 1
        self.assertEqual(nb_unrepresented_tables, 0)

        # test that all models are related to a db table that exists
        nb_unlinked_models = 0
        for table in map(get_db_table, self.mb_model_list):
            if table not in self.db_table_list:
                nb_unlinked_models += 1
        self.assertEqual(nb_unlinked_models, 0)

    def test_primary_keys(self):
        """
        Test that no primary key is auto created by Django.

        If the primary_key argument is not explicitaly set in one of the
        models field Django will automaticaly consider a column named id
        as the primary key. Which is not what we want here.
        """

        for mb_model in self.mb_model_list:
            self.assertFalse(mb_model._meta.pk.auto_created)

    def test_field_names(self):
        """Test that each db table column are represented by a model field."""

        for mb_model in self.mb_model_list:
            mb_fields = mb_model._meta.fields
            db_cols = connection.introspection.get_table_description(
                self.cursor, mb_model._meta.db_table)

            for i in range(0, len(mb_model._meta.fields)):
                self.assertEqual(
                    mb_fields[i].column,
                    db_cols[i].name
                )

    def test_field_types(self):
        """Test that field type are set accordingly to db column type."""

        for mb_model in self.mb_model_list:
            mb_fields = mb_model._meta.fields
            db_cols = connection.introspection.get_table_description(
                self.cursor, mb_model._meta.db_table)
            db_relations = connection.introspection.get_relations(
                self.cursor, mb_model._meta.db_table)

            for i in range(0, len(mb_model._meta.fields)):
                expected_field_type = None
                if db_relations.get(i):
                    expected_field_type = u'ForeignKey'
                else:
                    expected_field_type = get_field_type(db_cols[i].type_code)

                self.assertEqual(
                    mb_fields[i].get_internal_type(),
                    expected_field_type
                )

    def test_unique_together(self):
        """
        Test that unique_together is correctly set.

        As Django doesn't support composite primary key :
        https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys and
        https://code.djangoproject.com/ticket/373

        We set one of the field as primary_key and we manage unicity with
        unique_together option."""

        for mb_model in self.mb_model_list:
            indexes = connection.introspection.get_indexes(
                self.cursor, mb_model._meta.db_table)
            if not indexes and not is_db_view(mb_model._meta.db_table):
                self.assertTrue(mb_model._meta.unique_together)

    def get_foreign_keys(self, model):
        """Returns a dictionnary presenting all the fk given a model.

        We return a dictionnary (wich keys are Foreignkey fields and values
        the related classes) of all foreign keys of the given model.
        We exclude the Link attribute here because it is specific to
        musicbrainz database."""

        fks = {}
        for field in model._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                related_class = field.foreign_related_fields[0].model
                fks.update({
                    field: related_class
                })
        return fks

    def table_contains_elements(self, model):
        """Returns True if the db table is filled."""
        if model.objects.count() > 1:
            return True
        return False

    def get_intermediate_models(self):
        """
        Returns a list of all many to many intermediate models.

        We consider that every model that has a unique_together set as
        a custom intermediate model.
        Other many to many relationships are listed here :
        https://musicbrainz.org/relationships"""

        intermediate_models = []
        for mb_model in self.mb_model_list:
            fks = self.get_foreign_keys(mb_model)
            # add models with fields that are unique together
            if (
                    len(fks) >= 2 and
                    mb_model._meta.unique_together and
                    mb_model._meta.db_table[-4:] != "_raw" and
                    mb_model._meta.db_table[-8:] != "_deleted"
            ):
                intermediate_models.append(mb_model)
            # add models with a ForeignKey set to Link
            elif (
                    len(fks) >= 3 and
                    mb_models.Link in fks.values()
            ):
                intermediate_models.append(mb_model)
        return intermediate_models

    def presume_models_used_by_m2m(self, fks):
        if len(fks) <= 2:
            return fks.values()
        models = []
        for model in fks.values():
            if model != mb_models.Link:
                models.append(model)
        return models

    def is_m2m_set(self, int_model, model1, model2):
        """Test if a many_to_many field is set from model1 to model2."""
        for m2m in model1._meta.many_to_many:
            if m2m.rel.to == model2 and m2m.rel.through == int_model:
                return True
        for m2m in model2._meta.many_to_many:
            if m2m.rel.to == model1 and m2m.rel.through == int_model:
                return True
        return False

    def test_that_all_m2m_are_set(self):
        """Test that there is a ManyToManyField everytime it should."""
        m2m_forgotten = 0
        for int_model in self.get_intermediate_models():
            fks = self.get_foreign_keys(int_model)
            models = self.presume_models_used_by_m2m(fks)
            for model1, model2 in itertools.combinations(models, 2):
                if not self.is_m2m_set(int_model, model1, model2):
                    m2m_forgotten += 1
        self.assertEqual(m2m_forgotten, 0)
