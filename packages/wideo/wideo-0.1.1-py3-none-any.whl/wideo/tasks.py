from celery import shared_task

from . import get_video_model
from .models import UploadedVideo


@shared_task
def delete_orphan_uploaded_videos():
    used_ids = get_video_model().objects.values("upload_id")
    UploadedVideo.objects.exclude(id__in=used_ids).delete()
