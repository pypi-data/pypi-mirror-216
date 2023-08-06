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
    'Alpine Green'  : 'ALP',
    'Black'         : 'BLA',
    'Black & Slate' : 'BLS',
    'Blue'          : 'BLU',
    'Coral'         : 'COR', # ???
    'Deep Purple'   : 'DEE',
    'Graphite'      : 'GRA',
    'Green'         : 'GRE',
    'Gold'          : 'GOL',
    'Jet Black'     : 'JET',
    'Midnight'      : 'MID',
    'Midnight Green': 'MIG', # ???
    'Pink'          : 'PIN',
    'Red'           : 'RED',
    'Rose Gold'     : 'ROS',
    'PRODUCT(RED)'  : 'PRO',
    'Pacific Blue'  : 'PAC',
    'Purple'        : 'PUR',
    'Sierra Blue'   : 'SIE',
    'Silver'        : 'SIL',
    'Space Black'   : 'SPB',
    'Space Gray'    : 'SPA',
    'Space Grey'    : 'SPA',
    'Sky Blue'      : 'SKY',
    'Starlight'     : 'STA',
    'White'         : 'WHI',
    'White & Silver': 'WHS',
    'Yellow'        : 'YEL',
}
APPLE_COLOR_CODES: dict[str, str] = {v: k for k, v in APPLE_COLORS.items()}
APPLE_COLORS.update({k.lower(): v for k, v in APPLE_COLORS.items()})
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


def generate_sku(params: dict[str, Any]) -> str:
    kind = params.get('kind')
    color_code = params.pop('color_code', None)
    if not params.get('storage') and params.get('memory'):
        params['storage'] = params['memory']
    if params.get('color'):
        color_code = APPLE_COLORS[params['color']]
    match kind:
        case "iPad":
            if params['base'] != 'IPA':
                sku = '{base}{generation}{screen_inch}{color_code}{storage}'.format(color_code=color_code, **params)
            else:
                sku = '{base}{generation}{color_code}{storage}'.format(color_code=color_code, **params)
            sku += 'C' if params.get('cellular') else 'W'
        case "iPhone":
            params.update(APPLE_MODELS[params['model']]) # type: ignore
            params.setdefault('generation', '')
            sku = '{base}{color_code}{storage}'.format(color_code=color_code or '', **params)
        case _:
            raise NotImplementedError
    if params.get('restricted'):
        sku += params['restricted']
    if params.get('grade'):
        grade: str = params['grade']
        params['grade_name'] = GRADES[grade]
        if not grade.isdigit():
            grade = GRADES[grade]
        assert grade.isdigit()
        sku += grade

    if not params.get('device'):
        params['device'] = params['series']
    return sku


def parse_iphones(
    client: IClient[Any, Any]
):
    return extract.parse_iphones(
        client,
        colors=APPLE_COLORS,
        generate_sku=lambda params: '{base}{generation}{color_code}{memory}'.format(**params)
    )


def parse_ipads(
    client: IClient[Any, Any]
):
    return extract.parse_ipads(
        client,
        colors=APPLE_COLORS,
        generate_sku=lambda params: '{base}{generation}{screen_inch}{color_code}{memory}'.format(**params)
    )