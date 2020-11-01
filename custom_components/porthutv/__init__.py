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
from sampleclient.client import Client

from custom_components.porthutv.const import (
    CONF_TV_CHANNEL,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

from custom_components.porthutv.schedules import get_channel_name

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    channel = entry.data.get(CONF_TV_CHANNEL)

    coordinator = BlueprintDataUpdateCoordinator(hass, channel=channel)
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


class BlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, channel):
        """Initialize."""
        self.api = Client(channel, "password")
        self.platforms = []
        self.channel = channel

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            _LOGGER.debug("Channel ID: %s", self.channel)
            data = await self.api.async_get_data()
            return data.get("data", {})
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
