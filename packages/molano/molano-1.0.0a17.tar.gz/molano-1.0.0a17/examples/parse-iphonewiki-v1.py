# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

import yaml
from headless.core import httpx

from molano.lib.sku import v1


async def main():
    fn: str = v1.__file__.replace('.py', '.yaml')
    async with httpx.Client(base_url="") as client:
        with open(fn, 'w') as f:
            f.write(
                '---\n' +
                yaml.safe_dump( # type: ignore
                    [
                        *[row async for row in v1.parse_ipads(client)],
                        *[row async for row in v1.parse_iphones(client)],
                    ],
                    indent=2,
                    default_flow_style=False
                )
            )


if __name__ == '__main__':
    asyncio.run(main())