from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AlbumViewSet,
    ArtistViewSet,
    TrackViewSet,
    PlaylistViewSet,
    playlist_list,
    playlist_create,
    playlist_detail,
    playlist_update,
    playlist_add_track,
)

router = DefaultRouter()
router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)
router.register(r"tracks", TrackViewSet)
router.register(r"playlists", PlaylistViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(router.urls)),
    path("playlists/", playlist_list, name="playlist_list"),
    path("playlists/create/", playlist_create, name="playlist_create"),
    path("playlists/<uuid:uuid>/", playlist_detail, name="playlist_detail"),
    path("playlists/<uuid:uuid>/update/", playlist_update, name="playlist_update"),
    path(
        "playlists/<uuid:uuid>/add_track/",
        playlist_add_track,
        name="playlist_add_track",
    ),
]
