import uuid

from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Use related_name to specify a clear reverse relation.
class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=255)
    album = models.ForeignKey(Album, related_name="tracks", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Intermediary model, allows you to add extra fields to the relationship
class Playlist(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Track, through="PlaylistTrack")

    def __str__(self):
        return self.name


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        # The query results for PlaylistTrack will be ordered by the order field in ascending order by default.
        ordering = ["order"]
        # It ensures that there cannot be duplicate combinations of playlist, track, and order in the table.
        unique_together = ["playlist", "track", "order"]
