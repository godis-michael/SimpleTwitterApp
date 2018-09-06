import os
import pytest
import tweepy
from decouple import UndefinedValueError
from base64 import b32encode

from tweepy import TweepError
from typing import Iterable

from config import PATS, DOT_ENV, TWITTER_VARS, TwitterConfig, init_api
from SimpleTwitterApp import app


def hashtag_match(hashtag):
    match = PATS['hashtag'].match(hashtag)
    return match.string == hashtag if match else False


def username_match(username):
    match = PATS['username'].match(username)
    return match.string == username if match else False


def generate_tokens(vars, callback=None):
    for var in vars:
        token = b32encode(os.urandom(32)).decode()
        if callback:
            callback(var, token)

        yield token


@pytest.fixture
def dotenv():
    app.config['TESTING'] = True
    file_backup = ''
    vars_backup = {}
    try:
        f = open(DOT_ENV, 'r+')
        file_backup = f.read()
        if file_backup:  # clear file if it is not empty
            f.seek(0)
            f.truncate()

        vars_backup = os_make_backup(TWITTER_VARS)
        yield f

    finally:
        os_restore_backup(vars_backup)
        with open(DOT_ENV, 'w+') as f:  # restore previous content
            f.write(file_backup)


def os_make_backup(vars: Iterable):
    """
    Remove system variables by their names

    :param vars: iterable with system variables names
    :return: dictionary with names, values of removed variables
    """

    backup = {}
    for var in vars:
        backuped_var = os.environ.pop(var, None)
        if backuped_var:
            backup[var] = backuped_var

    return backup


def os_restore_backup(backup: dict):
    """
    Set system variables from dictionary

    :param backup: dictionary object with system variables names and their values
    :return: system variables are set
    """

    for key, value in backup.items():
        os.environ[key] = value


def test_hashtag_match():
    assert hashtag_match('HelloWorld') is True


def test_hashtag_unmatch():
    assert hashtag_match('Hello World') is False


def test_username_match():
    assert username_match('Twitter') is True


def test_username_incorrect_charchters():
    assert username_match('new.user') is False


def test_username_too_long():
    assert username_match('superlongusername') is False


def test_environment_setup_from_dotenv_file(dotenv):
    try:
        dotenv_write = lambda key, token: dotenv.write(f'{key}={token}\n')
        tokens = list(generate_tokens(TWITTER_VARS, dotenv_write))
    finally:
        dotenv.close()  # close .env file

    app_config_vars = []
    with TwitterConfig(app) as config:
        for var in TWITTER_VARS:
            app_config_vars.append(config[var])

    assert app_config_vars == tokens


def test_environment_setup_failed_when_any_required_variable_is_not_set(dotenv):
    try:
        dotenv_truncated_write = lambda key, token: dotenv.write(f'{key}={token}\n')
        generate_tokens(TWITTER_VARS[:-1], dotenv_truncated_write)
    finally:
        dotenv.close()

    with pytest.raises(UndefinedValueError):
        with TwitterConfig(app) as _:
            pass


def test_environment_setup_from_system_variables():
    os_setup = lambda key, token: os.environ.__setitem__(key, token)
    tokens = list(generate_tokens(TWITTER_VARS, os_setup))

    app_config_vars = []
    with TwitterConfig(app) as config:
        for var in TWITTER_VARS:
            app_config_vars.append(config[var])

    assert app_config_vars == tokens


def test_api_initialized_successfully():
    os_setup = lambda key, token: os.environ.__setitem__(key, token)
    generate_tokens(TWITTER_VARS, os_setup)

    with TwitterConfig(app) as _:
        api = init_api(app)

    assert api.__class__ is tweepy.API


def test_api_cant_initialize_without_credentials():
    with pytest.raises(KeyError):
        init_api(app)


def test_api_with_random_credentials_fails():
    os_setup = lambda key, token: os.environ.__setitem__(key, token)
    generate_tokens(TWITTER_VARS, os_setup)

    with TwitterConfig(app) as _:
        api = init_api(app)

        with pytest.raises(TweepError) as error_info:
            api.get_user('Twitter')

        assert str(error_info.value) == '[{\'code\': 215, \'message\': \'Bad Authentication data.\'}]'
