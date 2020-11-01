"""Sensor platform for porthutv."""
from custom_components.porthutv.const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from custom_components.porthutv.entity import BlueprintEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([BlueprintSensor(coordinator, entry)])


class BlueprintSensor(BlueprintEntity):
    """porthutv Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.coordinator.data.get("channel_name")

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("static")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON
