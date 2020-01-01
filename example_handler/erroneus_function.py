
from typing import Dict, Any


def typo_handler(event: Dict[str, Any], context: object) -> Any:
    rpint('This typo is on purpose')
