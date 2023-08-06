from django.urls import path

import wideo.views

app_name = "wideo"
urlpatterns = [
    path("", wideo.views.IndexView.as_view(), name="index"),
    path(
        "results/",
        wideo.views.ListingResultsView.as_view(),
        name="listing_results",
    ),
    path("add/", wideo.views.add, name="add"),
    path("<int:video_id>/", wideo.views.edit, name="edit"),
    path("<int:video_id>/delete/", wideo.views.delete, name="delete"),
    path("upload/", wideo.views.upload_file, name="upload"),
    path(
        "get_uploaded_video_render/<int:uploaded_video_id>/",
        wideo.views.get_uploaded_video_render,
        name="get-uploaded-video-render",
    ),
]
