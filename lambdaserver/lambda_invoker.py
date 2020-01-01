
import os
import json
import subprocess
import sys

from typing import Dict, Any


def _try_parse(body: Any) -> Any:
    try:
        return json.loads(body)

    except Exception as e:
        print(f'Failed to parse json: {e}')

        return body


def _try_parse_error(body: Any) -> Any:
    try:
        if '\x1b[31m' in body:
            chunks = body.split('\x1b[31m')
            body = chunks[1].split('\x1b[0m')[0]

        return json.loads(body)

    except Exception as e:
        print(f'Failed to parse error json: {e}')

        return body


def invoke(lambda_handler: str,
           event: Dict[str, Any],
           environment: Dict[str, Any]) -> Dict[str, Any]:

    command = [
        '/var/rapid/init',
        '--bootstrap',
        '/var/runtime/bootstrap'
    ]

    current_environment = os.environ.copy()

    environment.update({
        'AWS_LAMBDA_EVENT_BODY': json.dumps(event, ensure_ascii=False),
        'AWS_LAMBDA_FUNCTION_HANDLER': lambda_handler,
    })

    current_environment.update(environment)

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=current_environment,
    )

    print('\n======== Lambda logs: ========\n')

    lambda_logs = ''

    while True:
        log_output = str(process.stderr.readline(), 'utf-8')

        if log_output != '':
            lambda_logs += log_output

            sys.stdout.write(log_output)

        if process.poll() is not None:
            break

    output = _try_parse(str(process.stdout.read(), 'utf-8'))
    parsed_error = _try_parse_error(lambda_logs)
    log_lines = lambda_logs.split('\n')

    if log_lines[-1] == '':
        log_lines = log_lines[:-1]

    print('\n==============================\n')

    if 0 < process.returncode:
        if isinstance(parsed_error, dict) and parsed_error.get('stackTrace'):
            parsed_error['stackTrace'] = [
                [
                    str(item).strip()
                    for item in stack_trace.split('\n')
                    if len(str(item).strip()) > 0
                ]
                for stack_trace in parsed_error['stackTrace']
            ]

        return {'log_lines': log_lines, 'successful': False, 'error': parsed_error}

    return {'data': output, 'log_lines': log_lines, 'successful': True}
