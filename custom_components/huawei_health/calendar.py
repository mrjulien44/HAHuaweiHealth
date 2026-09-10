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

        for record in self.coordinator.data.workout_records:
            if record.start <= end_date and record.end >= start_date:
                events.append(CalendarEvent(
                    summary=f"Huawei Health {record.activity_type.title()}",
                    start=record.start,
                    end=record.end,
                    description=(
                        f"Huawei Health workout record sync: {record.activity_type} "
                        f"({record.duration_min} min, {record.distance_km} km)"
                    ),
                ))

        for activity in self.coordinator.data.daily_activities:
            item_date = datetime.fromisoformat(activity.date).replace(hour=0, minute=0, second=0, microsecond=0)
            if item_date.date() >= start_date.date() and item_date.date() <= end_date.date():
                events.append(CalendarEvent(
                    summary="Huawei Health Daily Activity",
                    start=item_date,
                    end=item_date.replace(hour=23, minute=59, second=59, microsecond=999999),
                    description=(
                        f"Huawei Health daily activity sync: {activity.steps} steps, "
                        f"{activity.distance_km} km, {activity.calories_kcal} kcal"
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
