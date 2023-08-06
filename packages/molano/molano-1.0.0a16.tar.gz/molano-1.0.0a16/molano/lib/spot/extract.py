# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# type: ignore
import sys
from typing import Any

from headless.types import IClient


DEFAULT_HEADERS: dict[str, str] = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}


report = lambda *x: print(*x, file=sys.stderr)


DESCRIPTION1: set[str] = {
    '661-19620',
    '661-25890',
    '661-25683',
    '923-07174',
    '923-07176',
}


def create_part(model: str, params: dict[str, Any]) -> dict[str, Any]:
    c_attrs: dict[str, Any] = {x['id_countries']: x for x in params['country_specific_attributes']}
    language_attrs: dict[str, Any] = {x['id_languages']: x for x in params['language_specific_attributes']}
    c = c_attrs['BE']
    l = language_attrs['en']
    if model == 'iPhone SE (3rd generation)':
        model = 'iPhone SE 2022'
    name = l['description2'] or l['description1']
    if params['partnumber'] in DESCRIPTION1:
        name = l['description1']
    if str.lower(name) in {str.lower("Display & Screw Kit"), str.lower("Battery & Screw Kit"), str.lower("Camera"), str.lower("Bottom Speaker"), str.lower("Taptic Engine")}:
        name = f'{name} ({model})'
    return {
        'kind': 'Part',
        'name': str.strip(name),
        'namespaces': ['parts.molano.nl'],
        'product_type': 'RAW_MATERIAL',
        'suppliers': ['selfservicerepair.eu'],
        'cost_estimation': str(c['price']),
        'annotations': {
            'selfservicerepair.eu/partnumber': params['partnumber'],
            'selfservicerepair.eu/credit-amount': str(c['creditamount'])
        },
        'search_keys': [
            f"selfservicerepair.eu/partnumber:{params['partnumber']}"
        ]
    }


async def parse_category(
    client: IClient[Any, Any],
    parts: dict[str, Any],
    device_type_id: int,
    model_id: int,
    model_name: str,
    repair_type_id: int,
    repair_type_code: str,
    url: str = "https://selfservicerepair.eu/api/Spares/Search"
):
    response = await client.get(
        url=url,
        headers=DEFAULT_HEADERS,
        params={
            'deviceTypeId': device_type_id,
            'deviceModelId': model_id,
            'repairTypeId': repair_type_id,
            'tools': False,
            'repairTypeCode': repair_type_code
        }
    )
    for dto in await response.json():
        # Ignore bundles.
        part_number: str = dto['partnumber']
        if part_number.startswith('BD') or part_number in parts or not part_number[0].isdigit():
            continue
        parts[part_number] = create_part(model_name, dto)


async def parse_model(
    client: IClient[Any, Any],
    parts: dict[str, Any],
    device_type_id: int,
    model_id: int,
    model_name: str,
    url: str = "https://selfservicerepair.eu/api/RepairTypes/GetByModel"
):
    response = await client.get(
        url=url,
        headers=DEFAULT_HEADERS,
        params={
            'deviceTypeId': device_type_id,
            'modelId': model_id
        }
    )
    for obj in await response.json():
        report(f"- Scraping category {obj['repairtype']}")
        await parse_category(client, parts, device_type_id, model_id, model_name, obj['id'], obj['repairtypecode'])


async def parse_selfservicerepair(client: IClient[Any, Any]) -> list[Any]:
    url: str = "https://selfservicerepair.eu/api/DeviceModels/GetByDeviceType?deviceTypeId=1&modelId=1"
    parts: dict[str, Any] = {}
    response = await client.get(url=url, headers=DEFAULT_HEADERS)
    for obj in await response.json():
        report(f"Scraping {obj['model']}")
        await parse_model(client, parts, obj['id_devicetypes'], obj['id'], obj['model'])
    return list([x[1] for x in sorted(parts.items(), key=lambda x: x[0])])