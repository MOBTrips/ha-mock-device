"""Config flow for Mock Device.

The flow intentionally has no credentials or user options. This keeps setup repeatable
for QA and prevents accidental differences between testers.
"""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_SINGLE_INSTANCE_ID, DOMAIN


class MockDeviceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Mock Device."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Create one Mock Device instance.

        v0.1.0 allows only one instance because stable entity IDs are important for
        repeatable QA packs. Multiple instances would cause HA to add suffixes.
        """
        await self.async_set_unique_id(CONF_SINGLE_INSTANCE_ID)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Mock Device", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MockDeviceOptionsFlow(config_entry)


class MockDeviceOptionsFlow(config_entries.OptionsFlow):
    """Options flow placeholder.

    Runtime controls are exposed as HA entities instead of setup options so testers can
    change behavior without reloading the integration.
    """

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
