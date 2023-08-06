# Copyright (C) 2023 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


APPLE_MODELS: dict[str, dict[str, int | str]] = {
    'iPad'                                  : {'device': 'iPad', 'year': 2010, 'generation': 1, 'base': 'IPA', 'msin': 'ipad:1:fix'},
    'iPad 2'                                : {'device': 'iPad', 'year': 2011, 'generation': 2, 'base': 'IPA', 'msin': 'ipad:2:fix'},
    'iPad (3rd generation)'                 : {'device': 'iPad', 'year': 2012, 'generation': 3, 'base': 'IPA', 'msin': 'ipad:3:fix'},
    'iPad (4th generation)'                 : {'device': 'iPad', 'year': 2012, 'generation': 4, 'base': 'IPA', 'msin': 'ipad:4:fix'},
    'iPad (5th generation)'                 : {'device': 'iPad', 'year': 2017, 'generation': 5, 'base': 'IPA', 'msin': 'ipad:5:fix'},
    'iPad (6th generation)'                 : {'device': 'iPad', 'year': 2018, 'generation': 6, 'base': 'IPA', 'msin': 'ipad:6:fix'},
    'iPad (7th generation)'                 : {'device': 'iPad', 'year': 2019, 'generation': 7, 'base': 'IPA', 'msin': 'ipad:7:fix'},
    'iPad (8th generation)'                 : {'device': 'iPad', 'year': 2020, 'generation': 8, 'base': 'IPA', 'msin': 'ipad:8:fix'},
    'iPad (9th generation)'                 : {'device': 'iPad', 'year': 2021, 'generation': 9, 'base': 'IPA', 'msin': 'ipad:9:fix'},
    'iPad (10th generation)'                : {'device': 'iPad', 'year': 2022, 'generation': 10, 'base': 'IPA', 'msin': 'ipad:10:fix'},
    'iPad Air'                              : {'device': 'iPad Air', 'year': 2013, 'generation': 1, 'base': 'IPAA', 'msin': 'air:1:fix'},
    'iPad Air 2'                            : {'device': 'iPad Air', 'year': 2014, 'generation': 2, 'base': 'IPAA', 'msin': 'air:2:fix'},
    'iPad Air (3rd generation)'             : {'device': 'iPad Air', 'year': 2019, 'generation': 3, 'base': 'IPAA', 'msin': 'air:3:fix'},
    'iPad Air (4th generation)'             : {'device': 'iPad Air', 'year': 2020, 'generation': 4, 'base': 'IPAA', 'msin': 'air:4:fix'},
    'iPad Air (5th generation)'             : {'device': 'iPad Air', 'year': 2022, 'generation': 5, 'base': 'IPAA', 'msin': 'air:5:fix'},
    'iPad Pro (9.7-inch)'                   : {'device': 'iPad Pro', 'year': 2016, 'screen_size': '9.7', 'generation': 1, 'base': 'IPAP', 'msin': 'pro:1:9.7'},
    'iPad Pro (10.5-inch)'                  : {'device': 'iPad Pro', 'year': 2017, 'screen_size': '10.5', 'generation': 1, 'base': 'IPAP', 'msin': 'pro:1:10.5'},
    'iPad Pro (11-inch)'                    : {'device': 'iPad Pro', 'year': 2018, 'screen_size': '11', 'generation': 1, 'base': 'IPAP', 'msin': 'pro:1:11'},
    'iPad Pro (11-inch) (2nd generation)'   : {'device': 'iPad Pro', 'year': 2020, 'screen_size': '11', 'generation': 2, 'base': 'IPAP', 'msin': 'pro:2: 11'},
    'iPad Pro (11-inch) (3rd generation)'   : {'device': 'iPad Pro', 'year': 2021, 'screen_size': '11', 'generation': 3, 'base': 'IPAP', 'msin': 'pro:3:11'},
    'iPad Pro (12.9-inch)'                  : {'device': 'iPad Pro', 'year': 2015, 'screen_size': '12.9', 'generation': 1, 'base': 'IPAP', 'msin': 'pro:1:12.9'},
    'iPad Pro (12.9-inch) (2nd generation)' : {'device': 'iPad Pro', 'year': 2017, 'screen_size': '12.9', 'generation': 2, 'base': 'IPAP', 'msin': 'pro:2:12.9'},
    'iPad Pro (12.9-inch) (3rd generation)' : {'device': 'iPad Pro', 'year': 2018, 'screen_size': '12.9', 'generation': 3, 'base': 'IPAP', 'msin': 'pro:3:12.9'},
    'iPad Pro (12.9-inch) (4th generation)' : {'device': 'iPad Pro', 'year': 2020, 'screen_size': '12.9', 'generation': 4, 'base': 'IPAP', 'msin': 'pro:4:12.9'},
    'iPad Pro (12.9-inch) (5th generation)' : {'device': 'iPad Pro', 'year': 2021, 'screen_size': '12.9', 'generation': 5, 'base': 'IPAP', 'msin': 'pro:5:12.9'},
    'iPad mini'                             : {'device': 'iPad mini', 'year': 2012, 'generation': 1, 'base': 'IPAM', 'msin': 'mini:1:fix'},
    'iPad mini 2'                           : {'device': 'iPad mini', 'year': 2013, 'generation': 2, 'base': 'IPAM', 'msin': 'mini:2:fix'},
    'iPad mini 3'                           : {'device': 'iPad mini', 'year': 2014, 'generation': 3, 'base': 'IPAM', 'msin': 'mini:3:fix'},
    'iPad mini 4'                           : {'device': 'iPad mini', 'year': 2015, 'generation': 4, 'base': 'IPAM', 'msin': 'mini:4:fix'},
    'iPad mini (5th generation)'            : {'device': 'iPad mini', 'year': 2019, 'generation': 5, 'base': 'IPAM', 'msin': 'mini:5:fix'},
    'iPad mini (6th generation)'            : {'device': 'iPad mini', 'year': 2021, 'generation': 6, 'base': 'IPAM', 'msin': 'mini:6:fix'},
    'iPhone'                                : {'year': 2007, 'base': 'IPH1'},
    'iPhone 3G'                             : {'year': 2008, 'base': 'IPH3G'},
    'iPhone 3GS'                            : {'year': 2008, 'base': 'IPH3GS'},
    'iPhone 4'                              : {'year': 2010, 'base': 'IPH4'},
    'iPhone 4S'                             : {'year': 2010, 'base': 'IPH4S'},
    'iPhone 5'                              : {'year': 2012, 'base': 'IPH5'},
    'iPhone 5c'                             : {'year': 2012, 'base': 'IPH5C'},
    'iPhone 5s'                             : {'year': 2012, 'base': 'IPH5S'},
    'iPhone 6'                              : {'year': 2014, 'base': 'IPH6'},
    'iPhone 6 Plus'                         : {'year': 2014, 'base': 'IPH6P'},
    'iPhone 6s'                             : {'year': 2014, 'base': 'IPH6S'},
    'iPhone 6s Plus'                        : {'year': 2014, 'base': 'IPH6SP'},
    'iPhone SE (1st generation)'            : {'year': 2016, 'base': 'IPHSE1', 'generation': 1},
    'iPhone SE (2nd generation)'            : {'year': 2020, 'base': 'IPHSE2', 'generation': 2},
    'iPhone SE (3rd generation)'            : {'year': 2022, 'base': 'IPHSE3', 'generation': 3},
    'iPhone 7'                              : {'year': 2016, 'base': 'IPH7'},
    'iPhone 7 Plus'                         : {'year': 2016, 'base': 'IPH7P'},
    'iPhone 8'                              : {'year': 2017, 'base': 'IPH8'},
    'iPhone 8 Plus'                         : {'year': 2017, 'base': 'IPH8P'},
    'iPhone X'                              : {'year': 2018, 'base': 'IPHX'},
    'iPhone XR'                             : {'year': 2018, 'base': 'IPHXR'},
    'iPhone XS'                             : {'year': 2018, 'base': 'IPHXS'},
    'iPhone XS Max'                         : {'year': 2018, 'base': 'IPHXSM'},
    'iPhone 11'                             : {'year': 2019, 'base': 'IPH11'},
    'iPhone 11 Pro'                         : {'year': 2019, 'base': 'IPH11P'},
    'iPhone 11 Pro Max'                     : {'year': 2019, 'base': 'IPH11PM'},
    'iPhone 12 mini'                        : {'year': 2020, 'base': 'IPH12M'},
    'iPhone 12'                             : {'year': 2020, 'base': 'IPH12'},
    'iPhone 12 Pro'                         : {'year': 2020, 'base': 'IPH12P'},
    'iPhone 12 Pro Max'                     : {'year': 2020, 'base': 'IPH12PM'},
    'iPhone 13 mini'                        : {'year': 2021, 'base': 'IPH13M'},
    'iPhone 13'                             : {'year': 2021, 'base': 'IPH13'},
    'iPhone 13 Pro'                         : {'year': 2021, 'base': 'IPH13P'},
    'iPhone 13 Pro Max'                     : {'year': 2021, 'base': 'IPH13PM'},
    'iPhone 14'                             : {'year': 2022, 'base': 'IPH14'},
    'iPhone 14 Pro'                         : {'year': 2022, 'base': 'IPH14P'},
    'iPhone 14 Plus'                        : {'year': 2022, 'base': 'IPH14PL'},
    'iPhone 14 Pro Max'                     : {'year': 2022, 'base': 'IPH14PM'},
}
APPLE_MODELS.update({
    'iPhone SE 2016': APPLE_MODELS['iPhone SE (1st generation)'],
    'iPhone SE 2020': APPLE_MODELS['iPhone SE (2nd generation)'],
    'iPhone SE 2022': APPLE_MODELS['iPhone SE (3rd generation)'],
})
APPLE_MODELS.update({k.lower(): v for k, v in APPLE_MODELS.items()})


APPLE_IDENTIFIERS: dict[str, dict[str, int | str | bool | None]] = {
    'iPad1,1': {'generation': 1, 'cellular': None},
    'iPad1,2': {'generation': 1, 'cellular': '3G'},
    'iPad2,1': {'generation': 2, 'cellular': None},
    'iPad2,2': {'generation': 2, 'cellular': 'GSM'},
    'iPad2,3': {'generation': 2, 'cellular': 'CDMA'},
    'iPad2,4': {
        'generation': 2,
        'cellular': None
    },
    'iPad3,1': {
        'generation': 3,
        'cellular': None
    },
    'iPad3,2': {
        'generation': 3,
        'cellular': 'CDMA'
    },
    'iPad3,3': {
        'generation': 3,
        'cellular': 'GSM'
    },
    'iPad2,5': {
        'generation': 1,
        'cellular': None
    },
    'iPad2,6': {
        'generation': 1,
        'cellular': 'GSM+LTE'
    },
    'iPad2,7': {
        'generation': 1,
        'cellular': 'CDMA+LTE'
    },
    'iPad3,4': {'generation': 4, 'cellular': None},
    'iPad3,5': {'generation': 4, 'cellular': 'GSM+LTE'},
    'iPad3,6': {'generation': 4, 'cellular': 'CDMA+LTE'},
    'iPad4,1': {'generation': 1, 'cellular': None},
    'iPad4,2': {'generation': 1, 'cellular': 'GSM+CDMA'},
    'iPad4,3': {'generation': 1, 'cellular': 'GSM+CDMA', 'spec': 'CN'},
    'iPad4,4': {'generation': 2, 'cellular': None},
    'iPad4,5': {'generation': 2, 'cellular': 'GSM+CDMA'},
    'iPad4,6': {'generation': 2, 'cellular': 'GSM+CDMA', 'spec': 'CN'},
    'iPad4,7': {'generation': 3, 'cellular': None},
    'iPad4,8': {'generation': 3, 'cellular': 'GSM+CDMA'},
    'iPad4,9': {'generation': 3, 'cellular': 'GSM+CDMA', 'spec': 'CN'},
    'iPad5,1': {'generation': 4, 'cellular': None},
    'iPad5,2': {'generation': 4, 'cellular': "WiFi+Cellular"},
    'iPad5,3': {'generation': 2, 'cellular': None},
    'iPad5,4': {'generation': 2, 'cellular': True},
    'iPad6,3': {'generation': 1, 'cellular': None, 'screen_size': "9.7"},
    'iPad6,4': {'generation': 1, 'cellular': True, 'screen_size': "9.7"},
    'iPad6,7': {'generation': 1, 'cellular': None, 'screen_size': "12.9"},
    'iPad6,8': {'generation': 1, 'cellular': True, 'screen_size': "12.9"},
    'iPad6,11': {'generation': 5, 'cellular': None},
    'iPad6,12': {'generation': 5, 'cellular': True},
    'iPad7,1': {'generation': 2, 'cellular': None, 'screen_size': '12.9'},
    'iPad7,2': {'generation': 2, 'cellular': True, 'screen_size': '12.9'},
    'iPad7,3': {'generation': 1, 'cellular': None, 'screen_size': '10.5'},
    'iPad7,4': {'generation': 1, 'cellular': True, 'screen_size': '10.5'},
    'iPad7,5': {'generation': 6, 'cellular': None},
    'iPad7,6': {'generation': 6, 'cellular': True},
    'iPad7,11': {'generation': 7, 'cellular': None, 'screen_size': '10.2'},
    'iPad7,12': {'generation': 7, 'cellular': True, 'screen_size': '10.2'},
    'iPad8,1': {'generation': 3, 'cellular': None, 'screen_size': '11'},
    'iPad8,2': {'generation': 3, 'cellular': None, 'screen_size': '11'},
    'iPad8,3': {'generation': 3, 'cellular': True, 'screen_size': '11'},
    'iPad8,4': {'generation': 3, 'cellular': True, 'screen_size': '11'},
    'iPad8,5': {'generation': 3, 'cellular': None, 'screen_size': '12.9'},
    'iPad8,6': {'generation': 3, 'cellular': None, 'screen_size': '12.9'},
    'iPad8,7': {'generation': 3, 'cellular': True, 'screen_size': '12.9'},
    'iPad8,8': {'generation': 3, 'cellular': True, 'screen_size': '12.9'},
    'iPad8,9': {'generation': 4, 'cellular': None, 'screen_size': '11'},
    'iPad8,10': {'generation': 4, 'cellular': True, 'screen_size': '11'},
    'iPad8,11': {'generation': 4, 'cellular': None, 'screen_size': '12.9'},
    'iPad8,12': {'generation': 4, 'cellular': True, 'screen_size': '12.9'},
    'iPad11,1': {'generation': 5, 'cellular': None},
    'iPad11,2': {'generation': 5, 'cellular': True},
    'iPad11,3': {'generation': 3, 'cellular': None},
    'iPad11,4': {'generation': 3, 'cellular': True},
    'iPad11,6': {'generation': 8, 'cellular': None},
    'iPad11,7': {'generation': 8, 'cellular': True},
    'iPad12,1': {'generation': 9, 'cellular': None},
    'iPad12,2': {'generation': 9, 'cellular': True},
    'iPad14,1': {'generation': 6, 'cellular': None},
    'iPad14,2': {'generation': 6, 'cellular': True},
    'iPad13,1': {'generation': 4, 'cellular': None},
    'iPad13,2': {'generation': 4, 'cellular': True},
    'iPad13,4': {'generation': 5, 'cellular': None, 'screen_size': '11'},
    'iPad13,5': {'generation': 5, 'cellular': None, 'screen_size': '11'},
    'iPad13,6': {'generation': 5, 'cellular': True, 'screen_size': '11'},
    'iPad13,7': {'generation': 5, 'cellular': True, 'screen_size': '11'},
    'iPad13,8': {'generation': 5, 'cellular': None, 'screen_size': '12.9'},
    'iPad13,9': {'generation': 5, 'cellular': None, 'screen_size': '12.9'},
    'iPad13,10': {'generation': 5, 'cellular': True, 'screen_size': '12.9'},
    'iPad13,11': {'generation': 5, 'cellular': True, 'screen_size': '12.9'},
    'iPad13,16': {'generation': 5, 'cellular': None},
    'iPad13,17': {'generation': 5, 'cellular': True},
    'iPad13,18': {'generation': 10, 'cellular': False},
    'iPad13,19': {'generation': 10, 'cellular': True},
    #'iPad13,18': iPad 10th Gen
    #'iPad13,19': iPad 10th Gen
    #'iPad14,3': iPad Pro 11 inch 4th Gen
    #'iPad14,4': iPad Pro 11 inch 4th Gen
    #'iPad14,5': iPad Pro 12.9 inch 6th Gen
    #'iPad14,6': iPad Pro 12.9 inch 6th Gen
}


DEFAULT_GRADINGS: dict[str, int] = {
    'A+'    : 0,
    'A'     : 1,
    'B+'    : 2,
    'B'     : 3,
    'C+'    : 4,
    'C'     : 5,
    'D'     : 6
}