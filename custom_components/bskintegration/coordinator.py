import logging
from datetime import timedelta

import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import STATUS_URL

_LOGGER = logging.getLogger(__name__)


class BSKFanCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config_entry):
        self._config_entry = config_entry
        super().__init__(hass, _LOGGER, name="BSK Fan Coordinator", update_interval=timedelta(seconds=10))

    async def _async_update_data(self):
        headers = {"Authorization": f"{self._config_entry.data['jwt_token']}",
                   "Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(STATUS_URL, headers=headers) as resp:
                if resp.status == 200:
                    json = await resp.json()
                    print(json)
                    return json[0]
                else:
                    raise Exception("Failed to fetch fan data")
