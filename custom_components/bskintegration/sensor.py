from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import BSKFanCoordinator


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up sensor platform from a config entry."""

    coordinator = BSKFanCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    # Create instances of the sensor entities
    temperature_sensor = FanTemperatureSensor(coordinator=coordinator, entry=config_entry)
    humidity_sensor = FanHumiditySensor(coordinator, config_entry)

    # Add the entities to Home Assistant
    async_add_entities([temperature_sensor, humidity_sensor])


class FanTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of the temperature sensor associated with the fan."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_name = "Fan Temperature"
        self._attr_unique_id = f"bsk_{entry.entry_id}_temperature"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = TEMP_CELSIUS

    @property
    def native_value(self):
        """Return the current temperature."""
        return round(self.coordinator.data.get("temperature"),1)


class FanHumiditySensor(CoordinatorEntity, SensorEntity):
    """Representation of the humidity sensor associated with the fan."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_name = "Fan Humidity"
        self._attr_unique_id = f"bsk_{entry.entry_id}_humidity"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self):
        """Return the current humidity."""
        return round(self.coordinator.data.get("humidity"),1)
