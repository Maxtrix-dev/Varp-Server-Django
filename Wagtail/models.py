from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

class HeadingBlock(blocks.StructBlock):
    level = blocks.ChoiceBlock(choices=[("h2", "H2"), ("h3", "H3")], default="h2")
    text = blocks.CharBlock()

    class Meta:
        template = "heading.html"
        icon = "title"
        label = "Heading"

class ParagraphBlock(blocks.RichTextBlock):
    def __init__(self, **kwargs):
        super().__init__(
            features=["bold", "italic", "link", "ol", "ul"],  # keep paragraph features lean
            **kwargs,
        )
    class Meta:
        template = "paragraph.html"
        icon = "doc-full"
        label = "Paragraph"

class ImageWithTextBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    text = blocks.RichTextBlock(features=["bold","italic","link","ol","ul"])
    position = blocks.ChoiceBlock(choices=[("left","Image left"), ("right","Image right")], default="left")
    caption = blocks.CharBlock(required=False)

    class Meta:
        template = "image_with_text_block.html"
        icon = "image"
        label = "Image + Text"

class ExternalEmbedBlock(EmbedBlock):
    class Meta:
        template = "embeded.html"
        icon = "media"
        label = "Embed (Instagram/YouTube/etc.)"


class ArticlePage(Page):
    content = StreamField(
        [
            ("heading", HeadingBlock()),
            ("paragraph", ParagraphBlock()),
            ("image_with_text", ImageWithTextBlock()),
            ("image", ImageWithTextBlock().child_blocks["image"]),  # simple image if you want
            ("embeded", ExternalEmbedBlock()),
        ],
        use_json_field=True,
        blank=True,
    )
    template="article_page.html"

    content_panels = Page.content_panels + [FieldPanel("content", heading="")]
