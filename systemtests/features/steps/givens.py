import logging

from typing import Dict, Any

from pytest_bdd import given, parsers
from types import ModuleType

import helpers.utils as utils

import yaml

LOGGER = logging.getLogger('lambda-server')


@given(parsers.parse('the request body:\n{yaml_string}'), target_fixture='request_body')
def create_request_body(request: Any, yaml_string: Any) -> Any:
    yaml_string = yaml.load(yaml_string, Loader=yaml.FullLoader)

    LOGGER.info(f'Request body set to:\n{utils.pretty_format(yaml_string)}')

    return yaml_string


@given(parsers.parse('the parameters:\n{yaml_string}'), target_fixture='parameters')
def create_parameters(request: Any, yaml_string: Dict[str, Any]) -> Dict[str, Any]:
    LOGGER.info(f'Parameters set to:\n{utils.pretty_format(yaml_string)}')

    return yaml.load(yaml_string, Loader=yaml.FullLoader)


@given(parsers.parse('the module {module:S}'))
def set_module(module: str):
    LOGGER.info(f'Base module set to {module}')

    pass
