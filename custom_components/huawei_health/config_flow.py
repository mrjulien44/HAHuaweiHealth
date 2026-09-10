"""Config flow for Huawei Health integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .api import HuaweiHealthApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HuaweiHealthConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Huawei Health."""

    VERSION = 1

    def __init__(self):
        self._user_input: dict | None = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Manage the initial step and defer to Health Kit authorization if needed."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input["account_id"])
            self._abort_if_unique_id_configured()

            client = HuaweiHealthApiClient(
                username=user_input["username"],
                password=user_input["password"],
                country=user_input.get("country", "global"),
                region=user_input.get("region", "global"),
                account_id=user_input.get("account_id"),
            )
            self._user_input = user_input

            if await client.async_get_health_app_authorization():
                return self.async_create_entry(
                    title=user_input["username"],
                    data=user_input,
                )

            return await self.async_step_healthkit()

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

    async def async_step_healthkit(self, user_input=None) -> FlowResult:
        """Show a follow-up Health Kit authorization gate when the app did not grant access."""
        if self._user_input is None:
            return self.async_abort(reason="unknown")

        if user_input is not None:
            client = HuaweiHealthApiClient(
                username=self._user_input["username"],
                password=self._user_input["password"],
                country=self._user_input.get("country", "global"),
                region=self._user_input.get("region", "global"),
                account_id=self._user_input.get("account_id"),
            )
            if await client.async_get_health_app_authorization():
                return self.async_create_entry(
                    title=self._user_input["username"],
                    data=self._user_input,
                )

        return self.async_show_form(
            step_id="healthkit",
            data_schema=vol.Schema({}),
            errors={"base": "healthkit_not_authorized"},
        )
