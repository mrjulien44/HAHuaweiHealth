"""Config flow for Huawei Health integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HuaweiHealthConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Huawei Health."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Manage the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate login credentials against Huawei Health API here.
            # For this scaffold, avoid an external dependency and accept inputs
            # as mandatory configuration values.
            await self.async_set_unique_id(user_input["account_id"])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input["username"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                    vol.Required("country", default="global"): str,
                    vol.Required("region", default="global"): str,
                    vol.Required("account_id"): str,
                }
            ),
            errors=errors,
        )
