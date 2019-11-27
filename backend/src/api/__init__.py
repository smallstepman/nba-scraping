"""
    connexion doesn't support OpenAPI 100%,
    one of the things that's not working is
    debundling large .yaml files into smaller
    ones: https://github.com/zalando/connexion/issues/254
"""

import prance
from typing import Any, Dict
from pathlib import Path


def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
    parser = prance.ResolvingParser(str(main_file.absolute()),
                                    lazy = True, backend = 'openapi-spec-validator')
    parser.parse()
    return parser.specification
