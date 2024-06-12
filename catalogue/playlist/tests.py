from django.test import TestCase
from django.urls import reverse
from playlist.models import Artist, Album, Track, Playlist, PlaylistTrack
from uuid import uuid4
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import (
    ArtistSerializer,
    AlbumSerializer,
    TrackSerializer,
    PlaylistSerializer,
)


class ArtistViewSetTests(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")
        self.valid_payload = {"name": "New Artist"}
        self.invalid_payload = {"name": ""}

    def test_get_all_artists(self):
        response = self.client.get(reverse("artist-list"))
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_valid_artist(self):
        response = self.client.post(reverse("artist-list"), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 2)

    def test_create_invalid_artist(self):
        response = self.client.post(reverse("artist-list"), data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_artist(self):
        response = self.client.put(
            reverse("artist-detail", args=[self.artist.id]), data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, self.valid_payload["name"])

    def test_delete_artist(self):
        response = self.client.delete(reverse("artist-detail", args=[self.artist.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Artist.objects.count(), 0)


class AlbumViewSetTests(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")
        self.album = Album.objects.create(title="Album 1", artist=self.artist)
        self.valid_payload = {"title": "New Album", "artist": self.artist.id}
        self.invalid_payload = {"title": "", "artist": ""}

    def test_get_all_albums(self):
        response = self.client.get(reverse("album-list"))
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_valid_album(self):
        response = self.client.post(reverse("album-list"), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)

    def test_create_invalid_album(self):
        response = self.client.post(reverse("album-list"), data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_album(self):
        response = self.client.put(
            reverse("album-detail", args=[self.album.id]), data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.album.refresh_from_db()
        self.assertEqual(self.album.title, self.valid_payload["title"])

    def test_delete_album(self):
        response = self.client.delete(reverse("album-detail", args=[self.album.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Album.objects.count(), 0)


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

    def test_create_valid_track(self):
        response = self.client.post(reverse("track-list"), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Track.objects.count(), 2)

    def test_create_invalid_track(self):
        response = self.client.post(reverse("track-list"), data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_track(self):
        response = self.client.put(
            reverse("track-detail", args=[self.track.id]), data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.track.refresh_from_db()
        self.assertEqual(self.track.title, self.valid_payload["title"])

    def test_delete_track(self):
        response = self.client.delete(reverse("track-detail", args=[self.track.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Track.objects.count(), 0)


class PlaylistViewSetTests(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Artist 1")
        self.album = Album.objects.create(title="Album 1", artist=self.artist)
        self.track1 = Track.objects.create(title="Track 1", album=self.album)
        self.track2 = Track.objects.create(title="Track 2", album=self.album)
        self.playlist = Playlist.objects.create(name="Test Playlist")
        self.playlist.tracks.add(self.track1, through_defaults={"order": 1})
        self.playlist.tracks.add(self.track2, through_defaults={"order": 2})
        self.valid_payload = {
            "name": "New Playlist",
            "tracks": [
                {"track": self.track1.id, "order": 1},
                {"track": self.track2.id, "order": 2},
            ],
        }
        self.invalid_payload = {"name": "", "tracks": []}

    def test_get_all_playlists(self):
        response = self.client.get(reverse("playlist-list"))
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # def test_create_valid_playlist(self):
    #     response = self.client.post(reverse("playlist-list"), data=self.valid_payload)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Playlist.objects.count(), 2)

    def test_create_valid_playlist(self):
        response = self.client.post(
            reverse("playlist-list"), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 2)

    def test_create_invalid_playlist(self):
        response = self.client.post(
            reverse("playlist-list"), data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_playlist(self):
        response = self.client.put(
            reverse("playlist-detail", args=[self.playlist.uuid]),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, self.valid_payload["name"])

    def test_delete_playlist(self):
        response = self.client.delete(
            reverse("playlist-detail", args=[self.playlist.uuid])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Playlist.objects.count(), 0)


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
            reverse("playlist_create"), {"name": "New Playlist"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Playlist.objects.count(), 2)
        self.assertEqual(Playlist.objects.last().name, "New Playlist")

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
