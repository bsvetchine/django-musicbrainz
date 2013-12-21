# ForeignKey relations are manually set according to
# http://musicbrainz.org/doc/MusicBrainz_Database/Schema
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
    owner = models.IntegerField()
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
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    type = models.ForeignKey('AreaType', db_column='type', blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'area'

class AreaAlias(models.Model):
    id = models.IntegerField(primary_key=True) 
    area = models.ForeignKey('Area', db_column='area')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('AreaAliasType', db_column='type', blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'area_alias_type'

class AreaAnnotation(models.Model):
    area = models.ForeignKey('Area', db_column='area')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'area_annotation'

class AreaGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'area_gid_redirect'

class AreaType(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'area_type'

class Artist(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    name = models.CharField(unique=True, max_length=CHARACTER_VARYING_MAX_LENGTH)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    type = models.ForeignKey('ArtistType', db_column='type', blank=True, null=True)
    area = models.ForeignKey('Area', db_column='area', blank=True, null=True)
    gender = models.ForeignKey('Gender', db_column='gender', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    ended = models.BooleanField()
    begin_area = models.ForeignKey('Area', db_column='begin_area', related_name='artist_begin_area_set', blank=True, null=True)
    end_area = models.ForeignKey('Area', db_column='end_area', related_name='artist_end_area_set', blank=True, null=True)
    credits = models.ManyToManyField('ArtistCredit', through='ArtistCreditName')
    class Meta:
        managed = False
        db_table = 'artist'

class ArtistAlias(models.Model):
    id = models.IntegerField(primary_key=True) 
    artist = models.ForeignKey('Artist', db_column='artist')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('ArtistAliasType', db_column='type', blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'artist_alias_type'

class ArtistAnnotation(models.Model):
    artist = models.ForeignKey('Artist', db_column='artist')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'artist_annotation'

class ArtistCredit(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_count = models.SmallIntegerField()
    ref_count = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'artist_credit'

class ArtistCreditName(models.Model):
    artist_credit = models.ForeignKey('ArtistCredit', db_column='artist_credit')
    position = models.SmallIntegerField()
    artist = models.ForeignKey('Artist', db_column='artist')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    join_phrase = models.TextField()
    class Meta:
        managed = False
        db_table = 'artist_credit_name'

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
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'artist_gid_redirect'

class ArtistIpi(models.Model):
    artist = models.ForeignKey('Artist', db_column='artist')
    ipi = models.CharField(max_length=11)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'artist_ipi'

class ArtistIsni(models.Model):
    artist = models.ForeignKey('Artist', db_column='artist')
    isni = models.CharField(max_length=16)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'artist_isni'

class ArtistMeta(models.Model):
    id = models.IntegerField(primary_key=True) 
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'artist_meta'

class ArtistRatingRaw(models.Model):
    artist = models.ForeignKey('Artist', db_column='artist')
    editor = models.ForeignKey('Editor', db_column='editor')
    rating = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'artist_rating_raw'

class ArtistTag(models.Model):
    artist = models.ForeignKey('Artist', db_column='artist')
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'artist_tag'

class ArtistTagRaw(models.Model):
    artist = models.ForeignKey('Artist', db_column='artist')
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')
    class Meta:
        managed = False
        db_table = 'artist_tag_raw'

class ArtistType(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'artist_type'

class AutoeditorElection(models.Model):
    id = models.IntegerField(primary_key=True) 
    candidate = models.IntegerField()
    proposer = models.IntegerField()
    seconder_1 = models.IntegerField(blank=True, null=True)
    seconder_2 = models.IntegerField(blank=True, null=True)
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
    autoeditor_election = models.ForeignKey('AutoeditorElection', db_column='autoeditor_election')
    voter = models.IntegerField()
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
    release = models.ForeignKey('Release', db_column='release')
    discid = models.CharField(max_length=28)
    track_count = models.IntegerField()
    leadout_offset = models.IntegerField()
    track_offset = models.TextField() 
    class Meta:
        managed = False
        db_table = 'cdtoc_raw'

class CountryArea(models.Model):
    area = models.ForeignKey('Area', db_column='area')
    class Meta:
        managed = False
        db_table = 'country_area'

class DbmirrorPending(models.Model):
    seqid = models.IntegerField(primary_key=True)
    tablename = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    op = models.CharField(max_length=1, blank=True)
    xid = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'dbmirror_pending'

class DbmirrorPendingdata(models.Model):
    seqid = models.ForeignKey(DbmirrorPending, db_column='seqid')
    iskey = models.BooleanField()
    data = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH, blank=True)
    class Meta:
        managed = False
        db_table = 'dbmirror_pendingdata'

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
    language = models.ForeignKey('Language', db_column='language', blank=True, null=True)
    quality = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'edit'

class EditArea(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    area = models.ForeignKey('Area', db_column='area')
    class Meta:
        managed = False
        db_table = 'edit_area'

class EditArtist(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    artist = models.ForeignKey('Artist', db_column='artist')
    status = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'edit_artist'

class EditLabel(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    label = models.ForeignKey('Label', db_column='label')
    status = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'edit_label'

class EditNote(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    edit = models.ForeignKey('Edit', db_column='edit')
    text = models.TextField()
    post_time = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'edit_note'

class EditPlace(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    place = models.ForeignKey('Place', db_column='place')
    class Meta:
        managed = False
        db_table = 'edit_place'

class EditRecording(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    recording = models.ForeignKey('Recording', db_column='recording')
    class Meta:
        managed = False
        db_table = 'edit_recording'

class EditRelease(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    release = models.ForeignKey('Release', db_column='release')
    class Meta:
        managed = False
        db_table = 'edit_release'

class EditReleaseGroup(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    release_group = models.ForeignKey('ReleaseGroup', db_column='release_group')
    class Meta:
        managed = False
        db_table = 'edit_release_group'

class EditUrl(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    url = models.ForeignKey('Url', db_column='url')
    class Meta:
        managed = False
        db_table = 'edit_url'

class EditWork(models.Model):
    edit = models.ForeignKey('Edit', db_column='edit')
    work = models.ForeignKey('Work', db_column='work')
    class Meta:
        managed = False
        db_table = 'edit_work'

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
    gender = models.ForeignKey('Gender', db_column='gender', blank=True, null=True)
    area = models.ForeignKey('Area', db_column='area', blank=True, null=True)
    password = models.CharField(max_length=128)
    ha1 = models.CharField(max_length=32)
    deleted = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'editor'

class EditorCollection(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    public = models.BooleanField()
    description = models.TextField()
    class Meta:
        managed = False
        db_table = 'editor_collection'

class EditorCollectionRelease(models.Model):
    collection = models.ForeignKey('EditorCollection', db_column='collection')
    release = models.ForeignKey('Release', db_column='release')
    class Meta:
        managed = False
        db_table = 'editor_collection_release'

class EditorLanguage(models.Model):
    editor = models.ForeignKey('Editor', db_column='editor')
    language = models.ForeignKey('Language', db_column='language')
    fluency = models.TextField() 
    class Meta:
        managed = False
        db_table = 'editor_language'

class EditorOauthToken(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    application = models.ForeignKey('Application', db_column='application')
    authorization_code = models.TextField(blank=True)
    refresh_token = models.TextField(unique=True, blank=True)
    access_token = models.TextField(unique=True, blank=True)
    mac_key = models.TextField(blank=True)
    mac_time_diff = models.IntegerField(blank=True, null=True)
    expire_time = models.DateTimeField()
    scope = models.IntegerField()
    granted = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'editor_oauth_token'

class EditorPreference(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'editor_preference'

class EditorSubscribeArtist(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    artist = models.ForeignKey('Artist', db_column='artist')
    last_edit_sent = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'editor_subscribe_artist'

class EditorSubscribeArtistDeleted(models.Model):
    editor = models.ForeignKey('Editor', db_column='editor')
    gid = models.TextField() 
    deleted_by = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'editor_subscribe_artist_deleted'

class EditorSubscribeCollection(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    collection = models.ForeignKey('EditorCollection', db_column='collection')
    last_edit_sent = models.IntegerField()
    available = models.BooleanField()
    last_seen_name = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'editor_subscribe_collection'

class EditorSubscribeEditor(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    subscribed_editor = models.ForeignKey('Editor', db_column='subscribed_editor', related_name='subscribed_editor_set')
    last_edit_sent = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'editor_subscribe_editor'

class EditorSubscribeLabel(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    label = models.ForeignKey('Label', db_column='label')
    last_edit_sent = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'editor_subscribe_label'

class EditorSubscribeLabelDeleted(models.Model):
    editor = models.ForeignKey('Editor', db_column='editor')
    gid = models.TextField() 
    deleted_by = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'editor_subscribe_label_deleted'

class EditorWatchArtist(models.Model):
    artist = models.ForeignKey('Artist', db_column='artist')
    editor = models.ForeignKey('Editor', db_column='editor')
    class Meta:
        managed = False
        db_table = 'editor_watch_artist'

class EditorWatchPreferences(models.Model):
    editor = models.ForeignKey('Editor', db_column='editor')
    notify_via_email = models.BooleanField()
    notification_timeframe = models.TextField() 
    last_checked = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'editor_watch_preferences'

class EditorWatchReleaseGroupType(models.Model):
    editor = models.ForeignKey('Editor', db_column='editor')
    release_group_type = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'editor_watch_release_group_type'

class EditorWatchReleaseStatus(models.Model):
    editor = models.ForeignKey('Editor', db_column='editor')
    release_status = models.ForeignKey('ReleaseStatus', db_column='release_status')
    class Meta:
        managed = False
        db_table = 'editor_watch_release_status'

class Gender(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'gender'

class Iso31661(models.Model):
    area = models.ForeignKey('Area', db_column='area')
    code = models.CharField(primary_key=True, max_length=2)
    class Meta:
        managed = False
        db_table = 'iso_3166_1'

class Iso31662(models.Model):
    area = models.ForeignKey('Area', db_column='area')
    code = models.CharField(primary_key=True, max_length=10)
    class Meta:
        managed = False
        db_table = 'iso_3166_2'

class Iso31663(models.Model):
    area = models.ForeignKey('Area', db_column='area')
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
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_area_entity0_set')
    entity1 = models.ForeignKey('Area', db_column='entity1', related_name='area_area_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_area'

class LAreaArtist(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_artist_entity0_set')
    entity1 = models.ForeignKey('Artist', db_column='entity1', related_name='area_artist_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_artist'

class LAreaLabel(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_label_entity0_set')
    entity1 = models.ForeignKey('Label', db_column='entity1', related_name='area_label_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_label'

class LAreaPlace(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_place_entity0_set')
    entity1 = models.ForeignKey('Place', db_column='entity1', related_name='area_place_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_place'

class LAreaRecording(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_recording_entity0_set')
    entity1 = models.ForeignKey('Recording', db_column='entity1', related_name='area_recording_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_recording'

class LAreaRelease(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_release_entity0_set')
    entity1 = models.ForeignKey('Release', db_column='entity1', related_name='area_release_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_release'

class LAreaReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_release_group_entity0_set')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1', related_name='area_release_group_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_release_group'

class LAreaUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='area_url_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_url'

class LAreaWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Area', db_column='entity0', related_name='area_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='area_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_area_work'

class LArtistArtist(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_artist_entity0_set')
    entity1 = models.ForeignKey('Artist', db_column='entity1', related_name='artist_artist_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_artist'

class LArtistLabel(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_label_entity0_set')
    entity1 = models.ForeignKey('Label', db_column='entity1', related_name='artist_label_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_label'

class LArtistPlace(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_place_entity0_set')
    entity1 = models.ForeignKey('Place', db_column='entity1', related_name='artist_place_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_place'

class LArtistRecording(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_recording_entity0_set')
    entity1 = models.ForeignKey('Recording', db_column='entity1', related_name='artist_recording_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_recording'

class LArtistRelease(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_release_entity0_set')
    entity1 = models.ForeignKey('Release', db_column='entity1', related_name='artist_release_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_release'

class LArtistReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_release_group_entity0_set')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1', related_name='artist_release_group_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_release_group'

class LArtistUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='artist_url_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_url'

class LArtistWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Artist', db_column='entity0', related_name='artist_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='artist_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_artist_work'

class LLabelLabel(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0', related_name='label_label_entity0_set')
    entity1 = models.ForeignKey('Label', db_column='entity1', related_name='label_label_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_label_label'

class LLabelPlace(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0', related_name='label_place_entity0_set')
    entity1 = models.ForeignKey('Place', db_column='entity1', related_name='label_place_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_label_place'

class LLabelRecording(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0', related_name='label_recording_entity0_set')
    entity1 = models.ForeignKey('Recording', db_column='entity1', related_name='label_recording_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_label_recording'

class LLabelRelease(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0', related_name='label_release_entity0_set')
    entity1 = models.ForeignKey('Release', db_column='entity1', related_name='label_release_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_label_release'

class LLabelReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0', related_name='label_release_group_entity0_set')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1', related_name='label_release_group_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_label_release_group'

class LLabelUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0', related_name='label_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='label_url_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_label_url'

class LLabelWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Label', db_column='entity0', related_name='label_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='label_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_label_work'

class LPlacePlace(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0', related_name='place_place_entity0_set')
    entity1 = models.ForeignKey('Place', db_column='entity1', related_name='place_place_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_place_place'

class LPlaceRecording(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0', related_name='place_recording_entity0_set')
    entity1 = models.ForeignKey('Recording', db_column='entity1', related_name='place_recording_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_place_recording'

class LPlaceRelease(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0', related_name='place_release_entity0_set')
    entity1 = models.ForeignKey('Release', db_column='entity1', related_name='place_release_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_place_release'

class LPlaceReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0', related_name='place_release_group_entity0_set')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1', related_name='place_release_group_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_place_release_group'

class LPlaceUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0', related_name='place_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='place_url_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_place_url'

class LPlaceWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Place', db_column='entity0', related_name='place_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='place_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_place_work'

class LRecordingRecording(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0', related_name='recording_recording_entity0_set')
    entity1 = models.ForeignKey('Recording', db_column='entity1', related_name='recording_recording_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_recording_recording'

class LRecordingRelease(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0', related_name='recording_release_entity0_set')
    entity1 = models.ForeignKey('Release', db_column='entity1', related_name='recording_release_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_recording_release'

class LRecordingReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0', related_name='recording_release_group_entity0_set')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1', related_name='recording_release_group_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_recording_release_group'

class LRecordingUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0', related_name='recording_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='recording_url_entity0_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_recording_url'

class LRecordingWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Recording', db_column='entity0', related_name='recording_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='recording_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_recording_work'

class LReleaseGroupReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('ReleaseGroup', db_column='entity0', related_name='release_group_release_group_entity0_set')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1', related_name='release_group_release_group_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_release_group_release_group'

class LReleaseGroupUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('ReleaseGroup', db_column='entity0', related_name='release_group_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='release_group_url_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_release_group_url'

class LReleaseGroupWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('ReleaseGroup', db_column='entity0', related_name='release_group_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='release_group_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_release_group_work'

class LReleaseRelease(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0', related_name='release_release_entity0_set')
    entity1 = models.ForeignKey('Release', db_column='entity1', related_name='release_release_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_release_release'

class LReleaseReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0', related_name='release_release_group_entity0_set')
    entity1 = models.ForeignKey('ReleaseGroup', db_column='entity1', related_name='release_release_group_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_release_release_group'

class LReleaseUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0', related_name='release_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='release_url_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_release_url'

class LReleaseWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Release', db_column='entity0', related_name='release_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='release_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_release_work'

class LUrlUrl(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Url', db_column='entity0', related_name='url_url_entity0_set')
    entity1 = models.ForeignKey('Url', db_column='entity1', related_name='url_url_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_url_url'

class LUrlWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Url', db_column='entity0', related_name='url_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='url_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_url_work'

class LWorkWork(models.Model):
    id = models.IntegerField(primary_key=True) 
    link = models.ForeignKey('Link', db_column='link')
    entity0 = models.ForeignKey('Work', db_column='entity0', related_name='work_work_entity0_set')
    entity1 = models.ForeignKey('Work', db_column='entity1', related_name='work_work_entity1_set')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'l_work_work'

class Label(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    name = models.CharField(unique=True, max_length=CHARACTER_VARYING_MAX_LENGTH)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    label_code = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey('LabelType', db_column='type', blank=True, null=True)
    area = models.ForeignKey('Area', db_column='area', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    ended = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'label'

class LabelAlias(models.Model):
    id = models.IntegerField(primary_key=True) 
    label = models.ForeignKey('Label', db_column='label')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('LabelAliasType', db_column='type', blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'label_alias_type'

class LabelAnnotation(models.Model):
    label = models.ForeignKey('Label', db_column='label')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'label_annotation'

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
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'label_gid_redirect'

class LabelIpi(models.Model):
    label = models.ForeignKey('Label', db_column='label')
    ipi = models.CharField(max_length=11)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'label_ipi'

class LabelIsni(models.Model):
    label = models.ForeignKey('Label', db_column='label')
    isni = models.CharField(max_length=16)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'label_isni'

class LabelMeta(models.Model):
    id = models.IntegerField(primary_key=True) 
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'label_meta'

class LabelRatingRaw(models.Model):
    label = models.ForeignKey('Label', db_column='label')
    editor = models.ForeignKey('Editor', db_column='editor')
    rating = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'label_rating_raw'

class LabelTag(models.Model):
    label = models.ForeignKey('Label', db_column='label')
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'label_tag'

class LabelTagRaw(models.Model):
    label = models.ForeignKey('Label', db_column='label')
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')
    class Meta:
        managed = False
        db_table = 'label_tag_raw'

class LabelType(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=255)
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
    class Meta:
        managed = False
        db_table = 'link'

class LinkAttribute(models.Model):
    link = models.ForeignKey('Link', db_column='link')
    attribute_type = models.ForeignKey('LinkAttributeType', db_column='attribute_type')
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'link_attribute'

class LinkAttributeCredit(models.Model):
    link = models.ForeignKey('Link', db_column='link')
    attribute_type = models.ForeignKey('LinkAttributeType', db_column='attribute_type')
    credited_as = models.TextField()
    class Meta:
        managed = False
        db_table = 'link_attribute_credit'

class LinkAttributeType(models.Model):
    id = models.IntegerField(primary_key=True) 
    parent = models.IntegerField(blank=True, null=True)
    root = models.IntegerField()
    child_order = models.IntegerField()
    gid = models.TextField(unique=True) 
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'link_attribute_type'

class LinkCreditableAttributeType(models.Model):
    attribute_type = models.ForeignKey('LinkAttributeType', db_column='attribute_type')
    class Meta:
        managed = False
        db_table = 'link_creditable_attribute_type'

class LinkType(models.Model):
    id = models.IntegerField(primary_key=True) 
    parent = models.IntegerField(blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'link_type'

class LinkTypeAttributeType(models.Model):
    link_type = models.ForeignKey('LinkType', db_column='link_type')
    attribute_type = models.ForeignKey('LinkAttributeType', db_column='attribute_type')
    min = models.SmallIntegerField(blank=True, null=True)
    max = models.SmallIntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'link_type_attribute_type'

class Medium(models.Model):
    id = models.IntegerField(primary_key=True) 
    release = models.ForeignKey('Release', db_column='release')
    position = models.IntegerField()
    format = models.ForeignKey('MediumFormat', db_column='format', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    track_count = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'medium'

class MediumCdtoc(models.Model):
    id = models.IntegerField(primary_key=True) 
    medium = models.ForeignKey('Medium', db_column='medium')
    cdtoc = models.ForeignKey('Cdtoc', db_column='cdtoc')
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'medium_cdtoc'

class MediumFormat(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=100)
    parent = models.IntegerField(blank=True, null=True)
    child_order = models.IntegerField()
    year = models.SmallIntegerField(blank=True, null=True)
    has_discids = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'medium_format'

class MediumIndex(models.Model):
    medium = models.IntegerField(primary_key=True)
    toc = models.TextField(blank=True) 
    class Meta:
        managed = False
        db_table = 'medium_index'

class Place(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    type = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    area = models.IntegerField(blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'place'

class PlaceAlias(models.Model):
    id = models.IntegerField(primary_key=True) 
    place = models.ForeignKey('Place', db_column='place')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('PlaceAliasType', db_column='type', blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'place_alias_type'

class PlaceAnnotation(models.Model):
    place = models.ForeignKey('Place', db_column='place')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'place_annotation'

class PlaceGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'place_gid_redirect'

class PlaceTag(models.Model):
    place = models.ForeignKey('Place', db_column='place')
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'place_tag'

class PlaceTagRaw(models.Model):
    place = models.ForeignKey('Place', db_column='place')
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')
    class Meta:
        managed = False
        db_table = 'place_tag_raw'

class PlaceType(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'place_type'

class Recording(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey('ArtistCredit', db_column='artist_credit')
    length = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    video = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'recording'

class RecordingAnnotation(models.Model):
    recording = models.ForeignKey('Recording', db_column='recording')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'recording_annotation'

class RecordingGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'recording_gid_redirect'

class RecordingMeta(models.Model):
    id = models.IntegerField(primary_key=True) 
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'recording_meta'

class RecordingRatingRaw(models.Model):
    recording = models.ForeignKey('Recording', db_column='recording')
    editor = models.ForeignKey('Editor', db_column='editor')
    rating = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'recording_rating_raw'

class RecordingTag(models.Model):
    recording = models.ForeignKey('Recording', db_column='recording')
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'recording_tag'

class RecordingTagRaw(models.Model):
    recording = models.ForeignKey('Recording', db_column='recording')
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')
    class Meta:
        managed = False
        db_table = 'recording_tag_raw'

class Release(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey('ArtistCredit', db_column='artist_credit')
    release_group = models.ForeignKey('ReleaseGroup', db_column='release_group')
    status = models.ForeignKey('ReleaseStatus', db_column='status', blank=True, null=True)
    packaging = models.ForeignKey('ReleasePackaging', db_column='packaging', blank=True, null=True)
    language = models.ForeignKey('Language', db_column='language', blank=True, null=True)
    script = models.ForeignKey('Script', db_column='script', blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    quality = models.SmallIntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release'

class ReleaseAnnotation(models.Model):
    release = models.ForeignKey('Release', db_column='release')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'release_annotation'

class ReleaseCountry(models.Model):
    release = models.ForeignKey('Release', db_column='release')
    country = models.ForeignKey('CountryArea', db_column='country')
    date_year = models.SmallIntegerField(blank=True, null=True)
    date_month = models.SmallIntegerField(blank=True, null=True)
    date_day = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release_country'

class ReleaseCoverart(models.Model):
    id = models.IntegerField(primary_key=True) 
    last_updated = models.DateTimeField(blank=True, null=True)
    cover_art_url = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'release_coverart'

class ReleaseEvent(models.Model):
    release = models.ForeignKey('Release', db_column='release', blank=True, null=True)
    date_year = models.SmallIntegerField(blank=True, null=True)
    date_month = models.SmallIntegerField(blank=True, null=True)
    date_day = models.SmallIntegerField(blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release_event'

class ReleaseGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release_gid_redirect'

class ReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey('ArtistCredit', db_column='artist_credit')
    type = models.ForeignKey('ReleaseGroupPrimaryType', db_column='type', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    secondary_types = models.ManyToManyField('ReleaseGroupSecondaryType', through='ReleaseGroupSecondaryTypeJoin')
    class Meta:
        managed = False
        db_table = 'release_group'

class ReleaseGroupAnnotation(models.Model):
    release_group = models.ForeignKey('ReleaseGroup', db_column='release_group')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'release_group_annotation'

class ReleaseGroupGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release_group_gid_redirect'

class ReleaseGroupMeta(models.Model):
    id = models.IntegerField(primary_key=True) 
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
    class Meta:
        managed = False
        db_table = 'release_group_primary_type'

class ReleaseGroupRatingRaw(models.Model):
    release_group = models.ForeignKey('ReleaseGroup', db_column='release_group')
    editor = models.ForeignKey('Editor', db_column='editor')
    rating = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'release_group_rating_raw'

class ReleaseGroupSecondaryType(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.TextField()
    class Meta:
        managed = False
        db_table = 'release_group_secondary_type'

class ReleaseGroupSecondaryTypeJoin(models.Model):
    release_group = models.ForeignKey('ReleaseGroup', db_column='release_group')
    secondary_type = models.ForeignKey('ReleaseGroupSecondaryType', db_column='secondary_type')
    created = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'release_group_secondary_type_join'

class ReleaseGroupTag(models.Model):
    release_group = models.ForeignKey('ReleaseGroup', db_column='release_group')
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release_group_tag'

class ReleaseGroupTagRaw(models.Model):
    release_group = models.ForeignKey('ReleaseGroup', db_column='release_group')
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')
    class Meta:
        managed = False
        db_table = 'release_group_tag_raw'

class ReleaseLabel(models.Model):
    id = models.IntegerField(primary_key=True) 
    release = models.ForeignKey('Release', db_column='release')
    label = models.IntegerField(blank=True, null=True)
    catalog_number = models.CharField(max_length=255, blank=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release_label'

class ReleaseMeta(models.Model):
    id = models.IntegerField(primary_key=True) 
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
    class Meta:
        managed = False
        db_table = 'release_status'

class ReleaseTag(models.Model):
    release = models.ForeignKey('Release', db_column='release')
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'release_tag'

class ReleaseTagRaw(models.Model):
    release = models.ForeignKey('Release', db_column='release')
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('Tag', db_column='tag')
    class Meta:
        managed = False
        db_table = 'release_tag_raw'

class ReleaseUnknownCountry(models.Model):
    release = models.IntegerField(primary_key=True)
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

class ScriptLanguage(models.Model):
    id = models.IntegerField(primary_key=True) 
    script = models.IntegerField()
    language = models.ForeignKey('Language', db_column='language')
    frequency = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'script_language'

class Tag(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(unique=True, max_length=255)
    ref_count = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tag'

class TagRelation(models.Model):
    tag1 = models.IntegerField()
    tag2 = models.IntegerField()
    weight = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tag_relation'

class Track(models.Model):
    id = models.IntegerField(primary_key=True) 
    gid = models.TextField(unique=True) 
    recording = models.ForeignKey('Recording', db_column='recording')
    medium = models.ForeignKey('Medium', db_column='medium')
    position = models.IntegerField()
    number = models.TextField()
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    artist_credit = models.ForeignKey('ArtistCredit', db_column='artist_credit')
    length = models.IntegerField(blank=True, null=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'track'

class TrackGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'track_gid_redirect'

class TrackRaw(models.Model):
    id = models.IntegerField(primary_key=True) 
    release = models.ForeignKey('Release', db_column='release')
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
    class Meta:
        managed = False
        db_table = 'url'

class UrlGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'url_gid_redirect'

class Vote(models.Model):
    id = models.IntegerField(primary_key=True) 
    editor = models.ForeignKey('Editor', db_column='editor')
    edit = models.ForeignKey('Edit', db_column='edit')
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
    type = models.ForeignKey('WorkType', db_column='type', blank=True, null=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    language = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'work'

class WorkAlias(models.Model):
    id = models.IntegerField(primary_key=True) 
    work = models.ForeignKey('Work', db_column='work')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('WorkAliasType', db_column='type', blank=True, null=True)
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
    class Meta:
        managed = False
        db_table = 'work_alias_type'

class WorkAnnotation(models.Model):
    work = models.ForeignKey('Work', db_column='work')
    annotation = models.ForeignKey('Annotation', db_column='annotation')
    class Meta:
        managed = False
        db_table = 'work_annotation'

class WorkAttribute(models.Model):
    id = models.IntegerField(primary_key=True) 
    work = models.ForeignKey('Work', db_column='work')
    work_attribute_type = models.ForeignKey('WorkAttributeType', db_column='work_attribute_type')
    work_attribute_type_allowed_value = models.IntegerField('WorkAttributeTypeAllowedValue', db_column='work_attribute_type_allowed_value', blank=True, null=True)
    work_attribute_text = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'work_attribute'

class WorkAttributeType(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    free_text = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'work_attribute_type'

class WorkAttributeTypeAllowedValue(models.Model):
    id = models.IntegerField(primary_key=True) 
    work_attribute_type = models.ForeignKey('WorkAttributeType', db_column='work_attribute_type')
    value = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'work_attribute_type_allowed_value'

class WorkGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) 
    new_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'work_gid_redirect'

class WorkMeta(models.Model):
    id = models.IntegerField(primary_key=True) 
    rating = models.SmallIntegerField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'work_meta'

class WorkRatingRaw(models.Model):
    work = models.ForeignKey('Work', db_column='work')
    editor = models.ForeignKey('Editor', db_column='editor')
    rating = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'work_rating_raw'

class WorkTag(models.Model):
    work = models.ForeignKey('Work', db_column='work')
    tag = models.ForeignKey('Tag', db_column='tag')
    count = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'work_tag'

class WorkTagRaw(models.Model):
    work = models.ForeignKey('Work', db_column='work')
    editor = models.ForeignKey('Editor', db_column='editor')
    tag = models.ForeignKey('WorkTag', db_column='tag')
    class Meta:
        managed = False
        db_table = 'work_tag_raw'

class WorkType(models.Model):
    id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'work_type'

