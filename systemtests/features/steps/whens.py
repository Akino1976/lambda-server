import logging

import importlib
import builtins
import contextlib

import requests

from typing import Any, Dict, Callable, List
from types import ModuleType

from pytest_bdd import when, parsers

import helpers.utils as utils

LOGGER = logging.getLogger('lambda-server')


@when(parsers.parse('I call the {callable_path} function'))
def call_callable(request: Any, callable_path: str, parameters: Dict[str, Any], module: ModuleType):
    module = importlib.import_module(module)

    callable = getattr(module, callable_path)

    try:
        request.return_value = callable(**parameters)

    except Exception as exception:
        LOGGER.exception(f'Exception in when calling {callable_path}')

        request.raised_exception = exception


@when(parsers.parse('I make a {request_type} request to {url}'))
def make_request(request: Any,
                 request_headers: Dict[str, Any],
                 request_body: Dict[str, Any],
                 request_type: str,
                 base_url: str,
                 url: str):
    LOGGER.debug(f'Setting up request url based on the yaml spec:\n{utils.pretty_format(url)}')

    try:
        url = utils.load_with_tags(request, url)

        LOGGER.debug(f'Request url set to:\n{utils.pretty_format(url)}')

        callable = getattr(requests, request_type.lower())

        LOGGER.debug(f'Making {request_type} request to:\n{utils.pretty_format(base_url + url)}')

        request.return_value = callable(
            f'{base_url}{url}',
            headers=request_headers,
            json=request_body if request_body else None
        )

        try:
            response = request.return_value.json()
        except ValueError:
            response = request.return_value.text

        LOGGER.debug(f'Request response:\n{utils.pretty_format(response)}')

    except Exception as exception:
        msg = f'{type(exception)}\n{exception}'
        LOGGER.debug(f'The request raised the exception:\n{utils.pretty_format(msg)}')

        request.raised_exception = exception
