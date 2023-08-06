# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import copy

from headless.core import httpx

from molano.lib.sku import v1
from molano.lib.sku import v2
from molano.lib.sku import generate
from molano.lib.sheets import Spreadsheet
from molano.lib.sheets import SpreadsheetModel


DEFAULT_GRADINGS: dict[str, str] = {
    'A+'    : '0',
    'A'     : '1',
    'B+'    : '2',
    'B'     : '3',
    'C+'    : '4',
    'C'     : '5',
    'D'     : '6'
}


class PhoneInfo(SpreadsheetModel):
    name: str
    model: str
    skuv1: str
    skuv2: str
    kind: str
    grading_level: str = 'ABC'
    grade: str
    body_grade: str = ""
    screen_grade: str = ""
    device: str
    memory: str
    year: str
    screen_size: str = ""
    parts_category: str = ""
    accessoires_category: str = ""
    vat: str = 'VAT'
    color: str


async def main():
    sheet = Spreadsheet(
        model=PhoneInfo,
        id='12fZ4JCiPyBwerZULjXZB40ecgAaHDy-HE_y19nrJLaM',
        sheet_id=1571318229,
        range='Apple Products'
    )
    sheet.clear()
    rows: list[PhoneInfo] = []
    async with httpx.Client(base_url="") as client:
        async for params in generate(client, using=v1, gradings=DEFAULT_GRADINGS, with_ungraded=False):
            if params.get('tag') in {'apple:model:exclusive:cn', 'apple:model:exclusive:jp'}:
                continue
            row = PhoneInfo.parse_obj({
                **params,
                'skuv1': v1.generate_sku(copy.deepcopy(params)),
                'skuv2': v2.generate_sku(copy.deepcopy(params))
            })
            assert not row.skuv1.endswith('+')
            assert not row.skuv2.endswith('+')
            if int(row.year) < 2015:
                continue
            rows.append(row)
    sheet.extend(rows)

if __name__ == '__main__':
    asyncio.run(main())