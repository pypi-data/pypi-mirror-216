# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# type: ignore
import asyncio
import collections
import copy
import hashlib
import re
import sys
from typing import Any

import yaml
from headless.core import httpx

from molano.lib import appleparts
from molano.lib import spot
from molano.lib.sku import v1
from molano.lib.sku import v2
from molano.lib.sku import extract


_generations: dict[int, str] = collections.defaultdict(lambda: '{n}th', {
    1: '{n}st',
    2: '{n}nd',
    3: '{n}rd',
})


APPLE_GRADES: list[tuple[str, str]] = [
    ('0', 'A+'),
    ('1', 'A'),
    ('2', 'B+'),
    ('3', 'B'),
    ('4', 'C+'),
    ('5', 'C')
]

def create_battery(params: dict[str, Any]) -> dict[str, Any]:
    params = copy.deepcopy(params)
    base = params['base']
    if base.startswith('IPHSE'):
        base = f"{base}{params['year']}"
    search_keys: list[str] = []

    h = hashlib.sha1()
    h.update(str.encode('apple', 'utf-8'))
    h.update(str.encode('apple', 'utf-8'))
    h.update(str.encode(base, 'utf-8'))

    return {
        'kind': 'Part',
        'catalog_name': f"{params['series']} Battery + Adhesive Tape",
        'name': f"{params['series']} Battery + Adhesive Tape",
        'namespaces': ['catalog.buymolano.com'],
        'product_type': 'FINISHED_GOOD',
        'search_keys': [
            h.hexdigest(),
            f"BATT{base}"
        ]
    }

def create_msin_name(product: dict[str, Any]) -> str | None:
    msin_name = None
    if product['kind'] == 'iPad':
        msin_name = f"{product['model']}"
        if product['model'] == 'iPad Pro':
            msin_name += f" {product['screen_size']}\""
        msin_name += f" {product['storage']}"
        msin_name += ' Wi-Fi' if not product['cellular'] else ' Wi-Fi + Cellular'
        msin_name += f" {product['color']}"
        generation = format_generation(product['generation']) + ' generation'
        if product['restricted'] == 'CN':
            generation += ', China'
        if product['restricted'] == 'JP':
            generation += ', Japan'
        msin_name = f'{msin_name} ({generation})'
    elif product['kind'] == 'iPhone':
        msin_name = "{model} {storage} {color}".format(**product)
        if product['restricted'] == 'CN':
            msin_name = f'{msin_name} (China)'
        if product['restricted'] == 'JP':
            msin_name = f'{msin_name} (Japan)'
    return msin_name


def create_variant_name(
    product: dict[str, Any],
    variant: dict[str, Any],
    color: str
) -> str:
    name = f"{product['name']} {color}"
    if product['kind'] == 'iPhone':
        name = '{model} {storage} {color}'.format(
            color=color,
            **product
        )
        if product['restricted'] == 'CN':
            name = f'{name} China'
        if product['restricted'] == 'JP':
            name = f'{name} Japan'
    return name


def create_bulk_name(params: dict[str, Any]) -> str | None:
    if params['kind'] != 'iPhone':
        return None
    memory = re.sub('^([0-9]+)(GB|TB)$', r'\1 \2', params['memory'])
    if params.get('series', '').startswith('iPhone SE'):
        name = f"iPhone SE ({params['year']})"
        if str.endswith(params.get('tag') or '', 'jp'):
            name = f"iPhone SE ({params['year']}, Japan)"
        elif str.endswith(params.get('tag') or '', 'cn'):
            name = f"iPhone SE ({params['year']}, China)"
        name += f" {memory}"
    else:
        name = f"{params['series']} {memory}"
        if str.endswith(params.get('tag') or '', 'jp'):
            name = f"{name} (Japan)"
        elif str.endswith(params.get('tag') or '', 'cn'):
            name = f"{name} (China)"
    return f'Bulk {name}'

def create_product_name(params: dict[str, Any]) -> str:
    memory = re.sub('^([0-9]+)(GB|TB)$', r'\1 \2', params['memory'])
    if params.get('series', '').startswith('iPhone SE'):
        name = f"iPhone SE ({params['year']})"
        if str.endswith(params.get('tag') or '', 'jp'):
            name = f"iPhone SE ({params['year']}, Japan)"
        elif str.endswith(params.get('tag') or '', 'cn'):
            name = f"iPhone SE ({params['year']}, China)"
        name += f" {memory}"
    elif params['kind'] == 'iPhone':
        name = f"{params['series']} {memory}"
        if str.endswith(params.get('tag') or '', 'jp'):
            name = f"{name} (Japan)"
        elif str.endswith(params.get('tag') or '', 'cn'):
            name = f"{name} (China)"
    elif params['kind'] == 'iPad':
        name = f"{params['device']}"
        if params.get('screen_size') and params.get('series') not in {'iPad', 'iPad mini'} and params.get('device') != 'iPad':
            name = f"{name} {params['screen_size']}\""
        if str.endswith(params.get('tag') or '', 'jp'):
            name = f"{name} ({params['year']}, Japan)"
        elif str.endswith(params.get('tag') or '', 'cn'):
            name = f"{name} ({params['year']}, China)"
        else:
            name = f"{name} ({params['year']})"
        name += f" {memory}"
        name += f" {'Cellular' if params.get('cellular') else 'Wi-Fi'}"
    else:
        raise NotImplementedError
    return name



def format_generation(n: int) -> str:
    return _generations[n].format(n=n)

def get_catalog_name(params: dict[str, Any]) -> str | None:
    name = None
    if params['kind'] == 'iPhone':
        name = f"{params['model']} {params['storage']} {params['color']} {params['grade_name']}"
    if params['kind'] == 'iPad':
        name = f"{params['model']} {params['storage']} ({params['year']})"
        if params.get('restricted') == 'CN':
            name = f"{params['model']} {params['storage']} ({params['year']}, China)"
        if params.get('restricted') == 'JP':
            name = f"{params['model']} {params['storage']} ({params['year']}, Japan) "
        if params['model'] == 'iPad Pro':
            name += f" {params['screen_inch']}\""
        name += " Wi-Fi" if not params.get('cellular') else " Wi-Fi + Cellular"
        name += f" {params['color']} {params['grade_name']}"
    return name


async def main():
    async with httpx.Client(base_url="", timeout=10) as client:
        parts = [
            #*(await appleparts.parse(client)),
            #*(await spot.parse_selfservicerepair(client))
        ]

        models = [
            #[row async for row in extract.parse_ipads(client, v2.APPLE_COLORS)],
            *[row async for row in extract.parse_iphones(client, v2.APPLE_COLORS)],
        ]

        # Create bulk
        series: dict[str, dict[str, Any]] = collections.defaultdict(lambda: {
            'features': [],
        })
        bulk: dict[tuple[str, str, str], dict[str, str | set[str]]] = collections.defaultdict(
            lambda: {
                'identifiers': [],
                'features': []
            }
        )
        batteries: dict[str, Any] = {}
        grades: dict[str, str] = {
            'A+'    : '0',
            'A'     : '1',
            'B+'    : '2',
            'B'     : '3',
            'C+'    : '4',
            'C'     : '5',
            'Any'   : None
        }
        for model in models:
            # Group products by series, market, storage and collect possible colors
            if model.get('year') < 2014:
                continue
            name = create_product_name(model)
            storage = {
                'kind': 'Generic',
                'category': 'primaryhd',
                'applicable': 'REQ',
                'label': re.sub('^([0-9]+)(GB|TB)$', r'\1 \2', model['memory'])
            }
            product = series[name]
            product['product_name'] = name
            if storage not in product['features']:
                product['features'].append(storage)

            kind_feature = {
                'kind': 'Generic',
                'category': 'apple.com/kind',
                'applicable': 'REQ',
                'label': model['kind']
            }
            if kind_feature not in product['features']:
                product['features'].append(kind_feature)

            model_feature = {
                'kind': 'Generic',
                'category': 'apple.com/model',
                'applicable': 'REQ',
                'label': model['series']
            }
            if model_feature not in product['features']:
                product['features'].append(model_feature)
            color_feature = {
                'kind': 'Generic',
                'category': 'apple.com/color',
                'applicable': 'SEL',
                'unique': True,
                'label': model['color']
            }
            if color_feature not in product['features']:
                product['features'].append(color_feature)
            restrict = None
            country = None
            if model.get('tag'):
                t = {
                    'CN': 'China',
                    'JP': 'Japan'
                }
                country = str.upper(model['tag'].split(':')[-1])
                restrict = {
                    'kind': 'Generic',
                    'category': 'apple.com/restriction',
                    'applicable': 'REQ',
                    'label': country
                }
                if restrict not in product['features']:
                    product['features'].insert(0, restrict)
            else:
                product['dropship'] = True
            for grade in grades.keys():
                ft = {
                    'kind': 'Generic',
                    'category': 'molano.nl/grade',
                    'applicable': 'SEL',
                    'label': grade
                }
                if ft not in product['features']:
                    product['features'].append(ft)

            bulk_name = create_bulk_name(model)
            if bulk_name:
                product = bulk[bulk_name]
                product['product_name'] = bulk_name
                product['bulk'] = True
                sku = f"{model['base']}{model['memory']}"
                if country:
                    sku = f"{sku}{country}"
                if sku not in product['identifiers']:
                    product['identifiers'].append(sku)
                if storage not in product['features']:
                    product['features'].append(storage)
                mixed = {
                    'kind': 'Generic',
                    'category': 'apple.com/color',
                    'applicable': 'SEL',
                    'label': 'Mixed'
                }
                if mixed not in product['features']:
                    product['features'].append(mixed)
                color_feature = {
                    'kind': 'Generic',
                    'category': 'apple.com/color',
                    'applicable': 'SEL',
                    'label': model['color']
                }
                if color_feature not in product['features']:
                    product['features'].append(color_feature)
                if kind_feature not in product['features']:
                    product['features'].append(kind_feature)
                if model_feature not in product['features']:
                    product['features'].append(model_feature)
                if restrict and restrict not in product['features']:
                    product['features'].insert(0, restrict)
                for grade in grades.keys():
                    ft = {
                        'kind': 'Generic',
                        'category': 'molano.nl/grade',
                        'applicable': 'SEL',
                        'label': grade
                    }
                    if ft not in product['features']:
                        product['features'].append(ft)
            continue
            #if model.get('kind') == 'iPhone':
            #    batteries[model['base']] = create_battery(model)
            cap = model.get('cellular')
            k = (
                model['series'],
                model['tag'] or '',
                model['memory'],
                model.get('cellular') or ''
            )
            product = bulk[k]
            product['base'] = model['base']
            product['cellular'] = model.get('cellular')
            product['product_type'] = 'RAW_MATERIAL'
            product['colors'].add(model['color'])
            product['firmware_versions'].add(model['identifier'])
            product['generation'] = model['generation']
            product['kind'] = model['kind']
            product['model'] = model['series']
            product['namespaces'] = []
            product['search_keys'] = []
            product['storage'] = model['memory']
            product['year'] = model['year']

            h = hashlib.sha1()
            h.update('apple'.encode('utf-8'))
            for x in k:
                if isinstance(x, bool):
                    x = 't' if x else 'f'
                h.update(str.encode(x.lower(), 'utf-8'))
            product['search_keys'].append(f'sha1:{h.hexdigest()}')
            if product['kind'] == 'iPhone':
                product['name'] = f"{model['series']} {model['memory']}"

            elif product['kind'] == 'iPad':
                product['model'] = model['device']
                n = f"{model['device']}"
                if model.get('screen_size') and model.get('series') not in {'iPad', 'iPad mini'} and model.get('device') != 'iPad':
                    n = f"{n} {model['screen_size']}\""
                n = f"{n} ({model['year']}) {model['memory']}"
                if cap:
                    n = f"{n} Wi-Fi + Cellular"
                else:
                    n = f"{n} Wi-Fi"
                product['name'] = n
                product['screen_inch'] = model['screen_inch']
                product['screen_size'] = model['screen_size']


            product['restricted'] = None
            if str.endswith(model.get('tag') or '', 'jp'):
                product['restricted'] = 'JP'
            if str.endswith(model.get('tag') or '', 'cn'):
                product['restricted'] = 'CN'

        items: list[Any] = [x[1] for x in sorted(batteries.items(), key=lambda x: x[0])]
        for k, product in bulk.items():
            continue
            product = copy.deepcopy(product)
            product['name'] = f"Bulk {product['name']}"
            product['colors'] = list(sorted(product['colors']))
            product['firmware_versions'] = list(sorted(product['firmware_versions']))

        # Create variants
        for k, product in bulk.items():
            continue
            product = copy.deepcopy(product)
            product['grade'] = None
            if product.get('kind') in {'iPhone', 'iPad'}:
                for color in product.pop('colors'):
                    assert len(product['search_keys']) == 1
                    h = hashlib.sha1()
                    h.update(str.encode(product['search_keys'][0], 'utf-8'))
                    h.update(str.encode(color, 'utf-8'))
                    variant = copy.deepcopy(product)
                    variant['search_keys'] = [f'sha1:{h.hexdigest()}']
                    variant['msin'] = True
                    variant['msin_key'] = variant['search_keys'][0]
                    variant['color'] = color
                    variant['firmware_versions'] = list(sorted(variant['firmware_versions']))
                    variant['name'] = create_variant_name(product, variant, color)
                    items.append(variant)

                    for grade, name in APPLE_GRADES:
                        assert len(variant['search_keys']) == 1
                        h = hashlib.sha1()
                        h.update(str.encode(variant['search_keys'][0], 'utf-8'))
                        h.update(str.encode(grade, 'utf-8'))
                        graded = {**copy.deepcopy(variant), 'msin': variant['search_keys'][0], 'msin_key': None}
                        graded['search_keys'] = [f'sha1:{h.hexdigest()}']
                        graded['name'] = f"{graded['name']} {name}"
                        graded['grade'] = grade
                        graded['grade_name'] = name
                        graded['product_type'] = 'FINISHED_GOOD'
                        graded['namespaces'].append('catalog.buymolano.com')
                        if graded['kind'] in {'iPhone', 'iPad'}:
                            graded['search_keys'].extend([
                                #v1.generate_sku(graded),
                                v2.generate_sku(graded)
                            ])
                        graded['catalog_name'] = get_catalog_name(graded)
                        items.append(graded)

                    h = hashlib.sha1()
                    h.update(str.encode(variant['search_keys'][0], 'utf-8'))
                    h.update(str.encode('6', 'utf-8'))
                    defunct =  {**copy.deepcopy(variant), 'msin': variant['search_keys'][0], 'msin_key': None}
                    defunct['search_keys'] = []
                    defunct['name'] = f"{variant['name']} (6 COSMETIC FAIL)"
                    defunct['grade'] = '6'
                    defunct['product_type'] = 'SUBASSEMBLY'
                    defunct['search_keys'].extend([
                        f'sha1:{h.hexdigest()}',
                        v2.generate_sku(defunct)
                    ])
                    items.append(defunct)

                    h = hashlib.sha1()
                    h.update(str.encode(variant['search_keys'][0], 'utf-8'))
                    h.update(str.encode('7', 'utf-8'))
                    functional =  {**copy.deepcopy(variant), 'msin': variant['search_keys'][0], 'msin_key': None}
                    functional['search_keys'] = []
                    functional['name'] = f"{variant['name']} (7 FUNCTIONAL FAIL)"
                    functional['grade'] = '7'
                    functional['product_type'] = 'SUBASSEMBLY'
                    functional['search_keys'].extend([
                        f'sha1:{h.hexdigest()}',
                        v2.generate_sku(functional)
                    ])
                    items.append(functional)

                    h = hashlib.sha1()
                    h.update(str.encode(variant['search_keys'][0], 'utf-8'))
                    h.update(str.encode('8', 'utf-8'))
                    bat84 =  {**copy.deepcopy(variant), 'msin': variant['search_keys'][0], 'msin_key': None}
                    bat84['search_keys'] = []
                    bat84['name'] = f"{variant['name']} (8 BATTERY 80-84)"
                    bat84['grade'] = '8'
                    bat84['product_type'] = 'SUBASSEMBLY'
                    bat84['search_keys'].extend([
                        f'sha1:{h.hexdigest()}',
                        v2.generate_sku(bat84)
                    ])
                    items.append(bat84)

                    h = hashlib.sha1()
                    h.update(str.encode(variant['search_keys'][0], 'utf-8'))
                    h.update(str.encode('9', 'utf-8'))
                    bat79 =  {**copy.deepcopy(variant), 'msin': variant['search_keys'][0], 'msin_key': None}
                    bat79['search_keys'] = []
                    bat79['name'] = f"{variant['name']} (9 BATTERY BELOW 80)"
                    bat79['grade'] = '9'
                    bat79['product_type'] = 'SUBASSEMBLY'
                    bat79['search_keys'].extend([
                        f'sha1:{h.hexdigest()}',
                        v2.generate_sku(bat79)
                    ])
                    items.append(bat79)
                    variant['msin_name'] = create_msin_name(variant)

            items.append(product)
        items = [
            *parts,
            *items,
            *sorted(bulk.values(), key=lambda x: x['product_name']),
            *sorted(series.values(), key=lambda x: x['product_name'])
        ]
        print(yaml.safe_dump(items, default_flow_style=False))
        print(f"Parsed {len(items)} products", file=sys.stderr)

if __name__ == '__main__':
    asyncio.run(main())