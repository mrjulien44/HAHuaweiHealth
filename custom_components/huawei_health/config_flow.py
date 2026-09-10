"""Config flow for Huawei Health integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .api import HuaweiHealthApiClient
from .const import DOMAIN

COUNTRY_OPTIONS = [
    "global",
    "CN",
    "US",
    "DE",
    "FR",
    "ES",
    "IT",
    "UK",
    "JP",
    "KR",
    "IN",
]

REGION_OPTIONS = [
    "global",
    "CN",
    "EU",
    "APAC",
    "US",
]

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
                client_id=user_input.get("client_id"),
                client_secret=user_input.get("client_secret"),
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
                    vol.Required("country", default="global"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=COUNTRY_OPTIONS,
                            mode="dropdown",
                            custom_value=False,
                        )
                    ),
                    vol.Required("region", default="global"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=REGION_OPTIONS,
                            mode="dropdown",
                            custom_value=False,
                        )
                    ),
                    vol.Required("account_id"): str,
                    vol.Optional("client_id"): str,
                    vol.Optional("client_secret"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_healthkit(self, user_input=None) -> FlowResult:
        """Show a Health Kit authorization page with refresh and quit menu options."""
        if self._user_input is None:
            return self.async_abort(reason="unknown")

        return self.async_show_menu(
            menu_options=["refresh", "quit"],
        )

    async def async_step_refresh(self, user_input=None) -> FlowResult:
        """Re-run the Health Kit authorization probe and resume the flow if the app now grants access."""
        if self._user_input is None:
            return self.async_abort(reason="unknown")

        client = HuaweiHealthApiClient(
            username=self._user_input["username"],
            password=self._user_input["password"],
            country=self._user_input.get("country", "global"),
            region=self._user_input.get("region", "global"),
            account_id=self._user_input.get("account_id"),
            client_id=self._user_input.get("client_id"),
            client_secret=self._user_input.get("client_secret"),
            access_token=self._user_input.get("access_token"),
            refresh_token=self._user_input.get("refresh_token"),
        )

        if await client.async_get_health_app_authorization():
            return self.async_create_entry(
                title=self._user_input["username"],
                data=self._user_input,
            )

        return self.async_show_menu(
            menu_options=["refresh", "quit"],
        )

    async def async_step_quit(self, user_input=None) -> FlowResult:
        """Abort the Health Kit page and end the configuration flow cleanly."""
        return self.async_abort(reason="user_quit")
