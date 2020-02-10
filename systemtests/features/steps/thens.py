import logging

from pytest_bdd import then, parsers
from types import ModuleType
from typing import Any, Dict, Callable, List

import requests

import helpers.utils as utils

LOGGER = logging.getLogger('lambda-server')


@then(parsers.parse('the string to be longer than {length} characters'))
def check_string_length(request, length):
    assert int(length) < len(request.return_value)


@then(parsers.parse('all items contains the key {key}'))
def list_contains_keys(request, key):
    data = request.return_value['data']
    assert len(data) > 0

    for item in data:
        assert key in item.keys()


@then(parsers.parse('the result should contain:\n{yaml_string}'))
def should_contain(request: Any, yaml_string: Any):
    assert yaml_string in request.return_value


@then(parsers.parse('the HTTP status code should be {status}'))
def http_status(request: Any, status: str):
    """Verify the HTTP status of a response"""

    expected_status = requests.codes.get(status)
    actual_status = request.return_value.status_code

    assert expected_status == actual_status


@then(parsers.parse('the JSON response body should contain:\n{yaml_string}'))
def json_response_body_contains(request: Any, yaml_string: str):
    LOGGER.debug(f'Validating response body based on the yaml spec:\n{utils.pretty_format(yaml_string)}')

    expected_response_body = utils.load_with_tags(request, yaml_string)

    LOGGER.debug(f'Response body yaml spec parsed to:\n{utils.pretty_format(expected_response_body)}')

    actual_response_body = request.return_value.json()

    assert utils.comparisons.contains(actual_response_body, expected_response_body)
