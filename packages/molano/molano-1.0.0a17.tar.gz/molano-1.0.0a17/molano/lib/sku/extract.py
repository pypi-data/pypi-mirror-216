# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# type: ignore
import collections
import copy
import itertools
import re
from typing import Any
from typing import Callable
from typing import AsyncIterator

import lxml.html
from headless.types import IClient

from .const import APPLE_MODELS
from .const import APPLE_IDENTIFIERS
from .utils import table_to_list


WIKI_URL: str = "https://www.theiphonewiki.com/wiki/Models"


TAGS: dict[int, str] = {
    1: 'apple:model:exclusive:cn',
    2: 'apple:model:limited:iphone6',
    3: 'apple:model:exclusive:jp',
    4: 'apple:model:exclusive:jp',
    5: 'apple:model:exclusive:cn',
    6: 'apple:model:demo',
    7: 'apple:model:exclusive:cn',
}


MACBOOKS: dict[str, Any] = {
    'MBP2023M2': {
        'name': 'MacBook Pro M2',
        'year': 2023,
        'screen_sizes': [13],
        'colors': [
            "Space Grey",
            "Silver"
        ],
        'memory': [
            "8GB",
            "16GB",
            "24GB",
        ],
        'storage': [
            "256GB",
            "512GB",
            "1TB",
            "2TB"
        ]
    },
    'MPB2023M2P': {
        'year': 2023,
        'cpu': [
            'm2p10x16',
            'm2p12x19',
        ],
        'colors': [
            "Space Grey",
            "Silver"
        ],
        'memory': [
            "16GB",
            "32GB",
        ],
        'storage': [
            "512GB",
            "1TB",
            "2TB",
            "4TB",
            "8TB",
        ]
    }
}


def parse_anumbers(row: Any, values: str) -> list[dict[str, Any]]:
    numbers: list[dict[str, Any]] = [f'A{x}' for x in str.split(values, 'A') if x and x != 'A?']
    for i, number in enumerate(numbers):
        if number == 'A?':
            numbers[i] = None
            continue
        params: dict[str, Any] = {}
        if len(number) != 5:
            m = re.match('(?P<number>.*)\[(?P<footnote>[0-9])\]$', number)
            if m is None:
                raise Exception(number)
            params['tag'] = TAGS[int(m.group('footnote'))]
            number = m.group('number')
        params['number'] = number
        numbers[i] = params
    return list(filter(bool, numbers))

async def parse_iphonewiki(
    client: IClient[Any, Any],
    kind: str,
    url: str = WIKI_URL
) -> AsyncIterator[Any]:
    response = await client.get(url=url)
    root = lxml.html.fromstring(response.content)
    for element in root.findall('.//table'):
        # Get the first row to determine which kind of models the
        # table contains.
        tbody = element[0]
        assert tbody.tag == 'tbody', tbody.tag
        try:
            first_row = tbody[1]
        except IndexError:
            continue
        name = str.strip(first_row[0].text or '')
        if len(first_row[0]) > 0: # Is a hyperlink
            name = str.strip(first_row[0][0].text)
        assert isinstance(name, str)
        if not str.lower(name).startswith(kind):
            continue
        rows = table_to_list(tbody)
        for row in rows[1:]:
            row[8] = [str.strip(x) for x in row[8].split(',')]
            row[1] = parse_anumbers(row, row[1])

            if row[8] == ['?']:
                row[8] = []
            yield row


async def parse_ipads(
    client: IClient[Any, Any],
    colors: dict[str, str],
    generate_sku: Callable[[dict[str, Any]], str] = lambda x: ''
):
    models: list[dict[str, Any]] = []
    model_identifiers: dict[Any, Any] = collections.defaultdict(set)
    async for row in parse_iphonewiki(client, 'ipad'):
        row[7] = str.replace(row[7], ' ', '')
        color_code = colors[row[6]]

        attrs = APPLE_IDENTIFIERS[row[5]]
        attrs.update(copy.deepcopy(APPLE_MODELS[row[0]]))
        msin = f"urn:msin:apple.com:"
        msin += str.lower(attrs.get('spec') or 'xx') + ':dev:ipad:'
        msin += attrs['msin']
        msin += ':' + str.lower(row[7])
        msin += ':' + str.lower(color_code)
        msin += ':' + ('w' if not attrs.get('cellular') else 'c')
        params: dict[str, int | str] = {
            'kind': 'iPad',
            'models': row[1],
            'identifier': row[5],
            'generation': 1,
            'screen_size': '',
            'screen_inch': '',
            **attrs,
            'memory'    : row[7],
            'model'     : row[7],
            'msin'      : msin,
            'series'    : row[0],
            'color'     : row[6],
            'color_code': color_code
        }
        if params.get('screen_size'):
            params['screen_inch'] = params['screen_size'].split('.')[0]
        params['sku'] = generate_sku(params)
        models.append(params)

        # Collect models
        for number in params['models']:
            k = (number['number'], row[5], row[6], row[7])
            model_identifiers[k].update(row[8])

    # Group by A numbers
    versions: dict[tuple[str, str | None], set[str]] = collections.defaultdict(set)
    for params in models:
        identifier = params['identifier']
        for model in params['models']:
            tag = model.get('tag')
            versions[(identifier, tag)].add(model['number'])

    for tag, params in itertools.product([None, *TAGS.values()], models):
        params = copy.deepcopy(params)
        identifier = params['identifier']
        numbers = versions.get((identifier, tag))
        if not numbers:
            continue
        params['tag'] = tag
        params['variants'] = []

        # Collect model numbers
        for a in list(sorted(numbers)):
            k = a, params['identifier'], params['color'], params['memory']
            params['variants'].append({
                'number': a,
                'models': list(sorted(model_identifiers[k]))
            })
        del params['models']
        yield params


async def parse_iphones(
    client: IClient[Any, Any],
    colors: dict[str, str],
    generate_sku: Callable[[dict[str, Any]], str] = lambda x: '',
):
    models: list[dict[str, Any]] = []
    model_identifiers: dict[Any, Any] = collections.defaultdict(set)
    async for row in parse_iphonewiki(client, 'iphone'):
        row[7] = str.replace(row[7], ' ', '')
        params: dict[str, int | str] = {
            'kind'      : 'iPhone',
            'generation': '',
            'models': row[1],
            'identifier': row[5],
            **copy.deepcopy(APPLE_MODELS[row[0]]),
            'memory'    : row[7],
            'model'     : row[0],
            'series'    : row[0],
            'color'     : row[6],
            'color_code': colors[row[6]]
        }
        params['sku'] = generate_sku(params)
        models.append(params)

        # Collect models
        for number in params['models']:
            k = (number['number'], row[5], row[6], row[7], False)
            model_identifiers[k].update(row[8])

    # Group by A numbers
    versions: dict[tuple[str, str | None], set[str]] = collections.defaultdict(set)
    for params in models:
        identifier = params['identifier']
        for model in params['models']:
            tag = model.get('tag')
            versions[(identifier, tag)].add(model['number'])

    seen = set()
    for tag, params in itertools.product([None, *TAGS.values()], models):
        params = copy.deepcopy(params)
        identifier = params['identifier']
        numbers = versions.get((identifier, tag))
        if not numbers:
            continue
        params['tag'] = tag
        params['variants'] = []
        k = (
            params['series'],
            params.get('tag'),
            params['memory'],
            params['color'],
            params['identifier']
        )
        del params['models']
        if k in seen:
            continue
        seen.add(k)

        # Collect model numbers
        for a in list(sorted(numbers)):
            k = a, params['identifier'], params['color'], params['memory'], False
            s = model_identifiers[k]
            for n in s:
                if not n.endswith('[6]'):
                    continue
                s.add(n[:-3])
                s.remove(n)
            params['variants'].append({
                'number': a,
                'model': list(sorted(s))
            })

        if params['memory'] == '32GB[2]' and params['series'] == 'iPhone 6':
            params['memory'] = '32GB'
            params['year'] = 2017
        yield params

#        1: 'apple:model:exclusive:cn',
#    2: 'apple:model:limited:iphone6',
#    3: 'apple:model:exclusive:jp',
#    4: 'apple:model:exclusive:jp',
#    5: 'apple:model:exclusive:cn',
#    6: 'apple:model:demo',
#    7: 'apple:model:exclusive:cn',