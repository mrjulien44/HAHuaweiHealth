"""Button platform for Huawei Health manual refresh."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a Huawei Health manual refresh button from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([HuaweiHealthRefreshButton(coordinator)])


class HuaweiHealthRefreshButton(CoordinatorEntity, ButtonEntity):
    """Expose a manual refresh action for the Huawei Health coordinator."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_manual_refresh_{coordinator.client.account_id}"
        self._attr_name = "Refresh Huawei Health"

    async def async_press(self) -> None:
        """Trigger a manual refresh through the data coordinator."""
        await self.coordinator.async_request_refresh()
