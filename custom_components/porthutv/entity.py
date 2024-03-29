"""PortHuTvEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.porthutv.const import DOMAIN, NAME, VERSION


class PortHuTvEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return {
            "next_show": self.coordinator.data.get("next_show_title"),
            "previous_show": self.coordinator.data.get("previous_show_title"),
            "schedule": self.coordinator.data.get("schedule"),
        }
