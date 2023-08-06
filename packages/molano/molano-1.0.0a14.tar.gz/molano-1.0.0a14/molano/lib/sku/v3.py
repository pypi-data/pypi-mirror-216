# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .const import APPLE_MODELS
from .v2 import APPLE_COLORS


GRADES: dict[str, str] = {
    'A+'    : '0',
    'A'     : '1',
    'B+'    : '2',
    'B'     : '3',
    'C+'    : '4',
    'C'     : '5',
}


def generate_sku(params: dict[str, Any]) -> str:
    kind = params.get('kind')
    color_code = APPLE_COLORS[params['color']] if params['color'] else None
    is_bulk = params.get('bulk')
    is_trading = params.get('trading')
    model_suffix: str = ''
    if is_bulk:
        model_suffix = 'B'
    if is_trading:
        model_suffix = 'T'
    match kind:
        case "iPad":
            raise NotImplementedError
        case "iPhone":
            params.update(APPLE_MODELS[params['model']]) # type: ignore
            params.setdefault('generation', '')
            if color_code:
                sku = '{base}{color_code}{storage}'.format(color_code=color_code, **params)
            else:
                sku = '{base}{model_suffix}{storage}'.format(color_code=color_code, model_suffix=model_suffix, **params)
        case _:
            raise NotImplementedError
    if params.get('restricted'):
        sku += params['restricted']
    if params.get('grade'):
        grade: str = params['grade']
        if not grade.isdigit():
            grade = GRADES[grade]
        sku += grade
    return sku