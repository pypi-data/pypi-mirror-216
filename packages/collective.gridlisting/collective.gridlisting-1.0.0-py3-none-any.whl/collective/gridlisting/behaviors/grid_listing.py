# -*- coding: utf-8 -*-

from collective.gridlisting import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


class IGridListingMarker(Interface):
    pass


LISTING_TITLE_TAGS = (
    # H1 not allowed
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
)


@provider(IFormFieldProvider)
class IGridListing(model.Schema):
    """ """

    row_css_class = schema.TextLine(
        title=_("Container row"),
        description=_("eg. if you want to set gutter between columns define here."),
        required=False,
    )

    column_css_class = schema.TextLine(
        title=_("Column"),
        description=_(
            "Use grid css class combinations for column. Example: 'col-12 col-md-6 col-xl-3'"
        ),
        required=False,
    )

    column_content_css_class = schema.TextLine(
        title=_("Column content"),
        description=_(
            "If you want borders or backgrounds inside the column define it here."
        ),
        required=False,
        default="row",
    )

    column_content_text_css_class = schema.TextLine(
        title=_("Column content text"),
        description=_("CSS class(es) for title/description/link in column content"),
        default="col",
        required=False,
    )

    column_content_image_css_class = schema.TextLine(
        title=_("Column content image"),
        description=_("CSS class(es) for preview image in column content"),
        default="col-3 text-end",
        required=False,
    )

    item_title_tag = schema.Choice(
        title=_("Listing item title tag"),
        values=LISTING_TITLE_TAGS,
        default="h3",
    )

    preview_scale = schema.Choice(
        title=_("Preview image scale"),
        vocabulary="plone.app.vocabularies.ImagesScales",
    )

    enable_masonry = schema.Bool(
        title=_("Enable masonry layout"),
        description=_("See masonry documentation."),
        required=False,
        default=False,
    )

    masonry_options = schema.TextLine(
        title=_("Additional masonry options"),
        description=_(
            'Options for "pat-masonry" see https://patternslib.com/demos/masonry.'
        ),
        required=False,
    )

    directives.fieldset(
        "gridlisting",
        label=_("Grid listing"),
        description=_(
            "Define grid listing properties. For further information see https://getbootstrap.com/docs/5.3/layout/grid/"
        ),
        fields=[
            "row_css_class",
            "column_css_class",
            "column_content_css_class",
            "column_content_text_css_class",
            "column_content_image_css_class",
            "item_title_tag",
            "preview_scale",
            "enable_masonry",
            "masonry_options",
        ],
    )


@implementer(IGridListing)
@adapter(IGridListingMarker)
class GridListing(object):
    def __init__(self, context):
        self.context = context

    @property
    def row_css_class(self):
        if safe_hasattr(self.context, "row_css_class"):
            return self.context.row_css_class
        return None

    @row_css_class.setter
    def row_css_class(self, value):
        self.context.row_css_class = value

    @property
    def column_css_class(self):
        if safe_hasattr(self.context, "column_css_class"):
            return self.context.column_css_class
        return None

    @column_css_class.setter
    def column_css_class(self, value):
        self.context.column_css_class = value

    @property
    def column_content_css_class(self):
        if safe_hasattr(self.context, "column_content_css_class"):
            return self.context.column_content_css_class
        return None

    @column_content_css_class.setter
    def column_content_css_class(self, value):
        self.context.column_content_css_class = value

    @property
    def column_content_text_css_class(self):
        if safe_hasattr(self.context, "column_content_text_css_class"):
            return self.context.column_content_text_css_class
        return None

    @column_content_text_css_class.setter
    def column_content_text_css_class(self, value):
        self.context.column_content_text_css_class = value

    @property
    def column_content_image_css_class(self):
        if safe_hasattr(self.context, "column_content_image_css_class"):
            return self.context.column_content_image_css_class
        return None

    @column_content_image_css_class.setter
    def column_content_image_css_class(self, value):
        self.context.column_content_image_css_class = value

    @property
    def item_title_tag(self):
        if safe_hasattr(self.context, "item_title_tag"):
            return self.context.item_title_tag
        return None

    @item_title_tag.setter
    def item_title_tag(self, value):
        self.context.item_title_tag = value

    @property
    def preview_scale(self):
        if safe_hasattr(self.context, "preview_scale"):
            return self.context.preview_scale
        return None

    @preview_scale.setter
    def preview_scale(self, value):
        self.context.preview_scale = value

    @property
    def enable_masonry(self):
        if safe_hasattr(self.context, "enable_masonry"):
            return self.context.enable_masonry
        return None

    @enable_masonry.setter
    def enable_masonry(self, value):
        self.context.enable_masonry = value

    @property
    def masonry_options(self):
        if safe_hasattr(self.context, "masonry_options"):
            return self.context.masonry_options
        return None

    @masonry_options.setter
    def masonry_options(self, value):
        self.context.masonry_options = value
