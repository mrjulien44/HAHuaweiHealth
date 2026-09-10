"""Calendar platform for Huawei Health events."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Huawei Health calendar from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([HuaweiHealthCalendar(coordinator)])


class HuaweiHealthCalendar(CoordinatorEntity, CalendarEntity):
    """Dedicated Home Assistant calendar for Huawei Health activities."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_calendar_{coordinator.client.account_id}"
        self._attr_name = "Huawei Health"

    async def async_get_events(self, start_date: datetime, end_date: datetime):
        """Return Home Assistant calendar events from the activity model and event model."""
        events = []

        for activity in self.coordinator.data.activities:
            if activity.start <= end_date and activity.end >= start_date:
                events.append(CalendarEvent(
                    summary=f"Huawei Health {activity.activity_type.title()}",
                    start=activity.start,
                    end=activity.end,
                    description=(
                        f"Huawei Health activity sync: {activity.activity_type} "
                        f"({activity.duration_min} min, {activity.distance_km} km)"
                    ),
                ))

        for item in self.coordinator.data.events:
            if item.start <= end_date and item.end >= start_date:
                events.append(CalendarEvent(
                    summary=item.summary,
                    start=item.start,
                    end=item.end,
                    description=item.description,
                ))

        return events

    async def async_create_event(self, summary: str, start_date_time: datetime, end_date_time: datetime, description: str | None = None):
        """Create a calendar event payload in the Huawei Health model shape."""
        return {
            "summary": summary,
            "start": start_date_time.isoformat(),
            "end": end_date_time.isoformat(),
            "description": description,
        }
