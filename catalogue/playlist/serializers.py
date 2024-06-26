from rest_framework import serializers

from .models import Artist, Album, Track, Playlist, PlaylistTrack


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())

    class Meta:
        model = PlaylistTrack
        fields = ["track", "order"]


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackSerializer(source="playlisttrack_set", many=True)

    class Meta:
        model = Playlist
        fields = ["uuid", "name", "tracks"]

    # create method is called when a new instance of a model is being created.
    def create(self, validated_data):
        tracks_data = validated_data.pop("playlisttrack_set")
        playlist = Playlist.objects.create(**validated_data)
        for track_data in tracks_data:
            PlaylistTrack.objects.create(playlist=playlist, **track_data)
        return playlist

    # update method is called when an existing instance of a model is being updated.
    def update(self, instance, validated_data):
        tracks_data = validated_data.pop("playlisttrack_set")
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        PlaylistTrack.objects.filter(playlist=instance).delete()
        for track_data in tracks_data:
            PlaylistTrack.objects.create(playlist=instance, **track_data)

        return instance
