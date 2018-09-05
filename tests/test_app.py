import json
from json import JSONDecodeError
from flask import request

import pytest
from decouple import UndefinedValueError
from tweepy import TweepError

from SimpleTwitterApp import app
from validators import ERRORS
from config import TwitterConfig, init_api


def credentials_validity():
    """
    This function checks if the Twitter API credentials are set and valid

    :return: dictionary with appropriate keyword argument for pytest.mark.skipif decorator
    """

    condition, reason = False, 'Default'  # default values, if credentials are correct
    try:
        with TwitterConfig(app) as _:
            api = init_api(app)
            api.get_user('Twitter')
    except UndefinedValueError:
        condition, reason = True, 'This test requires all Twitter credentials to be specified in .env file either in ' \
                                  'environment'
    except TweepError:
        condition, reason = True, 'This test requires valid Twitter API credentials'

    return dict(condition=condition, reason=reason)


skipif_kwarg = credentials_validity()  # cache call to the function


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with TwitterConfig(app) as _:
        app.config['API'] = init_api(app)
        yield app.test_client()


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_value_not_specified_in_url(client):
    response = client.get('/hashtags/')

    assert response.status_code == 404


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_returns_200_status_code(client):
    response = client.get('/hashtags/HelloWorld/')

    assert response.status_code == 200


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_context_check():
    with app.test_request_context('/hashtags/HelloWorld?pages_limit=3'):
        assert request.method == 'GET'
        assert request.path == '/hashtags/HelloWorld'
        assert request.args['pages_limit'] == '3'


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_returns_valid_json_response(client):
    response = client.get('/hashtags/HelloWorld/')

    assert response.is_json is True


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_returns_decodable_json_data(client):
    response = client.get('/hashtags/HelloWorld/')
    try:
        json.loads(response.data)
    except JSONDecodeError:
        pytest.fail('Failed decode response into json object')


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_returns_json_with_valid_data(client):
    response = client.get('/hashtags/HelloWorld/')
    data = json.loads(response.data)

    assert len(data['page 1']) > 0


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_with_invalid_format_returns_json_with_error(client):
    response = client.get('/hashtags/Hello World/')
    error = json.loads(response.data)

    assert error['error'] == ERRORS['FORMAT'].format(key='hashtag')


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_with_only_underscore_returns_json_with_error(client):
    response = client.get('/hashtags/_/')
    error = json.loads(response.data)

    assert error['error'] == 'Twitter error response: status code = 403'


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_with_pages_limit_3_returns_valid_json(client):
    response = client.get('/hashtags/HelloWorld/?pages_limit=3')
    data = json.loads(response.data)

    assert len(data) == 3


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_with_invalid_pages_limit_number_returns_json_with_error(client):
    response = client.get('/hashtags/HelloWorld/?pages_limit=-1')
    error = json.loads(response.data)

    assert error['error'] == ERRORS['POS_INT_RANGE']


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_with_invalid_pages_limit_value_returns_json_with_error(client):
    response = client.get('/hashtags/HelloWorld/?pages_limit=nan')
    error = json.loads(response.data)

    assert error['error'] == ERRORS['CONVERSION']


@pytest.mark.skipif(**skipif_kwarg)
def test_username_value_not_specified_in_url(client):
    response = client.get('/users/')

    assert response.status_code == 404


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_returns_200_status_code(client):
    response = client.get('/users/Twitter/')

    assert response.status_code == 200


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_context_check():
    with app.test_request_context('/users/Twitter?pages_limit=3'):
        assert request.method == 'GET'
        assert request.path == '/users/Twitter'
        assert request.args['pages_limit'] == '3'


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_returns_valid_json_response(client):
    response = client.get('/users/Twitter/')

    assert response.is_json is True


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_returns_decodable_json_data(client):
    response = client.get('/users/Twitter/')
    try:
        json.loads(response.data)
    except JSONDecodeError:
        pytest.fail('Failed decode response into json object')


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_returns_json_with_valid_data(client):
    response = client.get('/users/Twitter/')
    data = json.loads(response.data)

    assert len(data['page 1']) > 0


@pytest.mark.skipif(**skipif_kwarg)
def test_hashtag_request_with_invalid_format_returns_json_with_error(client):
    response = client.get('/users/Twit.ter/')
    error = json.loads(response.data)

    assert error['error'] == ERRORS['FORMAT'].format(key='username')


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_with_non_existent_user_returns_json_with_error(client):
    response = client.get('/users/sdabkshdadh/')
    error = json.loads(response.data)

    assert error['error'] == 'Twitter error response: status code = 404'


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_with_pages_limit_3_returns_valid_json(client):
    response = client.get('/users/Twitter/?pages_limit=3')
    data = json.loads(response.data)

    assert len(data) == 3


@pytest.mark.skipif(**skipif_kwarg)
def test_user_request_with_invalid_pages_limit_number_returns_json_with_error(client):
    response = client.get('/users/Twitter/?pages_limit=-1')
    error = json.loads(response.data)

    assert error['error'] == ERRORS['POS_INT_RANGE']


@pytest.mark.skipif(**skipif_kwarg)
def test_users_request_with_invalid_pages_limit_value_returns_json_with_error(client):
    response = client.get('/users/Twitter/?pages_limit=nan')
    error = json.loads(response.data)

    assert error['error'] == ERRORS['CONVERSION']