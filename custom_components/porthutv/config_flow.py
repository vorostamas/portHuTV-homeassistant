"""Adds config flow for PortHuTV."""
from homeassistant import config_entries
from homeassistant.core import callback
from sampleclient.client import Client
import voluptuous as vol

from custom_components.porthutv.const import (  # pylint: disable=unused-import
    CONF_PASSWORD,
    CONF_TV_CHANNEL,
    DOMAIN,
    PLATFORMS,
)


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
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
            valid = await self._test_channel_id(
                user_input[CONF_TV_CHANNEL], user_input[CONF_PASSWORD]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_TV_CHANNEL], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BlueprintOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_TV_CHANNEL): str, vol.Required(CONF_PASSWORD): str}
            ),
            errors=self._errors,
        )

    async def _test_channel_id(self, channel_id, password):
        """Return true if channel ID is valid."""
        # TODO: implement channel ID validation.
        try:
            client = Client(channel_id, password)
            await client.async_get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class BlueprintOptionsFlowHandler(config_entries.OptionsFlow):
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
            title=self.config_entry.data.get(CONF_TV_CHANNEL), data=self.options
        )
