"""Adds config flow for PortHuTV."""
from homeassistant import config_entries
from homeassistant.core import callback
from sampleclient.client import Client
import voluptuous as vol

from custom_components.porthutv.const import (
    CONF_TV_CHANNEL_ID,
    DOMAIN,
    PLATFORMS,
)

from custom_components.porthutv.channel_id_validation import validate_channel_id
from custom_components.porthutv.schedules import get_channel_name


class PortHuTvFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PortHuTV."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(
        self, user_input=None  # pylint: disable=bad-continuation
    ):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._validate_input(user_input[CONF_TV_CHANNEL_ID])
            if valid:
                channel_name = get_channel_name(user_input[CONF_TV_CHANNEL_ID])
                user_input["channel_name"] = channel_name
                return self.async_create_entry(title=channel_name, data=user_input)
            else:
                self._errors["base"] = "invalid_channel_id"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PortHuTvOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_TV_CHANNEL_ID): str}),
            errors=self._errors,
        )

    async def _validate_input(self, channel_id):
        """Return true if channel ID is valid."""
        return validate_channel_id(channel_id)


class PortHuTvOptionsFlowHandler(config_entries.OptionsFlow):
    """PortHuTv config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_TV_CHANNEL_ID), data=self.options
        )
