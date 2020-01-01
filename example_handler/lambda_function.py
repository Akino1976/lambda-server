
import os

from typing import Dict, List, Any

import inflection


class MissingWordException(Exception):
    pass


def json_handler(event: Dict[str, Any], context: object) -> Dict[str, Any]:
    word = event.get('word')

    if not word:
        raise MissingWordException('No word in event')

    print('json_handler successfully invoked!')
    print('Here is the event:')
    print(event)

    return {
        'singular': inflection.singularize(word),
        'plural': inflection.pluralize(word)
    }


def array_handler(event: Dict[str, Any], context: object) -> List[str]:
    word = event.get('word')

    if not word:
        raise MissingWordException('No word in event')

    print('array_handler successfully invoked!')
    print('Here is the event:')
    print(event)

    return [
        inflection.singularize(word),
        inflection.pluralize(word),
    ]


def text_handler(event: Dict[str, Any], context: object) -> str:
    word = event.get('word')

    if not word:
        raise MissingWordException('No word in event')

    print('text_handler successfully invoked!')
    print('Here is the event:')
    print(event)

    return f'{inflection.singularize(word)} in plural is {inflection.pluralize(word)}'


def null_handler(event: Dict[str, Any], context: object):
    word = event.get('word')

    if not word:
        raise MissingWordException('No word in event')

    print('none_handler successfully invoked!')
    print('Here is the event:')
    print(event)

    print('Not returning anything since that is the point')


def environment_handler(event: Dict[str, Any], context: object) -> Dict[str, Any]:
    variables = event['variables']

    return {variable: os.getenv(variable) for variable in variables}
