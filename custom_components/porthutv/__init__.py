"""
Custom integration to integrate PortHuTV with Home Assistant.

For more details about this integration, please refer to
https://github.com/vorostamas/portHuTV-homeassistant
"""
import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.porthutv.const import (
    CONF_TV_CHANNEL_ID,
    CONF_TV_CHANNEL_NAME,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

from custom_components.porthutv.schedules import get_schedules

SCAN_INTERVAL = timedelta(minutes=30)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    channel_id = entry.data.get(CONF_TV_CHANNEL_ID)
    channel_name = entry.data.get(CONF_TV_CHANNEL_NAME)

    coordinator = PortHuTvDataUpdateCoordinator(
        hass, channel_id=channel_id, channel_name=channel_name
    )
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.add_update_listener(async_reload_entry)
    return True


class PortHuTvDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, channel_id, channel_name):
        """Initialize."""
        self.platforms = []
        self.channel_id = channel_id
        self.channel_name = channel_name

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            _LOGGER.debug("Channel ID: %s", self.channel_id)
            _LOGGER.debug("Channel Name: %s", self.channel_name)

            schedule = get_schedules(self.channel_id)
            # _LOGGER.debug("Schedule: %s", schedule)

            data = {"channel_name": self.channel_name, "schedule": schedule}
            return data
        except Exception as exception:
            raise UpdateFailed(exception)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
