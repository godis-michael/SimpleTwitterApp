import os
import re

import tweepy
from decouple import config
from flask import Flask


BASEDIR = os.path.dirname(os.path.abspath(__file__))
DOT_ENV = os.path.join(BASEDIR, '.env')
PATS = dict(hashtag=re.compile(r'^[a-zA-Z0-9_]+$'),
            username=re.compile(r'^[a-zA-Z0-9_]{1,15}$'))
TWITTER_VARS = ('CONSUMER_KEY', 'CONSUMER_SECRET', 'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')


class TwitterConfig:
    """
    Configuration class for the Twitter credentials.
    Made with contextmanager support, so settings could be set temporarily.

    Note: variables set in environment are prior to same, set in .env file
    """

    def __init__(self, app: Flask):
        self.app = app
        self.update()

    def update(self):
        """
        Reload configuration from .env file

        :return: sets Flask configuration from the class object
        """

        config._load('.env')  # reload .env file
        for var in TWITTER_VARS:  # construct class attributes
            setattr(self.__class__, var, config(var))
        self.app.config.from_object('config.TwitterConfig')  # load object into a Flask configuration

    def __enter__(self):
        return self.app.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        config = self.app.config
        for var in TWITTER_VARS:
            config.pop(var, None)


def init_api(app: Flask):
    """
    Initialize Twitter API connection

    :param app: Flask class instance
    :return: tweepy API instance
    """

    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    auth.set_access_token(app.config['ACCESS_TOKEN'], app.config['ACCESS_TOKEN_SECRET'])

    return tweepy.API(auth)
