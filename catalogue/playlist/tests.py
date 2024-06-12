from django.test import TestCase
from django.urls import reverse
from playlist.models import Artist, Album, Track, Playlist
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import (
    ArtistSerializer,
    AlbumSerializer,
    TrackSerializer,
    PlaylistSerializer,
)


class ArtistViewSetTests(APITestCase):
    # setUp method is called before every test method to set up any necessary preconditions.
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")

    # every method should start with test and contain any number of assertaion to check condition
    def test_get_all_artists(self):
        response = self.client.get(reverse("artist-list"))
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        # self.assertEqual method is used to compare two values and check if they are equal.
        # self.assertEqual(actual_value, expected_value, msg=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_artist(self):
        response = self.client.get(reverse("artist-detail", args=[self.artist.id]))
        artist = Artist.objects.get(id=self.artist.id)
        serializer = ArtistSerializer(artist)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_artist_not_allowed(self):
        response = self.client.post(reverse("artist-list"), data={"name": "New Artist"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_artist_not_allowed(self):
        response = self.client.put(
            reverse("artist-detail", args=[self.artist.id]),
            data={"name": "Updated Artist"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_artist_not_allowed(self):
        response = self.client.delete(reverse("artist-detail", args=[self.artist.id]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AlbumViewSetTests(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")
        self.album = Album.objects.create(title="Album 1", artist=self.artist)
        self.valid_payload = {"title": "Album 2", "artist": self.artist.id}
        self.invalid_payload = {"title": "", "artist": self.artist.id}

    def test_get_all_albums(self):
        response = self.client.get(reverse("album-list"))
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_album(self):
        response = self.client.get(reverse("album-detail", args=[self.album.id]))
        album = Album.objects.get(id=self.album.id)
        serializer = AlbumSerializer(album)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_album_not_allowed(self):
        response = self.client.post(reverse("album-list"), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Album.objects.count(), 1)

    def test_update_album_not_allowed(self):
        response = self.client.put(
            reverse("album-detail", args=[self.album.id]), data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.album.refresh_from_db()
        self.assertNotEqual(self.album.title, self.valid_payload["title"])

    def test_partial_update_album_not_allowed(self):
        response = self.client.patch(
            reverse("album-detail", args=[self.album.id]),
            data={"title": "Updated Title"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.album.refresh_from_db()
        self.assertNotEqual(self.album.title, "Updated Title")

    def test_delete_album_not_allowed(self):
        response = self.client.delete(reverse("album-detail", args=[self.album.id]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Album.objects.count(), 1)


class TrackViewSetTests(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")
        self.album = Album.objects.create(title="Album 1", artist=self.artist)
        self.track = Track.objects.create(title="Track 1", album=self.album)
        self.valid_payload = {"title": "New Track", "album": self.album.id}
        self.invalid_payload = {"title": "", "album": ""}

    def test_get_all_tracks(self):
        response = self.client.get(reverse("track-list"))
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_track(self):
        response = self.client.get(reverse("track-detail", args=[self.track.id]))
        track = Track.objects.get(id=self.track.id)
        serializer = TrackSerializer(track)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_track_not_allowed(self):
        response = self.client.post(reverse("track-list"), data={"name": "New track"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_track_not_allowed(self):
        response = self.client.put(
            reverse("track-detail", args=[self.track.id]),
            data={"name": "Updated track"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_track_not_allowed(self):
        response = self.client.delete(reverse("track-detail", args=[self.track.id]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PlaylistViewSetTests(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")
        self.album = Album.objects.create(title="Album 1", artist=self.artist)
        self.track1 = Track.objects.create(title="Track 1", album=self.album)
        self.track2 = Track.objects.create(title="Track 2", album=self.album)
        self.playlist = Playlist.objects.create(name="Test Playlist")
        self.playlist.tracks.add(self.track1, through_defaults={"order": 1})
        self.playlist.tracks.add(self.track2, through_defaults={"order": 2})

    def test_get_all_playlists(self):
        response = self.client.get(reverse("playlist-list"))
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_playlist(self):
        response = self.client.get(
            reverse("playlist-detail", args=[self.playlist.uuid])
        )
        playlist = Playlist.objects.get(uuid=self.playlist.uuid)
        serializer = PlaylistSerializer(playlist)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_playlist_not_allowed(self):
        response = self.client.post(
            reverse("playlist-list"), data={"name": "New playlist"}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_playlist_not_allowed(self):
        response = self.client.put(
            reverse("playlist-detail", args=[self.playlist.uuid]),
            data={"name": "Updated playlist"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_playlist_not_allowed(self):
        response = self.client.delete(
            reverse("playlist-detail", args=[self.playlist.uuid])
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PlaylistWebTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")
        self.album = Album.objects.create(title="Album 1", artist=self.artist)
        self.track1 = Track.objects.create(title="Track 1", album=self.album)
        self.track2 = Track.objects.create(title="Track 2", album=self.album)
        self.playlist = Playlist.objects.create(name="Test Playlist")

    def test_playlist_list_view(self):
        response = self.client.get(reverse("playlist_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.playlist.name)

    def test_playlist_detail_view(self):
        response = self.client.get(
            reverse("playlist_detail", args=[self.playlist.uuid])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.playlist.name)

    def test_create_playlist_view(self):
        response = self.client.post(
            reverse("playlist_create"), {"name": "Test Playlist"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Playlist.objects.count(), 2)
        self.assertEqual(Playlist.objects.last().name, "Test Playlist")

    def test_update_playlist_view(self):
        response = self.client.post(
            reverse("playlist_update", args=[self.playlist.uuid]),
            {"name": "Updated Playlist"},
        )
        self.assertEqual(response.status_code, 302)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, "Updated Playlist")

    def test_delete_playlist_view(self):
        response = self.client.post(
            reverse("playlist_detail", args=[self.playlist.uuid]), {"delete": "delete"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Playlist.objects.count(), 0)

    def test_add_track_to_playlist_view(self):
        response = self.client.post(
            reverse("playlist_add_track", args=[self.playlist.uuid]),
            {"track": self.track1.id, "order": 1},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.playlist.tracks.count(), 1)
        self.assertEqual(self.playlist.tracks.first().title, "Track 1")
