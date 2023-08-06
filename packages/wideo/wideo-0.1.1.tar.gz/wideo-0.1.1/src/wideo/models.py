from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from wagtail.models import CollectionMember
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from . import get_render_model
from .storage import upload_to


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, db_index=True
    )


class UserUpload(models.Model):
    class Meta:
        abstract = True

    uploaded_by_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("uploaded by user"),
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    uploaded_by_user.wagtail_reference_index_ignore = True


class RemoteVideoFile(models.Model):
    class Meta:
        abstract = True

    INFORMATION_FIELDS = (
        "mime",
        "duration",
        "width",
        "height",
        "frames_per_second",
        "frame_count",
    )

    file = models.FileField(
        upload_to=upload_to,
        verbose_name=_("file"),
        help_text=_("The uploaded video file"),
    )
    mime = models.CharField(
        max_length=100,
        verbose_name=_("mime type"),
        help_text=_("MIME type of the video"),
    )
    duration = models.FloatField(
        verbose_name=_("duration in seconds"),
        help_text=_("Duration of the video in seconds"),
    )
    width = models.IntegerField(
        verbose_name=_("original width"),
        help_text=_("Width of the video in pixels"),
    )
    height = models.IntegerField(
        verbose_name=_("original height"),
        help_text=_("Height of the video in pixels"),
    )
    frames_per_second = models.DecimalField(
        verbose_name=_("original FPS"),
        help_text=_("FPS of the video"),
        max_digits=5,
        decimal_places=2,
    )
    frame_count = models.IntegerField(
        verbose_name=_("original frame count"),
        help_text=_("Number of frames in the video"),
    )


class UploadedVideo(TimestampedModel, UserUpload, RemoteVideoFile):
    def __str__(self) -> str:
        return str(self.file)


class AbstractVideo(index.Indexed, CollectionMember, TimestampedModel, UserUpload):
    class Meta:
        abstract = True

    class ProcessStatus(models.TextChoices):
        pending = "pending"
        processing = "processing"
        success = "success"
        failed = "failed"

    title = models.CharField(max_length=255, verbose_name=_("title"))
    upload = models.ForeignKey(
        to=UploadedVideo,
        on_delete=models.PROTECT,
        verbose_name=_("file"),
        help_text=_("The uploaded video file"),
    )
    status = models.CharField(
        max_length=max(len(x) for x, _ in ProcessStatus.choices),
        choices=ProcessStatus.choices,
        default=ProcessStatus.pending,
        verbose_name=_("status"),
        help_text=_(
            "The status of the video processing (pending means nothing "
            "happens on this video yet, processing means the task is running, "
            "success means a render is available and failed means the task "
            "failed)"
        ),
    )
    tags = TaggableManager(help_text=None, blank=True, verbose_name=_("tags"))
    search_fields = CollectionMember.search_fields + [
        index.SearchField("title", boost=10),
        index.AutocompleteField("title"),
        index.FilterField("title"),
        index.RelatedFields(
            "tags",
            [
                index.SearchField("name", boost=10),
                index.AutocompleteField("name"),
            ],
        ),
        index.FilterField("uploaded_by_user"),
    ]
    admin_form_fields = (
        "title",
        "upload",
        "tags",
    )

    @property
    def rendered(self) -> list:
        return [
            {
                "url": render.file.url,
                **{
                    field: getattr(render, field)
                    for field in RemoteVideoFile.INFORMATION_FIELDS
                },
            }
            for render in get_render_model().objects.filter(video=self)
        ]

    def __str__(self):
        return self.title


@register_snippet
class Video(AbstractVideo):
    pass


class AbstractRender(TimestampedModel, RemoteVideoFile):
    """
    If a video as processed correctly, a render is created with pointers to
    all the outputs of the rendering process.
    """

    class Meta:
        abstract = True


class Render(AbstractRender):
    video = models.ForeignKey(
        to=Video,
        on_delete=models.CASCADE,
        verbose_name=_("video"),
        help_text=_("The video that was rendered"),
    )
