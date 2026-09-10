"""Sensor platform for Huawei Health."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Huawei Health sensors from a config entry using the typed data model."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    entities = [
        HuaweiHealthSensor(coordinator, sensor_key, sensor_config)
        for sensor_key, sensor_config in SENSOR_TYPES.items()
    ]
    async_add_entities(entities)


class HuaweiHealthSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Huawei Health sensor mapped to the real model object."""

    def __init__(self, coordinator, sensor_key: str, config: dict):
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._config = config
        self._attr_unique_id = f"{DOMAIN}_{sensor_key}_{coordinator.client.account_id}"
        self._attr_name = f"Huawei Health {config['name']}"
        self._attr_native_unit_of_measurement = config.get("unit")
        self._attr_icon = config.get("icon")

    @property
    def native_value(self):
        summary = self.coordinator.data.summary
        profile = self.coordinator.data.profile
        mapping = {
            "steps": summary.steps,
            "distance": summary.distance_km,
            "calories": summary.calories_kcal,
            "heart_rate": summary.heart_rate_bpm,
            "sleep_duration": summary.sleep_duration_min,
            "weight": profile.weight_kg,
            "height": profile.height_cm,
            "bmi": profile.bmi,
            "sleep_deep": summary.sleep_deep_min,
            "sleep_shallow": summary.sleep_shallow_min,
            "sleep_dream": summary.sleep_dream_min,
            "stress_score": summary.stress_score,
            "body_fat_pct": summary.body_fat_pct,
        }
        return mapping.get(self._sensor_key)

    @property
    def extra_state_attributes(self):
        extra = self.coordinator.data.summary.extra or {}
        return {
            "source": "huawei_health",
            "account_id": self.coordinator.client.account_id,
            "measurement_date": self.coordinator.data.summary.measurement_date,
            "gender": self.coordinator.data.profile.gender,
            "body_composition_history": extra.get("body_composition_history", []),
            "sleep_depth_history": extra.get("sleep_depth_history", []),
            "stress_history": extra.get("stress_history", []),
        }
