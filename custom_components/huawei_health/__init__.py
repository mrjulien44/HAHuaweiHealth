"""The Huawei Health integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import HuaweiHealthApiClient
from .const import DOMAIN, SCAN_INTERVAL
from .models import HuaweiHealthData

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.CALENDAR, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Huawei Health from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    client = HuaweiHealthApiClient(
        username=entry.data["username"],
        password=entry.data["password"],
        country=entry.data.get("country", "global"),
        region=entry.data.get("region", "global"),
        account_id=entry.data.get("account_id"),
        client_id=entry.data.get("client_id"),
        client_secret=entry.data.get("client_secret"),
        access_token=entry.data.get("access_token"),
        refresh_token=entry.data.get("refresh_token"),
    )

    coordinator = HuaweiHealthDataCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class HuaweiHealthDataCoordinator(DataUpdateCoordinator):
    """Coordinator that polls Huawei Health data using the typed model."""

    def __init__(self, hass: HomeAssistant, client: HuaweiHealthApiClient):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> HuaweiHealthData:
        try:
            return await self.client.async_get_data()
        except Exception as exc:
            raise UpdateFailed(f"Error communicating with Huawei Health: {exc}") from exc
