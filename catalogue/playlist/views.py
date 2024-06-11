from rest_framework import generics, viewsets
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

from .models import Artist, Album, Track, Playlist, PlaylistTrack
from .serializers import (
    ArtistSerializer,
    AlbumSerializer,
    TrackSerializer,
    PlaylistSerializer,
)


# Views for REST API
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


# Template Views
def playlist_list(request):
    playlists = Playlist.objects.all()
    return render(request, "playlist_list.html", {"playlists": playlists})


def playlist_detail(request, uuid):
    playlist = get_object_or_404(Playlist, uuid=uuid)
    if request.method == "POST":
        if "delete" in request.POST:
            playlist.delete()
            return redirect("playlist_list")
    return render(request, "playlist_detail.html", {"playlist": playlist})


def playlist_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        playlist = Playlist.objects.create(name=name)
        return redirect("playlist_detail", uuid=playlist.uuid)
    return render(request, "playlist_form.html")


def playlist_update(request, uuid):
    playlist = get_object_or_404(Playlist, uuid=uuid)
    if request.method == "POST":
        playlist.name = request.POST["name"]
        playlist.save()
        return redirect("playlist_detail", uuid=playlist.uuid)
    return render(request, "playlist_form.html", {"playlist": playlist})


def playlist_add_track(request, uuid):
    playlist = get_object_or_404(Playlist, uuid=uuid)
    if request.method == "POST":
        track_id = request.POST["track"]
        order = request.POST["order"]
        track = get_object_or_404(Track, id=track_id)
        PlaylistTrack.objects.create(playlist=playlist, track=track, order=order)
        return redirect("playlist_detail", uuid=playlist.uuid)
    tracks = Track.objects.all()
    return render(
        request, "playlist_add_track.html", {"playlist": playlist, "tracks": tracks}
    )
