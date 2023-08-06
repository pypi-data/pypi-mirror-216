from django import forms

from .models import UploadedVideo, Video
from .widgets import VideoUploadWidget


class UploadedVideoForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo
        fields = [
            "file",
            "mime",
            "duration",
            "width",
            "height",
            "frames_per_second",
            "frame_count",
        ]

    mime = forms.HiddenInput()
    duration = forms.HiddenInput()
    width = forms.HiddenInput()
    height = forms.HiddenInput()
    frames_per_second = forms.HiddenInput()
    frame_count = forms.HiddenInput()


class BaseVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "upload", "tags"]


class VideoForm(BaseVideoForm):
    class Meta(BaseVideoForm.Meta):
        widgets = {"upload": VideoUploadWidget()}
