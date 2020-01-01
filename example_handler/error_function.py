
from typing import Dict, Any


def error_on_call_handler(event: Dict[str, Any], context: object):
    print('error_on_call_handler successfully invoked')

    raise Exception('Oh no')
