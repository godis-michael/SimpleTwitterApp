from collections import defaultdict

import tweepy
from flask import Flask, render_template, jsonify

from config import PATS, TwitterConfig, init_api
from validators import error_handler

__all__ = ['app', 'search_hashtags', 'search_users']

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title=app.name)


@app.route('/hashtags/<string:hashtag>/')
@error_handler('hashtag', PATS['hashtag'])
def search_hashtags(hashtag: str, pages_limit: int):
    """
    Find tweets by a hashtag

    :param hashtag: valid hashtag string
    :param pages_limit: pages limit to display, set to 1 by default
    :return: json response with tweets found by a hashtag or error information
    """

    result = defaultdict(list)
    for index, page in enumerate(tweepy.Cursor(app.config['API'].search, q=f'#{hashtag}').pages(pages_limit)):
        for tweet in page:
            result[f'page {index+1}'].append(tweet._json)

    return jsonify(result)


@app.route('/users/<string:username>/')
@error_handler('username', PATS['username'])
def search_users(username: str, pages_limit: int):
    """
    Find user`s tweets by a username

    :param username: valid screen user name
    :param pages_limit: pages limit to display, set to 1 by default
    :return: json response with user`s tweets or error information
    """

    result = defaultdict(list)
    for index, page in enumerate(
            tweepy.Cursor(app.config['API'].user_timeline, screen_name=username, count=10).pages(pages_limit)):
        for tweet in page:
            result[f'page {index+1}'].append(tweet._json)

    return jsonify(result)


if __name__ == '__main__':
    TwitterConfig(app)  # configure Twitter API credentials
    app.config['API'] = init_api(app)

    app.run(debug=True)
