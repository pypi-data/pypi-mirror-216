 # Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import canonical


NAME_MAP: dict[str, tuple[str, str]] = {
    'apple'     : ('1.3.6.1.4.1.63', 'Apple'),
    'samsung'   : ('1.3.6.1.4.1.236', 'Samsung'),
    'oppo'      : ('1.3.3.1.4.1.55500', 'Oppo')
}
OID_MAP: dict[str, str] = ({x[0]: x[1] for x in NAME_MAP.values()})


class PrivateEnterpriseNumber(canonical.StringType):
    __module__: str = 'molano.canon'

    @classmethod
    def parse_name(cls, value: str) -> 'PrivateEnterpriseNumber':
        value = str.lower(value)
        if value not in NAME_MAP:
            raise LookupError(f"Unknown manufacturer: {value[:64]}")
        return cls(NAME_MAP[value][0])

    @classmethod
    def validate(cls, v: str) -> str:
        if v in NAME_MAP:
            v = NAME_MAP[v][0]
        return cls(v)
    
    @property
    def name(self) -> str:
        return OID_MAP[str(self)]