# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import re
from types import ModuleType
from typing import Any
from typing import AsyncIterator
from typing import Callable

from headless.types import IClient

from .const import DEFAULT_GRADINGS
from .const import APPLE_MODELS
from . import v1
from . import v2
from . import v3


async def load_models(
    client: IClient[Any, Any],
    using: ModuleType
) -> AsyncIterator[dict[str, int | str]]:
    async for params in using.parse_iphones(client):
        yield params

    async for params in using.parse_ipads(client):
        # Create a variant for cellular, wifi
        for cap in {'C', 'W'}:
            params: dict[str, Any] = {
                **copy.deepcopy(params),
                'cellular': cap == 'C',
                'sku': params['sku'] + cap
            }
            yield params


def generate_name(params: dict[str, Any]) -> str:
    kind = str.lower(params.get('kind') or '')

    def generate_iphone_name(attrs: dict[str, Any]):
        name = '{model} {memory} {color}'.format(**attrs)
        return name


    def generate_ipad_name(attrs: dict[str, Any]):
        name = '{device} ({year})'.format(**attrs)
        if attrs.get('screen_size'):
            name = f'{name} {attrs["screen_size"]}"'
        name = f'{name} {"WiFi + Cellular" if attrs["cellular"] else "WiFi"}'
        name = '{name} {memory} {color}'.format(name=name, **params)
        return name

    name = None
    match kind:
        case "ipad":
            name = generate_ipad_name(params)
        case "iphone":
            name = generate_iphone_name(params)
        case _:
            raise NotImplementedError

    assert name is not None
    params.setdefault('grade_name', '')
    return str.strip('{name} {grade_name}'.format(name=name, **params))


async def generate(
    client: IClient[Any, Any],
    using: ModuleType,
    gradings: dict[str, Any] = DEFAULT_GRADINGS,
    generate_sku: Callable[[str, dict[str, Any]], str] | None = None,
    with_ungraded: bool = True
) -> AsyncIterator[dict[str, int | str]]:
    async for product in load_models(client, using=using):
        if gradings:
            for grade, sku in gradings.items():
                params = {
                    **copy.deepcopy(product),
                    'grading_level': 'ABC',
                    'grade': sku,
                    'grade_name': grade,
                    'sku': str(product['sku']) + str(sku)
                }
                yield {**params, 'name': generate_name(params)}

        params = copy.deepcopy(product)
        if with_ungraded:
            yield {**params, 'name': generate_name(params)}




model_pattern: re.Pattern[str] = re.compile(
    '(.*)(' + str.join('|', [
        x for x in reversed(APPLE_MODELS.keys())
    ]) + ')+'
)


def get_model_info(value: str) -> dict[str, Any]:
    m = model_pattern.match(value)
    if not m:
        raise ValueError("Unable to parse model")
    return APPLE_MODELS[m.group(2)]