# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .appleudid import AppleUDID
from .decimalmeid import DecimalMEID
from .deviceserialnumber import DeviceSerialNumber
from .documentreference import DocumentReference
from .imei import IMEI
from .meid import MEID
from .privateenterprisenumber import PrivateEnterpriseNumber
from .ordernumber import OrderNumber
from .purchaseordernumber import PurchaseOrderNumber
from .receiptnumber import ReceiptNumber
from .trackedmobiledevicereference import TrackedMobileDeviceReference


__all__: list[str] = [
    'AppleUDID',
    'DecimalMEID',
    'DeviceSerialNumber',
    'DocumentReference',
    'IMEI',
    'MEID',
    'PrivateEnterpriseNumber',
    'OrderNumber',
    'PurchaseOrderNumber',
    'ReceiptNumber',
    'TrackedMobileDeviceReference',
]