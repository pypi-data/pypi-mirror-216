from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

from . import get_render_model, get_video_model
from .models import AbstractVideo, RemoteVideoFile, UploadedVideo


@receiver(pre_delete, sender=UploadedVideo)
def on_uploaded_video_pre_delete(instance: UploadedVideo, *args, **kwargs):
    instance.file.delete(save=False)


@receiver(post_delete, sender=get_video_model())
def on_video_post_delete(instance: AbstractVideo, *args, **kwargs):
    instance.upload.delete()


@receiver(post_save, sender=get_video_model())
def on_video_post_save(instance: AbstractVideo, created: bool, *args, **kwargs):
    if not created:
        return

    get_render_model().objects.create(
        video=instance,
        **{
            field: getattr(instance.upload, field)
            for field in RemoteVideoFile.INFORMATION_FIELDS
        }
    )
