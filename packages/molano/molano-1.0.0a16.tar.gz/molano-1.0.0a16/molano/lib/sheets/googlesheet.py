# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generic
from typing import TypeVar

from googleapiclient import discovery

from .spreadsheetmodel import SpreadsheetModel


T = TypeVar('T', bound=SpreadsheetModel)


class Spreadsheet(Generic[T]):
    __module__: str = 'ea.ui'
    id: str
    model: type[T]
    service: Any = discovery.build('sheets', 'v4') # type: ignore
    sheet_id: int

    def __init__(
        self,
        model: type[T],
        id: str,
        sheet_id: int,
        range: str = 'A:Z'
    ):
        self.client = self.service.spreadsheets()
        self.id = id
        self.model = model
        self.range = range
        self.sheet_id = sheet_id
        self.values = []

    def load(self) -> None:
        """Load the current values."""
        request = self.client.values().get(
            spreadsheetId=self.id,
            range=self.range
        )
        response = request.execute()
        self.values = [
            self.model.parse_row(x)
            if any(x) else None
            for x in ((response.get('values') or [])[1:])
        ]

    def append(self, row: T) -> None:
        return self.extend([row])

    def extend(self, rows: list[T]) -> None:
        request = self.client.batchUpdate(
            spreadsheetId=self.id,
            body={
                'requests': [{
                    'appendCells': {
                        'sheetId': self.sheet_id,
                        'fields': '*',
                        'rows': [x.as_row() for x in rows]
                    }
                }]
            }
        )
        request.execute()
        self.write()

    def clear(self) -> None:
        """Clears all rows in the spreadsheet."""
        self.client.batchUpdate(
            spreadsheetId=self.id,
            body={
                'requests': [
                    {
                        'updateSheetProperties': {
                            'properties': {
                                'sheetId': self.sheet_id,
                                'gridProperties': {
                                    'frozenRowCount': 0
                                }
                            },
                            'fields': 'gridProperties.frozenRowCount'
                        }
                    }
                ]
            }
        ).execute()
        if len(self.values) > -1:
            self.client.batchUpdate(
                spreadsheetId=self.id,
                body={
                    'requests': {
                        'deleteDimension': {
                            'range': {
                                'sheetId': self.sheet_id,
                                'dimension': "ROWS",
                                'startIndex': 1
                            }
                        }
                    }
                }
            ).execute()

    def write(self) -> None:
        self.client.batchUpdate(
            spreadsheetId=self.id,
            body={
                'requests': [
                    {
                    "updateCells": 
                    {
                        "rows": 
                        [
                        {
                            "values": 
                            [
                            {
                                "userEnteredFormat": 
                                {
                                "verticalAlignment": "TOP"
                                }
                            }
                            ]
                        }
                        ],
                        "range": 
                        {
                            "sheetId": self.sheet_id,
                            "startRowIndex": 1,
                            "startColumnIndex": 0,
                        },
                        "fields": "userEnteredFormat"
                    }
                    },
                    {
                        'updateSheetProperties': {
                            'properties': {
                                'sheetId': self.sheet_id,
                                'gridProperties': {
                                    'frozenRowCount': 1
                                }
                            },
                            'fields': 'gridProperties.frozenRowCount'
                        }
                    },
                    {
                        'repeatCell': {
                            'fields': "userEnteredFormat(textFormat)",
                            'range': {
                                'startRowIndex': 1,
                                'sheetId': self.sheet_id
                            },
                            'cell': {
                                'userEnteredFormat': {
                                    'textFormat': {
                                        'fontSize': 10,
                                        'foregroundColor': {
                                            'red': 0,
                                            'green': 0,
                                            'blue': 0
                                        }
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        ).execute()