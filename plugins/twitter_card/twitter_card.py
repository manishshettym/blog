#!/usr/bin/env python

"""Implements Twitter Cards for Pelican Generated Sites"""

from pelican.settings import _DEFAULT_CONFIG
from pelican import signals


def twitter_card(generator):
    """
    https://dev.twitter.com/cards
    TWITTER_CARD_USE = (True) # (False)
    TWITTER_CARD_SITE = '@website' # The site's Twitter handle like @my_blog
    TWITTER_CARD_SITE_ID = 123456 # The site's Twitter ID
    TWITTER_CARD_CREATOR = '@username' # Your twitter handle like @yourtwitname
    TWITTER_CARD_CREATOR_ID = 56789 # The site creator's id
    GRAVATAR_URL = ''
    """

    _DEFAULT_CONFIG.setdefault("TWITTER_CARD_SITE", "True")
    _DEFAULT_CONFIG.setdefault("TWITTER_CARD_SITE_ID", "")
    _DEFAULT_CONFIG.setdefault("TWITTER_CARD_CREATOR", "@slimshetty_")
    _DEFAULT_CONFIG.setdefault("TWITTER_CARD_CREATOR_ID", "")
    _DEFAULT_CONFIG.setdefault("GRAVATAR_URL", "")


def register():
    signals.article_generator_finalized.connect(twitter_card)
