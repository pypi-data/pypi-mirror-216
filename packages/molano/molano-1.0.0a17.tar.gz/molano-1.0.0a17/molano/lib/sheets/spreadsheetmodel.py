# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Sequence
from typing import TypeVar

import pydantic


T = TypeVar('T', bound='SpreadsheetModel')


class SpreadsheetModel(pydantic.BaseModel):

    @classmethod
    def parse_row(
        cls: type[T],
        row: Sequence[Any]
    ) -> T:
        values: dict[str, Any] = {}
        for i, k in enumerate(cls.__fields__):
            try:
                values[k] = row[i]
            except IndexError:
                values[k] = None
        return cls.parse_obj(values)

    def as_row(self) -> dict[str, Any]:
        values = tuple(getattr(self, k) for k in self.__fields__.keys())
        return {'values': [
            {'userEnteredValue': {'stringValue': str(x or '')}}
            for x in values
        ]}