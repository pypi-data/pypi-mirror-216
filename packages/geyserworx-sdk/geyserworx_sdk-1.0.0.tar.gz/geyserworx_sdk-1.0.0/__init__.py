import enum
import json

from aiohttp import ClientSession


class PowerType(enum):
    AC = 'ACM'
    AC_BOOST = 'ACO'
    PV = 'PVM'


class TemperatureType(enum):
    AC = 'ACT'
    AC_BOOST = 'ACOT'
    PV = 'PVT'


class GeyserworxAPI:
    __API_BASE__ = 'gwa/'
    __TOPIC_BASE_GET__ = 'GWA'
    __TOPIC_BASE_SET__ = 'GWR'

    def __init__(
            self,
            session: ClientSession,
            geyser_serial_number: str,
            geyser_number: int = 1,
            base_url: str = "http://192.168.4.1"
    ):
        self.geyser_serial_number = geyser_serial_number
        self.geyser_number = geyser_number
        self.base_url_get = f'{base_url}{self.__API_BASE__}?topic={self.__TOPIC_BASE_GET__}/{self.geyser_serial_number}/{self.geyser_number}/'
        self.base_url_set = f'{base_url}{self.__API_BASE__}?topic={self.__TOPIC_BASE_SET__}/{self.geyser_serial_number}/{self.geyser_number}/'
        self.session = session

    async def get_current_temperature(self) -> float:
        url = f'{self.base_url_get}A'
        response = await self.session.get(url)
        response_json: dict = await response.json()
        return response_json['T']['G']

    async def get_settings(self) -> dict:
        url = f'{self.base_url_get}SET'
        response = await self.session.get(url)
        response_json: dict = await response.json()
        return {
            'POWER': {
                'AC': True if response_json['O']['ACM'] == 1 else False,
                'AC_BOOST': True if response_json['O']['ACO'] == 1 else False,
                'PV': True if response_json['O']['PVM'] == 1 else False
            },
            'TEMP': {
                'AC': response_json['S']['ACT'],
                'AC_BOOST': response_json['S']['ACOT'],
                'PV': response_json['S']['PVT']
            }
        }

    async def get_power_status(self) -> dict[str, bool]:
        url = f'{self.base_url_get}STS'
        response = await self.session.get(url)
        response_json: dict = await response.json()
        return {
            'AC': True if response_json['O']['AC'] == 1 else False,
            'PV': True if response_json['O']['PV'] == 1 else False
        }

    async def set_power(self, power_type: PowerType, on: bool) -> bool:
        payload = {
            'O': {
                power_type.value: 1 if on else 0
            }
        }
        url = f'{self.base_url_set}STS/O&payload={json.dumps(payload)}'
        response = await self.session.get(url)
        response_json: dict = await response.json()
        return response_json['O'][power_type.value] == 1

    async def set_temp(self, temperature_type: TemperatureType, temperature: int) -> int:
        payload = {
            'S': {
                temperature_type.value: temperature
            }
        }
        url = f'{self.base_url_set}STS/S&payload={json.dumps(payload)}'
        response = await self.session.get(url)
        response_json: dict = await response.json()
        return response_json['S'][temperature_type.value]
