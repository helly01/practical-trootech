from rest_framework import generics
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Artist, Album, Track, Playlist, PlaylistTrack
from .forms import PlaylistForm, PlaylistTrackForm
from .serializers import (
    ArtistSerializer,
    AlbumSerializer,
    TrackSerializer,
    PlaylistSerializer,
)


# Views for REST API
class ArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumListView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackListView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class PlaylistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


# Views for template base API
class PlaylistListView(ListView):
    model = Playlist
    template_name = "playlist/playlist_list.html"
    context_object_name = "playlists"


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = "playlist/playlist_detail.html"
    context_object_name = "playlist"


class PlaylistCreateView(CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = "playlist/playlist_form.html"
    success_url = reverse_lazy("playlist-list")


class PlaylistUpdateView(UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = "playlist/playlist_form.html"
    success_url = reverse_lazy("playlist-list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        PlaylistTrackFormSet = inlineformset_factory(
            Playlist, PlaylistTrack, form=PlaylistTrackForm, extra=1
        )
        if self.request.POST:
            data["tracks"] = PlaylistTrackFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data["tracks"] = PlaylistTrackFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tracks = context["tracks"]
        if form.is_valid() and tracks.is_valid():
            self.object = form.save()
            tracks.instance = self.object
            tracks.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PlaylistDeleteView(DeleteView):
    model = Playlist
    template_name = "playlist/playlist_confirm_delete.html"
    success_url = reverse_lazy("playlist-list")
