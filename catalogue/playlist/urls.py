from django.urls import path
from .views import (
    ArtistListView,
    AlbumListView,
    TrackListView,
    PlaylistListCreateView,
    PlaylistRetrieveUpdateDestroyView,
    PlaylistListView,
    PlaylistDetailView,
    PlaylistCreateView,
    PlaylistUpdateView,
    PlaylistDeleteView,
)

urlpatterns = [
    path("artists/", ArtistListView.as_view(), name="artist-list"),
    path("albums/", AlbumListView.as_view(), name="album-list"),
    path("tracks/", TrackListView.as_view(), name="track-list"),
    path("playlists/", PlaylistListCreateView.as_view(), name="playlist-list-create"),
    path(
        "playlists/<uuid:pk>/",
        PlaylistRetrieveUpdateDestroyView.as_view(),
        name="playlist-detail",
    ),

    # Urls for template base API
    path('artists/', ArtistListView.as_view(), name='artist-list'),
    path('albums/', AlbumListView.as_view(), name='album-list'),
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('playlists/', PlaylistListView.as_view(), name='playlist-list'),
    path('playlists/<uuid:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/create/', PlaylistCreateView.as_view(), name='playlist-create'),
    path('playlists/<uuid:pk>/update/', PlaylistUpdateView.as_view(), name='playlist-update'),
    path('playlists/<uuid:pk>/delete/', PlaylistDeleteView.as_view(), name='playlist-delete'),
]
