# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.types import IClient
from . import extract
from .const import APPLE_MODELS


APPLE_COLORS: dict[str, str] = {
    'Alpine Green'  : 'GR',
    'Black'         : 'B',
    'Black & Slate' : 'BS',
    'Blue'          : 'BL',
    'Coral'         : 'C',
    'Deep Purple'   : 'P',
    'Graphite'      : 'G',
    'Green'         : 'GR',
    'Gold'          : 'GO',
    'Jet Black'     : 'JB',
    'Midnight'      : 'M',
    'Midnight Green': 'MG',
    'Pink'          : 'PI',
    'Red'           : 'RE',
    'Rose Gold'     : 'GO',
    'PRODUCT(RED)'  : 'R',
    'Pacific Blue'  : 'BL',
    'Purple'        : 'P',
    'Sierra Blue'   : 'BL',
    'Silver'        : 'S',
    'Space Black'   : 'SBL',
    'Space Gray'    : 'SG',
    'Sky Blue'      : 'SK',
    'Starlight'     : 'ST',
    'White'         : 'W',
    'White & Silver': 'WS',
    'Yellow'        : 'Y',
}

GRADES: dict[str, str] = {
    'A+'    : '0',
    'A'     : '1',
    'B+'    : '2',
    'B'     : '3',
    'C+'    : '4',
    'C'     : '5',
    'D'     : '6'
}
GRADES.update({v: k for k, v in GRADES.items()})


def get_color(color: str) -> str:
    return APPLE_COLORS[color]


def generate_sku(params: dict[str, Any]):
    kind = params['kind']
    color_code = params.pop('color_code', None)
    if params.get('color') and not color_code:
        color_code = APPLE_COLORS[params['color']]
    if not params.get('storage') and params.get('memory'):
        params['storage'] = params['memory']
    match kind:
        case 'iPhone':
            sku = generate_iphone_sku({**params, 'color_code': color_code})
        case 'iPad':
            if params['base'] != 'IPA':
                sku =  '{base}{generation}{screen_inch}{color_code}{storage}'.format(color_code=color_code, **params)
            else:
                sku =  '{base}{generation}{color_code}{storage}'.format(color_code=color_code, **params)
            sku += 'C' if params.get('cellular') else 'W'
            if params.get('restricted'):
                sku += params['restricted']
            if params.get('grade'):
                sku += params['grade']
        case _:
            raise NotImplementedError
    return sku

def generate_iphone_sku(params: dict[str, str]):
    params.update(APPLE_MODELS[params['model']]) # type: ignore
    params.setdefault('generation', '')
    if not params.get('device'):
        params['device'] = params['series']
    if params.get('color') and params.get('storage'):
        sku = '{base}{color_code}{storage}'.format(**params)
        if params.get('restricted'):
            sku += params['restricted']
        if params.get('grade'):
            grade = params['grade']
            params['grade_name'] = GRADES[grade]
            if not grade.isdigit():
                grade = GRADES[grade]
            sku += grade
        return sku
    elif params.get('storage'):
        return '{base}{memory}'.format(**params)
    else:
        return '{base}'.format(**params)

def parse_iphones(
    client: IClient[Any, Any]
):
    return extract.parse_iphones(
        client,
        colors=APPLE_COLORS,
        generate_sku=generate_iphone_sku
    )


def parse_ipads(
    client: IClient[Any, Any]
):
    return extract.parse_ipads(
        client,
        colors=APPLE_COLORS,
        generate_sku=lambda params: '{base}{generation}{screen_inch}{color_code}{memory}'.format(**params)
    )