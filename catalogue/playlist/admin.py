from django.contrib import admin
from .models import Artist, Album, Track, Playlist, PlaylistTrack


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_date")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_date")
    list_filter = ("artist",)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "album", "duration")
    list_filter = ("album",)


class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 1


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")
    inlines = [PlaylistTrackInline]
