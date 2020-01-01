
from typing import Dict, Any

import connexion

from flask import jsonify

import lambda_invoker


def health():
    return 'OK', 200


def invoke_lambda(lambda_handler: str, parameters: Dict[str, Any]):
    result = lambda_invoker.invoke(
        lambda_handler=lambda_handler,
        event=parameters['event'],
        environment=parameters.get('environment', {}),
    )

    if not result['successful']:
        return {'logLines': result['log_lines'], 'error': result['error']}, 500

    return {'returnValue': result.get('data'), 'logLines': result['log_lines']}
