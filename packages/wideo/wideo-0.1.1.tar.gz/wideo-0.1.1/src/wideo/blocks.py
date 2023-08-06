from wagtail.blocks import BooleanBlock, StructBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class VideoBlock(StructBlock):
    video = SnippetChooserBlock(target_model="wideo.video")
    autoplay = BooleanBlock(required=False)
    controls = BooleanBlock(required=False)

    class Meta:
        label = "Video"
        template = "wideo/blocks/video.html"
