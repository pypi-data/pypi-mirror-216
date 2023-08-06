# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Callable

import base36

CIP_LENGTH: int = 78

def t(l: int) -> str:
    return f'{{:0{l}b}}'


def fb(l: int, v: int) -> str:
    return t(l).format(v)


BRANDS: dict[str, str] = {
    'apple.com'     : fb(14, 0b00000000000001),
    'samsung.com'   : fb(14, 0b00000000000010)
}

VERSIONS: dict[str, str] = {
    'v1'    : fb(2, 0b10),
    'v2+'   : fb(2, 0b11),
}

# Apple
APPLE_PRODUCT_LINES: dict[str, str] = {
    'macbook:air'   : fb(7, 0b0000001),
    'macbook:pro'   : fb(7, 0b0000010),
    'imac'          : fb(7, 0b0000011),
    'mac:mini'      : fb(7, 0b0000100),
    'mac:studio'    : fb(7, 0b0000101),
    'mac:pro'       : fb(7, 0b0000110),
    'iphone'        : fb(7, 0b0000111),
    'ipad'          : fb(7, 0b0001000),
    'watch'         : fb(7, 0b0001001),
    'airpods'       : fb(7, 0b0001010),
}

APPLE_RESTRICTIONS: dict[str | None, str] = {
    None    : fb(4, 0b0000),
    'cn'    : fb(4, 0b0001),
    'jp'    : fb(4, 0b0010),
    'eu'    : fb(4, 0b0100),
    'us'    : fb(4, 0b1000),
}


def encode_iphone(*, model: str, **kwargs: str):
    raise NotImplementedError


def encode_apple(
    *,
    product_line: str,
    restriction: str | None = None,
    **kwargs: str
) -> str:
    cip: str = APPLE_PRODUCT_LINES[product_line]
    cip += APPLE_RESTRICTIONS[restriction]
    return cip
    if product_line == 'iphone':
        cip += encode_iphone(**kwargs)
    else:
        raise NotImplementedError
    raise NotImplementedError


def encode(
    brand: str,
    *,
    version: str ='v1',
    **kwargs: str
) -> str:
    brand = BRANDS[brand]
    version = VERSIONS[version]
    cip = version + brand
    if brand == fb(14, 0b00000000000001):
        cip = encode_apple(**kwargs)
    else:
        raise NotImplementedError
    cip = str.ljust(cip, 80, '0')
    assert len(cip) == 80
    return str.upper(base36.dumps(int(cip, base=2))) # type: ignore