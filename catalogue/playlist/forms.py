from django import forms
from .models import Playlist, PlaylistTrack, Track


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["name"]


class PlaylistTrackForm(forms.ModelForm):
    track = forms.ModelChoiceField(queryset=Track.objects.all())
    order = forms.IntegerField()

    class Meta:
        model = PlaylistTrack
        fields = ["track", "order"]
