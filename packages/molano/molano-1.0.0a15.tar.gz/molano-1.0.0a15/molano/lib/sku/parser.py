# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Any

from .const import APPLE_MODELS
from .v2 import APPLE_COLORS


_color_pattern: re.Pattern[str] = re.compile(
    '(.*?)(' + str.join('|', [
        x for x in sorted(APPLE_COLORS.keys(), key=lambda x: -len(x))
    ]) + ')',
    re.IGNORECASE
)


_model_pattern: re.Pattern[str] = re.compile(
    '(.*?)(' + str.join('|', [
        x for x in sorted(APPLE_MODELS.keys(), key=lambda x: -len(x))
    ]) + ')',
    re.IGNORECASE
)


_storage_pattern: re.Pattern[str] = re.compile(
    r'(.*?)(([0-9]+(\s+)?)(GB|TB))',
    re.IGNORECASE
)


def parse_color(value: str) -> tuple[str, str] | tuple[None, None]:
    m = _color_pattern.match(value)
    if not m:
        return None, None
    color = m.group(2)
    return APPLE_COLORS[str.lower(color)], color


def parse_model(value: str) -> str | None:
    if 'iphone' in str.lower(value):
        m = _model_pattern.match(value)
        if not m:
            return None
        return m.group(2)
    else:
        return None


def parse_storage(value: str) -> str | None:
    m = _storage_pattern.match(value)
    if not m:
        return None
    storage = m.group(2)
    return str.upper(re.sub(r'\s+', '', storage))


def parse(value: str) -> dict[str, Any]:
    params: dict[str, Any] = {}
    params['color_code'], params['color'] = parse_color(value)
    params['model'] = model = parse_model(value)
    params['storage'] = parse_storage(value)
    if model:
        params.update(APPLE_MODELS[str.lower(model)])
    return params