from django.test import TestCase
from django.urls import reverse
from playlist.models import Artist, Album, Track, Playlist, PlaylistTrack
from uuid import uuid4


class PlaylistTests(TestCase):

    def setUp(self):
        # Create sample data
        self.artist = Artist.objects.create(name="Test Artist", birth_date="1980-01-01")
        self.album = Album.objects.create(
            title="Test Album", artist=self.artist, release_date="2020-01-01"
        )
        self.track1 = Track.objects.create(
            title="Track 1", album=self.album, duration="00:03:30"
        )
        self.track2 = Track.objects.create(
            title="Track 2", album=self.album, duration="00:04:00"
        )
        self.playlist = Playlist.objects.create(name="Test Playlist")

    def test_playlist_list_view(self):
        response = self.client.get(reverse("playlist-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.playlist.name)

    def test_playlist_detail_view(self):
        response = self.client.get(
            reverse("playlist-detail", args=[self.playlist.uuid])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.playlist.name)

    def test_playlist_create_view(self):
        response = self.client.post(
            reverse("playlist-create"),
            {
                "name": "New Playlist",
                "tracks-TOTAL_FORMS": "1",
                "tracks-INITIAL_FORMS": "0",
                "tracks-MIN_NUM_FORMS": "0",
                "tracks-MAX_NUM_FORMS": "1000",
                "tracks-0-track": self.track1.id,
                "tracks-0-order": 1,
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertTrue(Playlist.objects.filter(name="New Playlist").exists())

    def test_playlist_update_view(self):
        response = self.client.post(
            reverse("playlist-update", args=[self.playlist.uuid]),
            {
                "name": "Updated Playlist",
                "tracks-TOTAL_FORMS": "1",
                "tracks-INITIAL_FORMS": "0",
                "tracks-MIN_NUM_FORMS": "0",
                "tracks-MAX_NUM_FORMS": "1000",
                "tracks-0-track": self.track1.id,
                "tracks-0-order": 1,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, "Updated Playlist")
        self.assertTrue(
            PlaylistTrack.objects.filter(
                playlist=self.playlist, track=self.track1, order=1
            ).exists()
        )

    def test_playlist_delete_view(self):
        response = self.client.post(
            reverse("playlist-delete", args=[self.playlist.uuid])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful deletion
        self.assertFalse(Playlist.objects.filter(uuid=self.playlist.uuid).exists())
