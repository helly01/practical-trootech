from django.contrib import admin

from .models import Artist, Album, Track, Playlist, PlaylistTrack


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist")
    list_filter = ("artist",)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "album")
    list_filter = ("album",)


# admin.TabularInline specifies that the forms should be displayed in a tabular (table) format.
class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 1


# Specifies the number of empty forms to display by default. Setting extra = 1 means that one empty form will be shown
@admin.register(PlaylistTrack)
class PlaylistTrackAdmin(admin.ModelAdmin):
    list_display = ("playlist", "track", "order")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")
    inlines = [PlaylistTrackInline]
