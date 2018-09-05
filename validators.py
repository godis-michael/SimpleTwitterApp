from functools import wraps
from typing import Pattern

from flask import jsonify, request
from tweepy import TweepError


ERRORS = dict(FORMAT='{key} format is not valid',
              POS_INT_RANGE='pages_limit parameter should be a value from a positive integer range',
              CONVERSION='error converting pages_limit parameter`s value, should be a number')


def error_handler(key: str, parameter_pattern: Pattern):
    """
    Simple decorator for errors handling and converting them into json object

    :param key: function`s argument name, needed to resolve kwargs object
    :param parameter_pattern: compiled regex pattern to match function argument`s value
    :return: decorated flask routed function
    """

    def wrapper(func):
        @wraps(func)
        def wrapped(**kwargs):
            try:
                if not parameter_pattern.match(kwargs[key]):  # if value format is not valid
                    return jsonify({'error': ERRORS['FORMAT'].format(key=key)})

                pages_limit = int(request.args.get('pages_limit', 1))
                if pages_limit < 1:  # if pages_limit value is not valid
                    return jsonify({'error': ERRORS['POS_INT_RANGE']})

                return func(kwargs.pop(key), pages_limit)

            except TweepError as e:  # any twitter api error
                result = {'error': e.reason}
            except ValueError:  # can not convert pages_limit value
                result = {'error': ERRORS['CONVERSION']}

            return jsonify(result)

        return wrapped
    return wrapper
