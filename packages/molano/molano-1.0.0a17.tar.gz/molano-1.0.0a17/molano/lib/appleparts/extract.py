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
import hashlib
import re
import sys
from typing import Any

import lxml.html
import lxml.etree
from headless.types import IClient

from ..sku.const import APPLE_MODELS


CATEGORIES: list[str] = [
    (
        "https://www.appleparts.nl/iPhone-onderdelen",
        re.compile('.*iphone.*onderdelen$', re.IGNORECASE)
    ),
    #"https://www.appleparts.nl/iPad/onderdelen"
]

IGNORE: set[str] = {
    "https://www.appleparts.nl/iPhone-onderdelen"
}

DEFAULT_HEADERS: dict[str, str] = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}


APPLE_COLORS: dict[str, str] = {
    'Blauw'                 : 'Blue',
    'Blue'                  : None,
    'Dieppaars'             : 'Deep Purple',
    'Grafiet'               : 'Graphite',
    'Green'                 : None,
    'Space Grey'            : None,
    'Geel'                  : 'Yellow',
    'Gold'                  : None,
    'goud'                  : 'Gold',
    'Goud'                  : 'Gold',
    'Groen'                 : 'Green',
    'Koraal'                : 'Coral',
    'Red'                   : None,
    'Rood'                  : 'Red',
    'rood'                  : 'Red',
    'Roze'                  : 'Pink',
    'Middernacht (Zwart)'   : 'Midnight',
    'Middernacht zwart'     : 'Midnight',
    'Middernacht (zwart)'   : 'Midnight',
    'Midnight'              : 'Midnight',
    'Midnight Green'        : None,
    'Oceaan blauw'          : 'Pacific Blue',
    'Pink'                  : None,
    'paars'                 : 'Purple',
    'Paars'                 : 'Purple',
    'Rosé Gold'             : 'Rose Gold',
    'Rose Gold'             : 'Rose Gold',
    'Sierra Blauw'          : 'Sierra Blue',
    'Space grey'            : 'Space Grey',
    'Spacezwart'            : 'Space Black',
    'Starlight'             : None,
    'Sterrenlicht (Zilver)' : 'Starlight',
    'Sterrenlicht'          : 'Starlight',
    'Wit'                   : 'White',
    'wit'                   : 'White',
    'White'                 : None,
    'Yellow'                : None,
    'zwart'                 : 'Black',
    'Zwart'                 : 'Black',
    'Zilver'                : 'Silver',
    'Zilver Wit'            : 'Silver',
    'zilver wit'            : 'Silver',
    'zilver Wit'            : 'Silver',
    '(Product) Red'         : 'PRODUCT(RED)'
}

report = lambda *x: print(*x, file=sys.stderr)


def parse_urls(root, pattern: re.Pattern, ignore: set[str], xpath: str ='.//a') -> list[str]:
    seen: set[str] = set()
    for element in root.findall(xpath):
        url = str.strip(element.attrib.get('href') or '')
        if not url or not pattern.match(url) or url in seen or url in ignore:
            continue
        seen.add(url)
    return list(sorted(seen))


async def parse_backcover(
    client: IClient[Any, Any],
    parts: dict[str, Any],
    url: str,
):
    pattern: re.Pattern[str] = re.compile(
        '.*?Achterkant back cover glas met logo voor Apple (?P<model>iPhone\s[^s]+?)(?:\s(Max|2020 2e generatie|2020|Mini|Pro Max|Pro|Plus))?\s(?P<color>.*)$',
    )
    response = await client.get(url=url)
    root = lxml.html.fromstring(response.content)

    elements = root.xpath('.//span[@class="content-page-title product-title"]')
    if not elements:
        raise NotImplementedError(url)
    title = elements[0]
    if not title.text:
        raise NotImplementedError(f"Title did not contain text at {url}")
    m = pattern.match(str.strip(title.text))
    if not m:
        raise NotImplementedError(f"Unable to parse title: {repr(title.text)}")
    model, variant, color = m.groups()
    color = APPLE_COLORS[color] or color
    report(f"- Part is for model {model} {variant}")
    if variant == '2020 2e generatie':
        variant = '2020'
    if variant == 'Mini':
        variant = 'mini'
    try:
        name = f"Apple {model} {'' if not variant else (variant) + ' '}back cover ({color}, OEM)"
    except KeyError:
        report(f"Unable to parse color '{color}' from {title.text}")
        raise SystemExit
    report(f"- Discovered {name}")

    # Parse article number
    elements = root.xpath('.//div[div[p[contains(text(), "Artikelnummer")]]]')
    if not elements or len(elements[0]) != 2:
        raise NotImplementedError(f"Unable to find article number at {url}")
    parent = elements[0]
    p = parent[1][0]
    m = re.match('.*(A[0-9]+).*', p.text_content(), flags=re.DOTALL)
    if not m:
        raise NotImplementedError(f"Unable to parse article number at {url}", p.text_content())
    partnumber = m.group(1)
    report(f"- Discovered part {partnumber}")

    # Parse price
    elements = root.xpath('.//span[@id="Price1_exc"]')
    if not elements:
        raise NotImplementedError(f"Unable to find price element at {url}")
    span = elements[0]
    price = str.replace(re.sub('[^\d,.]', '', span.text), ',', '.')
    report(f"- Discovered price {price}")

    # This vendor is the MSIN for back covers
    if variant == '2020':
        variant = '(2nd generation)'
    attrs = APPLE_MODELS[f'{model} {variant}' if variant else model]
    urn = f"urn:molano:products:apple:iphone:{str.lower(attrs['base'])}:backcover"
    h = hashlib.sha1()
    h.update(str.encode(urn, 'utf-8'))
    h.update(str.encode('oem', 'utf-8'))
    h.update(str.encode(color, 'utf-8'))
    search_key = f'sha1:{h.hexdigest()}'

    # Add to parts
    parts[partnumber] = dto = {
        'color': color,
        'kind': 'Part',
        'name': name,
        'namespaces': ['parts.molano.nl'],
        'product_type': 'RAW_MATERIAL',
        'suppliers': ['appleparts.nl'],
        'cost_estimation': price,
        'msin_base': search_key,
        'msin_name': name,
        'annotations': {
            'appleparts.nl/partnumber': partnumber,
            'color': color
        },
        'search_keys': [
            search_key,
            f"appleparts.nl/partnumber:{partnumber}"
        ]
    }


async def parse_product_list(
    client: IClient[Any, Any],
    parts: dict[str, Any],
    url: str,
):
    response = await client.get(url=url)
    root = lxml.html.fromstring(response.content)
    xpath = './/div[@class="c-product-block"]//a'
    futures = []
    for url in parse_urls(root, re.compile('.*Achterkant-back-cover-glas.*', re.IGNORECASE), IGNORE, xpath=xpath):
        futures.append(parse_backcover(client, parts, url))
    await asyncio.gather(*futures)


async def parse_category(
    client: IClient[Any, Any],
    parts: dict[str, Any],
    url: str,
    pattern: re.Pattern[str]
):
    response = await client.get(url=url)
    root = lxml.html.fromstring(response.content)
    futures = []
    for url in parse_urls(root, pattern, IGNORE):
        report(f"Scraping category {url}")
        futures.append(parse_product_list(client, parts, url))
    await asyncio.gather(*futures)


async def parse(client: IClient[Any, Any]) -> list[Any]:
    parts: dict[str, Any] = {}
    futures = []
    for category_url, pattern in CATEGORIES:
        futures.append(parse_category(client, parts, category_url, pattern))
    await asyncio.gather(*futures)
    return [x[1] for x in sorted(parts.items(), key=lambda x: x[0])]