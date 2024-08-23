import logging

import aiohttp
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import UPDATE_URL
from .coordinator import BSKFanCoordinator

_LOGGER = logging.getLogger(__name__)


class BSKFanEntity(FanEntity, CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "BSK Fan"
        self._attr_unique_id = config_entry.entry_id
        self._attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE
        self._attr_preset_modes = ['extract', 'supply', 'cycle']
        self._data = {
            "deviceID": self.coordinator.data["deviceID"],
            "groupID": self.coordinator.data["groupID"],
            "boostTime": -1,
            "humidityBoost": 100,
            "cycleTime": 50,
            "cycleDirection": "parallel",
            "fanSpeed": self.coordinator.data['settings']['fanSpeed'],
            "fanMode": self.coordinator.data['settings']['fanMode'],
            "deviceStatus": self.coordinator.data['settings']['deviceStatus'],
        }

    @property
    def is_on(self):
        self._data["deviceStatus"] = self.coordinator.data["settings"]["deviceStatus"]
        return self._data["deviceStatus"] == "On"

    @property
    def percentage(self):
        self._data["fanSpeed"] = self.coordinator.data["settings"]["fanSpeed"]
        return self._data["fanSpeed"]

    @property
    def current_temperature(self):
        return self.coordinator.data["temperature"]

    @property
    def current_humidity(self):
        return self.coordinator.data["humidity"]

    @property
    def fan_mode(self):
        self._data["fanMode"] = self.coordinator.data["settings"]["fanMode"]
        return self._data["fanMode"]

    @property
    def preset_mode(self) -> str | None:
        self._data["fanMode"] = self.coordinator.data["settings"]["fanMode"]
        return self._data["fanMode"]

    async def async_turn_on(self, *args, **kwargs):
        self._data["deviceStatus"] = "On"
        await self._send_update()

    async def async_turn_off(self, **kwargs):
        self._data["deviceStatus"] = "Off"
        await self._send_update()

    async def async_set_percentage(self, percentage):
        self._data["fanSpeed"] = percentage
        await self._send_update()

    async def async_set_preset_mode(self, preset_mode):
        self._data["fanMode"] = preset_mode
        await self._send_update()

    async def _send_update(self):
        headers = {"Authorization": f"{self._config_entry.data['jwt_token']}",
                   "Content-Type": "application/json"}
        print(self._data)
        async with aiohttp.ClientSession() as session:
            async with session.post(UPDATE_URL, headers=headers, json=self._data) as resp:
                if resp.status != 200:
                    print(await resp.content.read())
                    _LOGGER.error("Failed to update fan settings: %s", resp.content)

    async def async_update(self):
        self.async_write_ha_state()


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = BSKFanCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([BSKFanEntity(coordinator, config_entry)])
