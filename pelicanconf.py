#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Manish Shetty"
SITENAME = "Manish Shetty"
SITETITLE = "manishs.org | Manish"
SITEURL = "https://manishs.org/blog"

PATH = "content"

TIMEZONE = "America/Los_Angeles"
DEFAULT_DATE_FORMAT = "%B %d, %Y"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Uncomment these to test the feeds
# FEED_DOMAIN = SITEURL
# FEED_ALL_ATOM = 'feeds/all.atom.xml'
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DEFAULT_PAGINATION = 2

PAGINATION_PATTERNS = (
    (1, "{url}", "{save_as}"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# My own defaults
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.sane_lists": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.smarty": {},
    },
    "output_format": "html5",
}

PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "eric_extensions",
    "neighbors",
    "sitemap",
    "yuicompressor",
    "render_math",
    "social_cards",
]

THEME = "theme"
LOGO = "images/logo.png"
MERMAID = True

DEFAULT_CATEGORY = "Dross"

DIRECT_TEMPLATES = ["index", "categories", "archives", "tags"]

SITEMAP = {"format": "xml", "exclude": ["tags/", "author/", "categories/"]}

YUICOMPRESSOR_EXECUTABLE = "yuicompressor"

ARTICLE_URL = "scrivings/{slug}/"
ARTICLE_SAVE_AS = "scrivings/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
DRAFT_URL = "drafts/{slug}/"
DRAFT_SAVE_AS = "drafts/{slug}/index.html"
CATEGORY_URL = "categories/{slug}/"
CATEGORY_SAVE_AS = "categories/{slug}/index.html"
AUTHOR_SAVE_AS = ""
TAG_URL = "tags/{slug}/"
TAG_SAVE_AS = "tags/{slug}/index.html"

ARCHIVES_SAVE_AS = "scrivings/index.html"
ARCHIVES_URL = "scrivings/"
AUTHORS_SAVE_AS = ""
CATEGORIES_SAVE_AS = "categories/index.html"
CATEGORIES_URL = "categories"
TAGS_SAVE_AS = "tags/index.html"
TAGS_URL = "tags/"

STATIC_PATHS = ["images", "static", "fonts"]

EXTRA_PATH_METADATA = {
    "static/robots.txt": {"path": "robots.txt"},
    "images/favicon.ico": {"path": "favicon.ico"},
}

# Theme extras
MENUITEMS = [
    ("Vault", "scrivings/"),
    ("Tags", "tags/"),
]

SOCIAL = (
    ("Twitter", "https://twitter.com/slimshetty_"),
    ("GitHub", "https://github.com/manishshettym"),
    ("LinkedIn", "https://www.linkedin.com/in/manishshettym/"),
)

TWITTER_HANDLE = "@slimshetty_"
SITEMETA = "Your description here"

### Social Cards ###
SOCIAL_CARDS_PATH = "images/social-cards/"
SOCIAL_CARDS_TEMPLATE = "content/images/card-template.png"
SOCIAL_CARDS_FONT_FILENAME = "/Users/manishs/Projects/personal/blog/content/fonts/et-bembo-bold-line-figures/et-bembo-bold-line-figures.ttf"
SOCIAL_CARDS_CANVAS_LEFT = 150
SOCIAL_CARDS_CANVAS_TOP = 100
SOCIAL_CARDS_CANVAS_WIDTH = 1300
SOCIAL_CARDS_CANVAS_HEIGHT = 630
