
import os

from typing import Dict, Any

import inflection


def lambda_handler(event: Dict[str, Any], context: object) -> Dict[str, Any]:
    word = event.get('word', 'lambda')

    print('json_handler successfully invoked!')
    print('Here is the event:')
    print(event)

    return {
        'word': {
            'singular': inflection.singularize(word),
            'plural': inflection.pluralize(word),
        },
        'originalEvent': event,
    }
