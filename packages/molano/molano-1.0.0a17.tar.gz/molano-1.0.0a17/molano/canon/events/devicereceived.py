# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime

import aorta
from canonical import EmailAddress

from ..devicesource import DeviceSource
from ..documentreference import DocumentReference
from ..imei import IMEI
from ..trackedmobiledevicereference import TrackedMobileDeviceReference


class DeviceReceived(aorta.Event):
    device: TrackedMobileDeviceReference
    timestamp: datetime
    document: DocumentReference
    handler: EmailAddress
    imei: list[IMEI]
    product_id: int | None = None
    sku: str | None = None
    source: DeviceSource