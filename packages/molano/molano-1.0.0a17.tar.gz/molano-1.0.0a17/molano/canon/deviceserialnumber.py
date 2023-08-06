# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hashlib

import pydantic

from .privateenterprisenumber import PrivateEnterpriseNumber


class DeviceSerialNumber(pydantic.BaseModel):
    manufacturer: PrivateEnterpriseNumber
    model: str
    serial: str

    def sha256(self) -> str:
        h = hashlib.sha3_256()
        h.update(str.encode(type(self).__name__))
        h.update(str.encode(self.manufacturer.sha256(), encoding='ascii'))
        h.update(str.encode(self.model, encoding='utf-8'))
        h.update(str.encode(self.serial, encoding='utf-8'))
        return h.hexdigest()