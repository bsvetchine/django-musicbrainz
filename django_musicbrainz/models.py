from __future__ import unicode_literals

from django.db import models

CHARACTER_VARYING_MAX_LENGTH = 10000


class Annotation(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey('Editor', db_column='editor')
    text = models.TextField(blank=True)
    changelog = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annotation'


class Application(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey('Editor', db_column='owner')
    name = models.TextField()
    oauth_id = models.TextField(unique=True)
    oauth_secret = models.TextField()
    oauth_redirect_uri = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'application'


class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    type = models.ForeignKey(
        'AreaType', db_column='type', blank=True, null=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    ended = models.BooleanField()
    comment = models.CharField(max_length=255)

    annotations = models.ManyToManyField(
        'Annotation', through='AreaAnnotation')
    areas = models.ManyToManyField('Area', through='LAreaArea')
    edits = models.ManyToManyField('Edit', through='EditArea')
    urls = models.ManyToManyField('Url', through='LAreaUrl')

    class Meta:
        managed = False
        db_table = 'area'


class AreaAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.ForeignKey(Area, db_column='area')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey(
        'AreaAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'area_alias'


class AreaAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'area_alias_type'


class AreaAnnotation(models.Model):
    area = models.ForeignKey(Area, db_column='area', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'area_annotation'
        unique_together = ('area', 'annotation')


class AreaGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Area)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_gid_redirect'


class AreaType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'area_type'


class Artist(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(
        unique=True, max_length=CHARACTER_VARYING_MAX_LENGTH)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    type = models.ForeignKey(
        'ArtistType', db_column='type', blank=True, null=True)
    area = models.ForeignKey(Area, db_column='area', blank=True, null=True)
    gender = models.ForeignKey(
        'Gender', db_column='gender', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    ended = models.BooleanField()
    begin_area = models.ForeignKey(
        Area, db_column='begin_area',
        related_name='begin_artist_set', blank=True, null=True)
    end_area = models.ForeignKey(
        Area, db_column='end_area',
        related_name='end_artist_set', blank=True, null=True)

    annotations = models.ManyToManyField(
        'Annotation', through='ArtistAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaArtist')
    artists = models.ManyToManyField(
        'Artist', through='LArtistArtist')
    edits = models.ManyToManyField(
        'Edit', through='EditArtist')
    instruments = models.ManyToManyField(
        'Instrument', through='LArtistInstrument')
    labels = models.ManyToManyField(
        'Label', through='LArtistLabel')
    places = models.ManyToManyField(
        'Place', through='LArtistPlace')
    recordings = models.ManyToManyField(
        'Recording', through='LArtistRecording')
    releases = models.ManyToManyField(
        'Release', through='LArtistRelease')
    release_groups = models.ManyToManyField(
        'ReleaseGroup', through='LArtistReleaseGroup')
    series = models.ManyToManyField(
        'Series', through='LArtistSeries')
    tags = models.ManyToManyField('Tag', through='ArtistTag')
    urls = models.ManyToManyField('Url', through='LArtistUrl')
    works = models.ManyToManyField('Work', through='LArtistWork')

    class Meta:
        managed = False
        db_table = 'artist'


class ArtistAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    artist = models.ForeignKey(Artist, db_column='artist')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey(
        'ArtistAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'artist_alias'


class ArtistAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'artist_alias_type'


class ArtistAnnotation(models.Model):
    artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'artist_annotation'
        unique_together = ('artist', 'annotation')


class ArtistCredit(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_count = models.SmallIntegerField()
    ref_count = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    artists = models.ManyToManyField(
        'Artist', through='ArtistCreditName')

    class Meta:
        managed = False
        db_table = 'artist_credit'


class ArtistCreditName(models.Model):
    artist_credit = models.ForeignKey(
        ArtistCredit, db_column='artist_credit', primary_key=True)
    position = models.SmallIntegerField()
    artist = models.ForeignKey(Artist, db_column='artist')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    join_phrase = models.TextField()

    class Meta:
        managed = False
        db_table = 'artist_credit_name'
        unique_together = ('artist_credit', 'position')


class ArtistDeletion(models.Model):
    gid = models.TextField(primary_key=True)
    last_known_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    last_known_comment = models.TextField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'artist_deletion'


class ArtistGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Artist)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_gid_redirect'


class ArtistIpi(models.Model):
    artist = models.ForeignKey(
        Artist, db_column='artist', primary_key=True)
    ipi = models.CharField(max_length=11)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_ipi'
        unique_together = ('artist', 'ipi')


class ArtistIsni(models.Model):
    artist = models.ForeignKey(
        Artist, db_column='artist', primary_key=True)
    isni = models.CharField(max_length=16)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_isni'
        unique_together = ('artist', 'isni')


class ArtistMeta(models.Model):
    id = models.ForeignKey(Artist, db_column='id', primary_key=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_meta'


class ArtistRatingRaw(models.Model):
    artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
    editor = models.ForeignKey('Editor', db_column='editor')
    rating = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'artist_rating_raw'
        unique_together = ('artist', 'editor')


class ArtistTag(models.Model):
    artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist_tag'
        unique_together = ('artist', 'tag')


class ArtistTagRaw(models.Model):
    artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')

    class Meta:
        managed = False
        db_table = 'artist_tag_raw'
        unique_together = ('artist', 'editor', 'tag')


class ArtistType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'artist_type'


class AutoeditorElection(models.Model):
    id = models.IntegerField(primary_key=True)
    candidate = models.ForeignKey(
        'Editor', db_column='candidate',
        related_name='candidate_autoeditorelection_set')
    proposer = models.ForeignKey(
        'Editor', db_column='proposer',
        related_name='proposer_autoeditorelection_set')
    seconder_1 = models.ForeignKey(
        'Editor', db_column='seconder_1',
        related_name='seconder_1_autoeditorelection_set',
        blank=True, null=True)
    seconder_2 = models.ForeignKey(
        'Editor', db_column='seconder_2',
        related_name='seconder_2_autoeditorelection_set',
        blank=True, null=True)
    status = models.IntegerField()
    yes_votes = models.IntegerField()
    no_votes = models.IntegerField()
    propose_time = models.DateTimeField()
    open_time = models.DateTimeField(blank=True, null=True)
    close_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'autoeditor_election'


class AutoeditorElectionVote(models.Model):
    id = models.IntegerField(primary_key=True)
    autoeditor_election = models.ForeignKey(
        AutoeditorElection, db_column='autoeditor_election')
    voter = models.ForeignKey('Editor', db_column='voter')
    vote = models.IntegerField()
    vote_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'autoeditor_election_vote'


class Cdtoc(models.Model):
    id = models.IntegerField(primary_key=True)
    discid = models.CharField(unique=True, max_length=28)
    freedb_id = models.CharField(max_length=8)
    track_count = models.IntegerField()
    leadout_offset = models.IntegerField()
    track_offset = models.TextField()
    degraded = models.BooleanField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cdtoc'


class CdtocRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.ForeignKey('ReleaseRaw', db_column='release')
    discid = models.CharField(max_length=28)
    track_count = models.IntegerField()
    leadout_offset = models.IntegerField()
    track_offset = models.TextField()

    class Meta:
        managed = False
        db_table = 'cdtoc_raw'


class CountryArea(models.Model):
    area = models.ForeignKey(Area, db_column='area', primary_key=True)

    class Meta:
        managed = False
        db_table = 'country_area'


class Edit(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey('Editor', db_column='editor')
    type = models.SmallIntegerField()
    status = models.SmallIntegerField()
    data = models.TextField()
    yes_votes = models.IntegerField()
    no_votes = models.IntegerField()
    autoedit = models.SmallIntegerField()
    open_time = models.DateTimeField(blank=True, null=True)
    close_time = models.DateTimeField(blank=True, null=True)
    expire_time = models.DateTimeField()
    language = models.ForeignKey(
        'Language', db_column='language', blank=True, null=True)
    quality = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'edit'


class EditArea(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    area = models.ForeignKey(Area, db_column='area')

    class Meta:
        managed = False
        db_table = 'edit_area'
        unique_together = ('edit', 'area')


class EditArtist(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    artist = models.ForeignKey(Artist, db_column='artist')
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'edit_artist'
        unique_together = ('edit', 'artist')


class EditInstrument(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    instrument = models.ForeignKey('Instrument', db_column='instrument')

    class Meta:
        managed = False
        db_table = 'edit_instrument'
        unique_together = ('edit', 'instrument')


class EditLabel(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    label = models.ForeignKey('Label', db_column='label')
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'edit_label'
        unique_together = ('edit', 'label')


class EditNote(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey('Editor', db_column='editor')
    edit = models.ForeignKey(Edit, db_column='edit')
    text = models.TextField()
    post_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edit_note'


class EditPlace(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    place = models.ForeignKey('Place', db_column='place')

    class Meta:
        managed = False
        db_table = 'edit_place'
        unique_together = ('edit', 'place')


class EditRecording(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    recording = models.ForeignKey('Recording', db_column='recording')

    class Meta:
        managed = False
        db_table = 'edit_recording'
        unique_together = ('edit', 'recording')


class EditRelease(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    release = models.ForeignKey('Release', db_column='release')

    class Meta:
        managed = False
        db_table = 'edit_release'
        unique_together = ('edit', 'release')


class EditReleaseGroup(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    release_group = models.ForeignKey(
        'ReleaseGroup', db_column='release_group')

    class Meta:
        managed = False
        db_table = 'edit_release_group'
        unique_together = ('edit', 'release_group')


class EditSeries(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    series = models.ForeignKey('Series', db_column='series')

    class Meta:
        managed = False
        db_table = 'edit_series'
        unique_together = ('edit', 'series')


class EditUrl(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    url = models.ForeignKey('Url', db_column='url')

    class Meta:
        managed = False
        db_table = 'edit_url'
        unique_together = ('edit', 'url')


class EditWork(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    work = models.ForeignKey('Work', db_column='work')

    class Meta:
        managed = False
        db_table = 'edit_work'
        unique_together = ('edit', 'work')


class Editor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    privs = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=64, blank=True)
    website = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    member_since = models.DateTimeField(blank=True, null=True)
    email_confirm_date = models.DateTimeField(blank=True, null=True)
    last_login_date = models.DateTimeField(blank=True, null=True)
    edits_accepted = models.IntegerField(blank=True, null=True)
    edits_rejected = models.IntegerField(blank=True, null=True)
    auto_edits_accepted = models.IntegerField(blank=True, null=True)
    edits_failed = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.ForeignKey(
        'Gender', db_column='gender', blank=True, null=True)
    area = models.ForeignKey(Area, db_column='area', blank=True, null=True)
    password = models.CharField(max_length=128)
    ha1 = models.CharField(max_length=32)
    deleted = models.BooleanField()

    artists_subscribed = models.ManyToManyField(
        'Artist', through='EditorSubscribeArtist')
    artists_watched = models.ManyToManyField(
        'Artist', through='EditorWatchArtist')
    artists_deleted = models.ManyToManyField(
        'ArtistDeletion', through='EditorSubscribeArtistDeleted')
    labels_deleted = models.ManyToManyField(
        'LabelDeletion', through='EditorSubscribeLabelDeleted')
    languages = models.ManyToManyField('Language', through='EditorLanguage')
    release_group_types_watched = models.ManyToManyField(
        'ReleaseGroupPrimaryType', through='EditorWatchReleaseGroupType')
    release_status_watched = models.ManyToManyField(
        'ReleaseStatus', through='EditorWatchReleaseStatus')
    series_deleted = models.ManyToManyField(
        'SeriesDeletion', through='EditorSubscribeSeriesDeleted')

    class Meta:
        managed = False
        db_table = 'editor'


class EditorCollection(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    public = models.BooleanField()
    description = models.TextField()

    releases = models.ManyToManyField(
        'Release', through='EditorCollectionRelease')

    class Meta:
        managed = False
        db_table = 'editor_collection'


class EditorCollectionRelease(models.Model):
    collection = models.ForeignKey(
        EditorCollection, db_column='collection', primary_key=True)
    release = models.ForeignKey('Release', db_column='release')

    class Meta:
        managed = False
        db_table = 'editor_collection_release'
        unique_together = ('collection', 'release')


class EditorLanguage(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    language = models.ForeignKey('Language', db_column='language')
    fluency = models.TextField()

    class Meta:
        managed = False
        db_table = 'editor_language'
        unique_together = ('editor', 'language')


class EditorOauthToken(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    application = models.ForeignKey(Application, db_column='application')
    authorization_code = models.TextField(blank=True)
    refresh_token = models.TextField(unique=True, blank=True)
    access_token = models.TextField(unique=True, blank=True)
    expire_time = models.DateTimeField()
    scope = models.IntegerField()
    granted = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'editor_oauth_token'


class EditorPreference(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'editor_preference'


class EditorSubscribeArtist(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    artist = models.ForeignKey(Artist, db_column='artist')
    last_edit_sent = models.ForeignKey(Edit, db_column='last_edit_sent')

    class Meta:
        managed = False
        db_table = 'editor_subscribe_artist'


class EditorSubscribeArtistDeleted(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    gid = models.ForeignKey(ArtistDeletion, db_column='gid')
    deleted_by = models.ForeignKey(Edit, db_column='deleted_by')

    class Meta:
        managed = False
        db_table = 'editor_subscribe_artist_deleted'
        unique_together = ('editor', 'gid')


class EditorSubscribeCollection(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    collection = models.IntegerField()
    last_edit_sent = models.IntegerField()
    available = models.BooleanField()
    last_seen_name = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'editor_subscribe_collection'


class EditorSubscribeEditor(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    subscribed_editor = models.ForeignKey(
        Editor, db_column='subscribed_editor',
        related_name='subscribed_editor_set')
    last_edit_sent = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'editor_subscribe_editor'


class EditorSubscribeLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    label = models.ForeignKey('Label', db_column='label')
    last_edit_sent = models.ForeignKey(Edit, db_column='last_edit_sent')

    class Meta:
        managed = False
        db_table = 'editor_subscribe_label'


class EditorSubscribeLabelDeleted(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    gid = models.ForeignKey('LabelDeletion', db_column='gid')
    deleted_by = models.ForeignKey(Edit, db_column='deleted_by')

    class Meta:
        managed = False
        db_table = 'editor_subscribe_label_deleted'
        unique_together = ('editor', 'gid')


class EditorSubscribeSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    series = models.ForeignKey('Series', db_column='series')
    last_edit_sent = models.ForeignKey(Edit, db_column='last_edit_sent')

    class Meta:
        managed = False
        db_table = 'editor_subscribe_series'


class EditorSubscribeSeriesDeleted(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    gid = models.ForeignKey('SeriesDeletion', db_column='gid')
    deleted_by = models.ForeignKey(Edit, db_column='deleted_by')

    class Meta:
        managed = False
        db_table = 'editor_subscribe_series_deleted'
        unique_together = ('editor', 'gid')


class EditorWatchArtist(models.Model):
    artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')

    class Meta:
        managed = False
        db_table = 'editor_watch_artist'
        unique_together = ('artist', 'editor')


class EditorWatchPreferences(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    notify_via_email = models.BooleanField()
    notification_timeframe = models.TextField()
    last_checked = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'editor_watch_preferences'


class EditorWatchReleaseGroupType(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    release_group_type = models.ForeignKey(
        'ReleaseGroupPrimaryType', db_column='release_group_type')

    class Meta:
        managed = False
        db_table = 'editor_watch_release_group_type'
        unique_together = ('editor', 'release_group_type')


class EditorWatchReleaseStatus(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    release_status = models.ForeignKey(
        'ReleaseStatus', db_column='release_status')

    class Meta:
        managed = False
        db_table = 'editor_watch_release_status'
        unique_together = ('editor', 'release_status')


class Gender(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'gender'


class Instrument(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    type = models.ForeignKey(
        'InstrumentType', db_column='type', blank=True, null=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=255)
    description = models.TextField()

    annotations = models.ManyToManyField(
        'Annotation', through='InstrumentAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaInstrument')
    edits = models.ManyToManyField(
        'Edit', through='EditInstrument')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentInstrument')
    urls = models.ManyToManyField(
        'Url', through='LInstrumentUrl')

    class Meta:
        managed = False
        db_table = 'instrument'


class InstrumentAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    instrument = models.ForeignKey(Instrument, db_column='instrument')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey(
        'InstrumentAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instrument_alias'


class InstrumentAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'instrument_alias_type'


class InstrumentAnnotation(models.Model):
    instrument = models.ForeignKey(
        Instrument, db_column='instrument', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'instrument_annotation'
        unique_together = ('instrument', 'annotation')


class InstrumentGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Instrument)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instrument_gid_redirect'


class InstrumentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'instrument_type'


class Iso31661(models.Model):
    area = models.ForeignKey(Area, db_column='area')
    code = models.CharField(primary_key=True, max_length=2)

    class Meta:
        managed = False
        db_table = 'iso_3166_1'


class Iso31662(models.Model):
    area = models.ForeignKey(Area, db_column='area')
    code = models.CharField(primary_key=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'iso_3166_2'


class Iso31663(models.Model):
    area = models.ForeignKey(Area, db_column='area')
    code = models.CharField(primary_key=True, max_length=4)

    class Meta:
        managed = False
        db_table = 'iso_3166_3'


class Isrc(models.Model):
    id = models.IntegerField(primary_key=True)
    recording = models.ForeignKey('Recording', db_column='recording')
    isrc = models.CharField(max_length=12)
    source = models.SmallIntegerField(blank=True, null=True)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'isrc'


class Iswc(models.Model):
    id = models.IntegerField(primary_key=True)
    work = models.ForeignKey('Work', db_column='work')
    iswc = models.CharField(max_length=15, blank=True)
    source = models.SmallIntegerField(blank=True, null=True)
    edits_pending = models.IntegerField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'iswc'


class LAreaArea(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        Area, db_column='entity0',
        related_name='entity0_lareaarea_set')
    entity1 = models.ForeignKey(
        Area, db_column='entity1',
        related_name='entity1_lareaarea_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_area'


class LAreaArtist(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        Area, db_column='entity0',
        related_name='entity0_lareaartist_set')
    entity1 = models.ForeignKey(
        Artist, db_column='entity1',
        related_name='entity1_lareaartist_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_artist'


class LAreaInstrument(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey(Instrument, db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_instrument'


class LAreaLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('Label', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_label'


class LAreaPlace(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('Place', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_place'


class LAreaRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('Recording', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_recording'


class LAreaRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('Release', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_release'


class LAreaReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_release_group'


class LAreaSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_series'


class LAreaUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_url'


class LAreaWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Area, db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_area_work'


class LArtistArtist(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        Artist, db_column='entity0',
        related_name='entity0_lartistartist_set')
    entity1 = models.ForeignKey(
        Artist, db_column='entity1',
        related_name='entity1_lartistartist_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_artist'


class LArtistInstrument(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey(Instrument, db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_instrument'


class LArtistLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('Label', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_label'


class LArtistPlace(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('Place', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_place'


class LArtistRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('Recording', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_recording'


class LArtistRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('Release', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_release'


class LArtistReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_release_group'


class LArtistSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_series'


class LArtistUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_url'


class LArtistWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Artist, db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_artist_work'


class LInstrumentInstrument(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        Instrument, db_column='entity0',
        related_name='entity0_linstrumentinstrument_set')
    entity1 = models.ForeignKey(
        Instrument, db_column='entity1',
        related_name='entity1_linstrumentinstrument_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_instrument'


class LInstrumentLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('Label', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_label'


class LInstrumentPlace(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('Place', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_place'


class LInstrumentRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('Recording', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_recording'


class LInstrumentRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('Release', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_release'


class LInstrumentReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_release_group'


class LInstrumentSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_series'


class LInstrumentUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_url'


class LInstrumentWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(Instrument, db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_instrument_work'


class LLabelLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'Label', db_column='entity0',
        related_name='entity0_llabellabel_set')
    entity1 = models.ForeignKey(
        'Label', db_column='entity1',
        related_name='entity1_llabellabel_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_label'


class LLabelPlace(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0')
    entity1 = models.ForeignKey('Place', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_place'


class LLabelRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0')
    entity1 = models.ForeignKey('Recording', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_recording'


class LLabelRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0')
    entity1 = models.ForeignKey('Release', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_release'


class LLabelReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_release_group'


class LLabelSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_series'


class LLabelUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_url'


class LLabelWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_label_work'


class LPlacePlace(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'Place', db_column='entity0',
        related_name='entity0_lplaceplace_set')
    entity1 = models.ForeignKey(
        'Place', db_column='entity1',
        related_name='entity1_lplaceplace_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_place_place'


class LPlaceRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0')
    entity1 = models.ForeignKey('Recording', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_place_recording'


class LPlaceRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0')
    entity1 = models.ForeignKey('Release', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_place_release'


class LPlaceReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_place_release_group'


class LPlaceSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_place_series'


class LPlaceUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_place_url'


class LPlaceWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_place_work'


class LRecordingRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'Recording', db_column='entity0',
        related_name='entity0_lrecordingrecording_set')
    entity1 = models.ForeignKey(
        'Recording', db_column='entity1',
        related_name='entity1_lrecordingrecording_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_recording_recording'


class LRecordingRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0')
    entity1 = models.ForeignKey('Release', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_recording_release'


class LRecordingReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_recording_release_group'


class LRecordingSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_recording_series'


class LRecordingUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_recording_url'


class LRecordingWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_recording_work'


class LReleaseGroupReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'ReleaseGroup', db_column='entity0',
        related_name='entity0_lreleasegroupreleasegroup_set')
    entity1 = models.ForeignKey(
        'ReleaseGroup', db_column='entity1',
        related_name='entity1_lreleasegroupreleasegroup_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_group_release_group'


class LReleaseGroupSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('ReleaseGroup', db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_group_series'


class LReleaseGroupUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('ReleaseGroup', db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_group_url'


class LReleaseGroupWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('ReleaseGroup', db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_group_work'


class LReleaseRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'Release', db_column='entity0',
        related_name='entity0_lreleaserelease_set')
    entity1 = models.ForeignKey(
        'Release', db_column='entity1',
        related_name='entity1_lreleaserelease_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_release'


class LReleaseReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_release_group'


class LReleaseSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0')
    entity1 = models.ForeignKey('Series', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_series'


class LReleaseUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_url'


class LReleaseWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_release_work'


class LSeriesSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'Series', db_column='entity0',
        related_name='entity0_lseriesseries_set')
    entity1 = models.ForeignKey(
        'Series', db_column='entity1',
        related_name='entity1_lseriesseries_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_series_series'


class LSeriesUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Series', db_column='entity0')
    entity1 = models.ForeignKey('Url', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_series_url'


class LSeriesWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Series', db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_series_work'


class LUrlUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'Url', db_column='entity0',
        related_name='entity0_lurlurl_set')
    entity1 = models.ForeignKey(
        'Url', db_column='entity1',
        related_name='entity1_lurlurl_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_url_url'


class LUrlWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Url', db_column='entity0')
    entity1 = models.ForeignKey('Work', db_column='entity1')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_url_work'


class LWorkWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey(
        'Work', db_column='entity0',
        related_name='entity0_lworkwork_set')
    entity1 = models.ForeignKey(
        'Work', db_column='entity1',
        related_name='entity1_lworkwork_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    link_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'l_work_work'


class Label(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(
        unique=True, max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    label_code = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey(
        'LabelType', db_column='type', blank=True, null=True)
    area = models.ForeignKey(Area, db_column='area', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    ended = models.BooleanField()

    annotations = models.ManyToManyField(
        'Annotation', through='LabelAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaLabel')
    edits = models.ManyToManyField(
        'Edit', through='EditLabel')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentLabel')
    labels = models.ManyToManyField('Label', through='LLabelLabel')
    places = models.ManyToManyField('Place', through='LLabelPlace')
    series = models.ManyToManyField('Series', through='LLabelSeries')
    tags = models.ManyToManyField('Tag', through='LabelTag')
    urls = models.ManyToManyField('Url', through='LLabelUrl')
    works = models.ManyToManyField('Work', through='LLabelWork')

    class Meta:
        managed = False
        db_table = 'label'


class LabelAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.ForeignKey(Label, db_column='label')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey(
        'LabelAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'label_alias'


class LabelAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'label_alias_type'


class LabelAnnotation(models.Model):
    label = models.ForeignKey(Label, db_column='label', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'label_annotation'
        unique_together = ('label', 'annotation')


class LabelDeletion(models.Model):
    gid = models.TextField(primary_key=True)
    last_known_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    last_known_comment = models.TextField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'label_deletion'


class LabelGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Label)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'label_gid_redirect'


class LabelIpi(models.Model):
    label = models.ForeignKey(Label, db_column='label', primary_key=True)
    ipi = models.CharField(max_length=11)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'label_ipi'
        unique_together = ('label', 'ipi')


class LabelIsni(models.Model):
    label = models.ForeignKey(Label, db_column='label', primary_key=True)
    isni = models.CharField(max_length=16)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'label_isni'
        unique_together = ('label', 'isni')


class LabelMeta(models.Model):
    id = models.ForeignKey(Label, db_column='id', primary_key=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'label_meta'


class LabelRatingRaw(models.Model):
    label = models.ForeignKey(Label, db_column='label', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    rating = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'label_rating_raw'
        unique_together = ('label', 'editor')


class LabelTag(models.Model):
    label = models.ForeignKey(Label, db_column='label', primary_key=True)
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'label_tag'
        unique_together = ('label', 'tag')


class LabelTagRaw(models.Model):
    label = models.ForeignKey(Label, db_column='label', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')

    class Meta:
        managed = False
        db_table = 'label_tag_raw'
        unique_together = ('label', 'editor', 'tag')


class LabelType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'label_type'


class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    iso_code_2t = models.CharField(unique=True, max_length=3, blank=True)
    iso_code_2b = models.CharField(unique=True, max_length=3, blank=True)
    iso_code_1 = models.CharField(unique=True, max_length=2, blank=True)
    name = models.CharField(max_length=100)
    frequency = models.IntegerField()
    iso_code_3 = models.CharField(unique=True, max_length=3, blank=True)

    class Meta:
        managed = False
        db_table = 'language'


class Link(models.Model):
    id = models.IntegerField(primary_key=True)
    link_type = models.ForeignKey('LinkType', db_column='link_type')
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    attribute_count = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    ended = models.BooleanField()

    creditable_attribute_types = models.ManyToManyField(
        'LinkCreditableAttributeType', through='LinkAttributeCredit')
    attribute_types = models.ManyToManyField(
        'LinkAttributeType', through='LinkAttribute')
    text_attribute_types = models.ManyToManyField(
        'LinkTextAttributeType', through='LinkAttributeTextValue')

    class Meta:
        managed = False
        db_table = 'link'


class LinkAttribute(models.Model):
    link = models.ForeignKey(Link, db_column='link', primary_key=True)
    attribute_type = models.ForeignKey(
        'LinkAttributeType', db_column='attribute_type')
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_attribute'
        unique_together = ('link', 'attribute_type')


class LinkAttributeCredit(models.Model):
    link = models.ForeignKey(Link, db_column='link', primary_key=True)
    attribute_type = models.ForeignKey(
        'LinkCreditableAttributeType', db_column='attribute_type')
    credited_as = models.TextField()

    class Meta:
        managed = False
        db_table = 'link_attribute_credit'
        unique_together = ('link', 'attribute_type')


class LinkAttributeTextValue(models.Model):
    link = models.ForeignKey(Link, db_column='link', primary_key=True)
    attribute_type = models.ForeignKey(
        'LinkTextAttributeType', db_column='attribute_type')
    text_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'link_attribute_text_value'
        unique_together = ('link', 'attribute_type')


class LinkAttributeType(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True,
        related_name='parent_linkattributetype_set')
    root = models.ForeignKey(
        'self', db_column='root',
        related_name='root_linkattributetype_set')
    child_order = models.IntegerField()
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_attribute_type'


class LinkCreditableAttributeType(models.Model):
    attribute_type = models.ForeignKey(
        LinkAttributeType, db_column='attribute_type', primary_key=True)

    class Meta:
        managed = False
        db_table = 'link_creditable_attribute_type'


class LinkTextAttributeType(models.Model):
    attribute_type = models.ForeignKey(
        LinkAttributeType, db_column='attribute_type', primary_key=True)

    class Meta:
        managed = False
        db_table = 'link_text_attribute_type'


class LinkType(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    gid = models.TextField(unique=True)
    entity_type0 = models.CharField(max_length=50)
    entity_type1 = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link_phrase = models.CharField(max_length=255)
    reverse_link_phrase = models.CharField(max_length=255)
    long_link_phrase = models.CharField(max_length=255)
    priority = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    is_deprecated = models.BooleanField()
    has_dates = models.BooleanField()
    entity0_cardinality = models.IntegerField()
    entity1_cardinality = models.IntegerField()

    attribute_types = models.ManyToManyField(
        'LinkAttributeType', through='LinkTypeAttributeType')

    class Meta:
        managed = False
        db_table = 'link_type'


class LinkTypeAttributeType(models.Model):
    link_type = models.ForeignKey(
        LinkType, db_column='link_type', primary_key=True)
    attribute_type = models.ForeignKey(
        LinkAttributeType, db_column='attribute_type')
    min = models.SmallIntegerField(blank=True, null=True)
    max = models.SmallIntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_type_attribute_type'
        unique_together = ('link_type', 'attribute_type')


class Medium(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.ForeignKey('Release', db_column='release')
    position = models.IntegerField()
    format = models.ForeignKey(
        'MediumFormat', db_column='format', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    track_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'medium'


class MediumCdtoc(models.Model):
    id = models.IntegerField(primary_key=True)
    medium = models.ForeignKey(Medium, db_column='medium')
    cdtoc = models.ForeignKey(Cdtoc, db_column='cdtoc')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medium_cdtoc'


class MediumFormat(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    year = models.SmallIntegerField(blank=True, null=True)
    has_discids = models.BooleanField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'medium_format'


class MediumIndex(models.Model):
    medium = models.ForeignKey(Medium, db_column='medium', primary_key=True)
    toc = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'medium_index'


class OrderableLinkType(models.Model):
    link_type = models.ForeignKey(
        LinkType, db_column='link_type', primary_key=True)
    direction = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'orderable_link_type'


class Place(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    type = models.ForeignKey(
        'PlaceType', db_column='type', blank=True, null=True)
    address = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    area = models.ForeignKey(Area, db_column='area', blank=True, null=True)
    coordinates = models.TextField(blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    ended = models.BooleanField()

    annotations = models.ManyToManyField(
        'Annotation', through='PlaceAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaPlace')
    edits = models.ManyToManyField(
        'Edit', through='EditPlace')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentPlace')
    places = models.ManyToManyField('Place', through='LPlacePlace')
    tags = models.ManyToManyField('Tag', through='PlaceTag')
    urls = models.ManyToManyField('Url', through='LPlaceUrl')
    works = models.ManyToManyField('Work', through='LPlaceWork')

    class Meta:
        managed = False
        db_table = 'place'


class PlaceAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    place = models.ForeignKey(Place, db_column='place')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey(
        'PlaceAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'place_alias'


class PlaceAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'place_alias_type'


class PlaceAnnotation(models.Model):
    place = models.ForeignKey(Place, db_column='place', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'place_annotation'
        unique_together = ('place', 'annotation')


class PlaceGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Place)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place_gid_redirect'


class PlaceTag(models.Model):
    place = models.ForeignKey(Place, db_column='place', primary_key=True)
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place_tag'
        unique_together = ('place', 'tag')


class PlaceTagRaw(models.Model):
    place = models.ForeignKey(Place, db_column='place', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')

    class Meta:
        managed = False
        db_table = 'place_tag_raw'
        unique_together = ('place', 'editor', 'tag')


class PlaceType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'place_type'


class Recording(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey(ArtistCredit, db_column='artist_credit')
    length = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    video = models.BooleanField()

    annotations = models.ManyToManyField(
        'Annotation', through='RecordingAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaRecording')
    edits = models.ManyToManyField(
        'Edit', through='EditRecording')
    labels = models.ManyToManyField(
        'Label', through='LLabelRecording')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentRecording')
    places = models.ManyToManyField(
        'Place', through='LPlaceRecording')
    recording = models.ManyToManyField(
        'Recording', through='LRecordingRecording')
    series = models.ManyToManyField(
        'Series', through='LRecordingSeries')
    tags = models.ManyToManyField(
        'Tag', through='RecordingTag')
    urls = models.ManyToManyField(
        'Url', through='LRecordingUrl')
    work = models.ManyToManyField(
        'Work', through='LRecordingWork')

    class Meta:
        managed = False
        db_table = 'recording'


class RecordingAnnotation(models.Model):
    recording = models.ForeignKey(
        Recording, db_column='recording', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'recording_annotation'
        unique_together = ('recording', 'annotation')


class RecordingGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Recording)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recording_gid_redirect'


class RecordingMeta(models.Model):
    id = models.ForeignKey(Recording, db_column='id', primary_key=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recording_meta'


class RecordingRatingRaw(models.Model):
    recording = models.ForeignKey(
        Recording, db_column='recording', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    rating = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'recording_rating_raw'
        unique_together = ('recording', 'editor')


class RecordingTag(models.Model):
    recording = models.ForeignKey(
        Recording, db_column='recording', primary_key=True)
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recording_tag'
        unique_together = ('recording', 'tag')


class RecordingTagRaw(models.Model):
    recording = models.ForeignKey(
        Recording, db_column='recording', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')

    class Meta:
        managed = False
        db_table = 'recording_tag_raw'
        unique_together = ('recording', 'editor')


class Release(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey(
        ArtistCredit, db_column='artist_credit')
    release_group = models.ForeignKey(
        'ReleaseGroup', db_column='release_group')
    status = models.ForeignKey(
        'ReleaseStatus', db_column='status', blank=True, null=True)
    packaging = models.ForeignKey(
        'ReleasePackaging', db_column='packaging', blank=True, null=True)
    language = models.ForeignKey(
        Language, db_column='language', blank=True, null=True)
    script = models.ForeignKey(
        'Script', db_column='script', blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    quality = models.SmallIntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    annotations = models.ManyToManyField(
        'Annotation', through='ReleaseAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaRelease')
    countries = models.ManyToManyField('CountryArea', through='ReleaseCountry')
    edits = models.ManyToManyField('Edit', through='EditRelease')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentRelease')
    labels = models.ManyToManyField(
        'Label', through='LLabelRelease')
    places = models.ManyToManyField(
        'Place', through='LPlaceRelease')
    recordings = models.ManyToManyField(
        'Recording', through='LRecordingRelease')
    releases = models.ManyToManyField('Release', through='LReleaseRelease')
    series = models.ManyToManyField('Series', through='LReleaseSeries')
    tags = models.ManyToManyField('Tag', through='ReleaseTag')
    urls = models.ManyToManyField('Url', through='LReleaseUrl')
    works = models.ManyToManyField('Work', through='LReleaseWork')

    class Meta:
        managed = False
        db_table = 'release'


class ReleaseAnnotation(models.Model):
    release = models.ForeignKey(Release, db_column='release', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'release_annotation'
        unique_together = ('release', 'annotation')


class ReleaseCountry(models.Model):
    release = models.ForeignKey(Release, db_column='release', primary_key=True)
    country = models.ForeignKey(CountryArea, db_column='country')
    date_year = models.SmallIntegerField(blank=True, null=True)
    date_month = models.SmallIntegerField(blank=True, null=True)
    date_day = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_country'
        unique_together = ('release', 'country')


class ReleaseCoverart(models.Model):
    id = models.ForeignKey(Release, db_column='id', primary_key=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    cover_art_url = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'release_coverart'


class ReleaseGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Release)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_gid_redirect'


class ReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey(ArtistCredit, db_column='artist_credit')
    type = models.ForeignKey(
        'ReleaseGroupPrimaryType', db_column='type', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    annotations = models.ManyToManyField(
        'Annotation', through='ReleaseGroupAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaReleaseGroup')
    edits = models.ManyToManyField(
        'Edit', through='EditReleaseGroup')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentReleaseGroup')
    labels = models.ManyToManyField(
        'Label', through='LLabelReleaseGroup')
    places = models.ManyToManyField(
        'Place', through='LPlaceReleaseGroup')
    recordings = models.ManyToManyField(
        'Recording', through='LRecordingReleaseGroup')
    releases = models.ManyToManyField(
        'Release', through='LReleaseReleaseGroup')
    release_groups = models.ManyToManyField(
        'ReleaseGroup', through='LReleaseGroupReleaseGroup')
    secondary_types = models.ManyToManyField(
        'ReleaseGroupSecondaryType', through='ReleaseGroupSecondaryTypeJoin')
    series = models.ManyToManyField(
        'Series', through='LReleaseGroupSeries')
    tags = models.ManyToManyField('Tag', through='ReleaseGroupTag')
    urls = models.ManyToManyField('Url', through='LReleaseGroupUrl')
    works = models.ManyToManyField('Work', through='LReleaseGroupWork')

    class Meta:
        managed = False
        db_table = 'release_group'


class ReleaseGroupAnnotation(models.Model):
    release_group = models.ForeignKey(
        ReleaseGroup, db_column='release_group', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'release_group_annotation'
        unique_together = ('release_group', 'annotation')


class ReleaseGroupGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(ReleaseGroup)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_group_gid_redirect'


class ReleaseGroupMeta(models.Model):
    id = models.ForeignKey(ReleaseGroup, db_column='id', primary_key=True)
    release_count = models.IntegerField()
    first_release_date_year = models.SmallIntegerField(blank=True, null=True)
    first_release_date_month = models.SmallIntegerField(blank=True, null=True)
    first_release_date_day = models.SmallIntegerField(blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_group_meta'


class ReleaseGroupPrimaryType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'release_group_primary_type'


class ReleaseGroupRatingRaw(models.Model):
    release_group = models.ForeignKey(
        ReleaseGroup, db_column='release_group', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    rating = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'release_group_rating_raw'
        unique_together = ('release_group', 'editor')


class ReleaseGroupSecondaryType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'release_group_secondary_type'


class ReleaseGroupSecondaryTypeJoin(models.Model):
    release_group = models.ForeignKey(
        ReleaseGroup, db_column='release_group', primary_key=True)
    secondary_type = models.ForeignKey(
        ReleaseGroupSecondaryType, db_column='secondary_type')
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'release_group_secondary_type_join'
        unique_together = ('release_group', 'secondary_type')


class ReleaseGroupTag(models.Model):
    release_group = models.ForeignKey(
        ReleaseGroup, db_column='release_group', primary_key=True)
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_group_tag'
        unique_together = ('release_group', 'tag')


class ReleaseGroupTagRaw(models.Model):
    release_group = models.ForeignKey(
        ReleaseGroup, db_column='release_group', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')

    class Meta:
        managed = False
        db_table = 'release_group_tag_raw'
        unique_together = ('release_group', 'editor', 'tag')


class ReleaseLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.ForeignKey(Release, db_column='release')
    label = models.ForeignKey(Label, db_column='label', blank=True, null=True)
    catalog_number = models.CharField(max_length=255, blank=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_label'


class ReleaseMeta(models.Model):
    id = models.ForeignKey(Release, db_column='id', primary_key=True)
    date_added = models.DateTimeField(blank=True, null=True)
    info_url = models.CharField(max_length=255, blank=True)
    amazon_asin = models.CharField(max_length=10, blank=True)
    amazon_store = models.CharField(max_length=20, blank=True)
    cover_art_presence = models.TextField()

    class Meta:
        managed = False
        db_table = 'release_meta'


class ReleasePackaging(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'release_packaging'


class ReleaseRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    added = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    lookup_count = models.IntegerField(blank=True, null=True)
    modify_count = models.IntegerField(blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'release_raw'


class ReleaseStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'release_status'


class ReleaseTag(models.Model):
    release = models.ForeignKey(Release, db_column='release', primary_key=True)
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_tag'
        unique_together = ('release', 'tag')


class ReleaseTagRaw(models.Model):
    release = models.ForeignKey(Release, db_column='release', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')

    class Meta:
        managed = False
        db_table = 'release_tag_raw'
        unique_together = ('release', 'editor', 'tag')


class ReleaseUnknownCountry(models.Model):
    release = models.ForeignKey(Release, db_column='release', primary_key=True)
    date_year = models.SmallIntegerField(blank=True, null=True)
    date_month = models.SmallIntegerField(blank=True, null=True)
    date_day = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_unknown_country'


class ReplicationControl(models.Model):
    id = models.IntegerField(primary_key=True)
    current_schema_sequence = models.IntegerField()
    current_replication_sequence = models.IntegerField(blank=True, null=True)
    last_replication_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replication_control'


class Script(models.Model):
    id = models.IntegerField(primary_key=True)
    iso_code = models.CharField(unique=True, max_length=4)
    iso_number = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    frequency = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'script'


class Series(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    comment = models.CharField(max_length=255)
    type = models.ForeignKey('SeriesType', db_column='type')
    ordering_attribute = models.ForeignKey(
        LinkTextAttributeType, db_column='ordering_attribute')
    ordering_type = models.ForeignKey(
        'SeriesOrderingType', db_column='ordering_type')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    annotations = models.ManyToManyField(
        'Annotation', through='SeriesAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaSeries')
    edits = models.ManyToManyField(
        'Edit', through='EditSeries')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentSeries')
    places = models.ManyToManyField(
        'Place', through='LPlaceSeries')
    series = models.ManyToManyField(
        'Series', through='LSeriesSeries')
    urls = models.ManyToManyField(
        'Url', through='LSeriesUrl')
    works = models.ManyToManyField(
        'Work', through='LSeriesWork')

    class Meta:
        managed = False
        db_table = 'series'


class SeriesAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    series = models.ForeignKey(Series, db_column='series')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey(
        'SeriesAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'series_alias'


class SeriesAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'series_alias_type'


class SeriesAnnotation(models.Model):
    series = models.ForeignKey(Series, db_column='series', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'series_annotation'
        unique_together = ('series', 'annotation')


class SeriesDeletion(models.Model):
    gid = models.TextField(primary_key=True)
    last_known_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    last_known_comment = models.TextField()
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'series_deletion'


class SeriesGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Series)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series_gid_redirect'


class SeriesOrderingType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'series_ordering_type'


class SeriesType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'series_type'


class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    ref_count = models.IntegerField()

    tags = models.ManyToManyField('Tag', through='TagRelation')

    class Meta:
        managed = False
        db_table = 'tag'


class TagRelation(models.Model):
    tag1 = models.ForeignKey(
        Tag, db_column='tag1',
        related_name='tag1_tagrelation_set', primary_key=True)
    tag2 = models.ForeignKey(
        Tag, db_column='tag2',
        related_name='tag2_tagrelation_set')
    weight = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag_relation'
        unique_together = ('tag1', 'tag2')


class Track(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    recording = models.ForeignKey(Recording, db_column='recording')
    medium = models.ForeignKey(Medium, db_column='medium')
    position = models.IntegerField()
    number = models.TextField()
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey(ArtistCredit, db_column='artist_credit')
    length = models.IntegerField(blank=True, null=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'track'


class TrackGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Track)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'track_gid_redirect'


class TrackRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.ForeignKey(ReleaseRaw, db_column='release')
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    sequence = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'track_raw'


class Url(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    url = models.TextField(unique=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    edits = models.ManyToManyField('Edit', through='EditUrl')
    urls = models.ManyToManyField('Url', through='LUrlUrl')

    class Meta:
        managed = False
        db_table = 'url'


class UrlGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Url)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'url_gid_redirect'


class Vote(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    edit = models.ForeignKey(Edit, db_column='edit')
    vote = models.SmallIntegerField()
    vote_time = models.DateTimeField(blank=True, null=True)
    superseded = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'vote'


class Work(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    type = models.ForeignKey(
        'WorkType', db_column='type', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    language = models.ForeignKey(
        Language, db_column='language', blank=True, null=True)

    annotations = models.ManyToManyField(
        'Annotation', through='WorkAnnotation')
    areas = models.ManyToManyField(
        'Area', through='LAreaWork')
    edits = models.ManyToManyField(
        'Edit', through='EditWork')
    instruments = models.ManyToManyField(
        'Instrument', through='LInstrumentWork')
    tags = models.ManyToManyField('Tag', through='WorkTag')
    works = models.ManyToManyField('Work', through='LWorkWork')
    urls = models.ManyToManyField('Url', through='LUrlWork')

    class Meta:
        managed = False
        db_table = 'work'


class WorkAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    work = models.ForeignKey(Work, db_column='work')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey(
        'WorkAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'work_alias'


class WorkAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'work_alias_type'


class WorkAnnotation(models.Model):
    work = models.ForeignKey(Work, db_column='work', primary_key=True)
    annotation = models.ForeignKey(Annotation, db_column='annotation')

    class Meta:
        managed = False
        db_table = 'work_annotation'
        unique_together = ('work', 'annotation')


class WorkAttribute(models.Model):
    id = models.IntegerField(primary_key=True)
    work = models.ForeignKey(Work, db_column='work')
    work_attribute_type = models.ForeignKey(
        'WorkAttributeType', db_column='work_attribute_type')
    work_attribute_type_allowed_value = models.ForeignKey(
        'WorkAttributeTypeAllowedValue',
        db_column='work_attribute_type_allowed_value',
        blank=True, null=True)
    work_attribute_text = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'work_attribute'


class WorkAttributeType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    free_text = models.BooleanField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'work_attribute_type'


class WorkAttributeTypeAllowedValue(models.Model):
    id = models.IntegerField(primary_key=True)
    work_attribute_type = models.ForeignKey(
        WorkAttributeType, db_column='work_attribute_type')
    value = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'work_attribute_type_allowed_value'


class WorkGidRedirect(models.Model):
    gid = models.TextField(primary_key=True)
    new = models.ForeignKey(Work)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_gid_redirect'


class WorkMeta(models.Model):
    id = models.ForeignKey(Work, db_column='id', primary_key=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_meta'


class WorkRatingRaw(models.Model):
    work = models.ForeignKey(Work, db_column='work', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    rating = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'work_rating_raw'
        unique_together = ('work', 'editor')


class WorkTag(models.Model):
    work = models.ForeignKey(Work, db_column='work', primary_key=True)
    tag = models.ForeignKey(Tag, db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_tag'
        unique_together = ('work', 'tag')


class WorkTagRaw(models.Model):
    work = models.ForeignKey(Work, db_column='work', primary_key=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    tag = models.ForeignKey(Tag, db_column='tag')

    class Meta:
        managed = False
        db_table = 'work_tag_raw'
        unique_together = ('work', 'editor', 'tag')


class WorkType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'work_type'
