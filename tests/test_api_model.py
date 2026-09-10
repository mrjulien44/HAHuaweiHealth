import sys
import types
import unittest

# Provide lightweight Home Assistant stubs so the package can be imported in
# a minimal test runtime without a full Home Assistant installation.
homeassistant = types.ModuleType("homeassistant")
config_entries = types.ModuleType("homeassistant.config_entries")
core = types.ModuleType("homeassistant.core")
const = types.ModuleType("homeassistant.const")
coord = types.ModuleType("homeassistant.helpers.update_coordinator")
platform = types.ModuleType("homeassistant.helpers.entity_platform")
calendar_component = types.ModuleType("homeassistant.components.calendar")
sensor_component = types.ModuleType("homeassistant.components.sensor")
data_flow = types.ModuleType("homeassistant.data_entry_flow")

class ConfigEntry:
    def __init__(self):
        self.entry_id = "test-entry"
        self.data = {}

class HomeAssistant:
    pass

class Platform:
    SENSOR = "sensor"
    CALENDAR = "calendar"

class DataUpdateCoordinator:
    def __init__(self, hass, logger, name=None, update_interval=None):
        self.hass = hass
        self.logger = logger
        self.name = name
        self.update_interval = update_interval
        self.data = None

class UpdateFailed(Exception):
    pass

class CalendarEntity:
    pass

class CalendarEvent:
    def __init__(self, summary=None, start=None, end=None, description=None):
        self.summary = summary
        self.start = start
        self.end = end
        self.description = description

class SensorEntity:
    pass

class CoordinatorEntity:
    def __init__(self, coordinator):
        self.coordinator = coordinator

class AddEntitiesCallback:
    pass

config_entries.ConfigEntry = ConfigEntry
core.HomeAssistant = HomeAssistant
const.Platform = Platform
coord.DataUpdateCoordinator = DataUpdateCoordinator
coord.UpdateFailed = UpdateFailed
coord.CoordinatorEntity = CoordinatorEntity
platform.AddEntitiesCallback = AddEntitiesCallback
calendar_component.CalendarEntity = CalendarEntity
calendar_component.CalendarEvent = CalendarEvent
sensor_component.SensorEntity = SensorEntity

homeassistant.config_entries = config_entries
homeassistant.core = core
homeassistant.const = const
homeassistant.helpers = types.ModuleType("homeassistant.helpers")
homeassistant.helpers.update_coordinator = coord
homeassistant.helpers.entity_platform = platform
homeassistant.components = types.ModuleType("homeassistant.components")
homeassistant.components.calendar = calendar_component
homeassistant.components.sensor = sensor_component
homeassistant.data_entry_flow = data_flow
homeassistant.data_entry_flow.FlowResult = dict

sys.modules.setdefault("homeassistant", homeassistant)
sys.modules.setdefault("homeassistant.config_entries", config_entries)
sys.modules.setdefault("homeassistant.core", core)
sys.modules.setdefault("homeassistant.const", const)
sys.modules.setdefault("homeassistant.helpers", homeassistant.helpers)
sys.modules.setdefault("homeassistant.helpers.update_coordinator", coord)
sys.modules.setdefault("homeassistant.helpers.entity_platform", platform)
sys.modules.setdefault("homeassistant.components", homeassistant.components)
sys.modules.setdefault("homeassistant.components.calendar", calendar_component)
sys.modules.setdefault("homeassistant.components.sensor", sensor_component)
sys.modules.setdefault("homeassistant.data_entry_flow", data_flow)

from custom_components.huawei_health.api import HuaweiHealthApiClient


class HuaweiHealthApiClientPayloadModelTest(unittest.TestCase):
    def test_build_data_from_real_payload(self):
        client = HuaweiHealthApiClient(
            username="demo",
            password="demo",
            country="global",
            region="global",
            account_id="acct-123",
        )

        payload = {
            "profile": {
                "username": "demo",
                "account_id": "acct-123",
                "country": "global",
                "region": "global",
                "gender": "female",
                "birthday": "1998-01-01",
                "height_cm": 170.0,
                "weight_kg": 70.0,
                "bmi": 24.2,
            },
            "summary": {
                "steps": 123,
                "distance_km": 1.0,
                "calories_kcal": 50,
                "heart_rate_bpm": 70,
                "sleep_duration_min": 400,
                "sleep_deep_min": 100,
                "sleep_shallow_min": 200,
                "sleep_dream_min": 100,
                "stress_score": 80,
                "body_fat_pct": 20.0,
                "active_minutes": 30,
                "measurement_date": "2026-09-10",
                "extra": {
                    "body_composition_history": [],
                    "sleep_depth_history": [],
                    "stress_history": [],
                },
            },
            "statistics": {
                "total_steps": 123,
                "total_distance_km": 1.0,
                "total_calories_kcal": 50,
                "average_heart_rate_bpm": 70,
                "active_minutes": 30,
                "sleep_duration_min": 400,
                "stress_score": 80,
                "body_fat_pct": 20.0,
                "period_start": "2026-09-10",
                "period_end": "2026-09-10",
            },
            "activities": [
                {
                    "activity_id": "activity-1",
                    "activity_type": "walk",
                    "start": "2026-09-10T07:00:00",
                    "end": "2026-09-10T08:00:00",
                    "duration_min": 60,
                    "distance_km": 1.0,
                    "calories_kcal": 50,
                    "steps": 123,
                    "average_speed_kmh": 1.0,
                    "average_pace_min_km": 9.8,
                    "average_heart_rate_bpm": 70,
                    "max_heart_rate_bpm": 78,
                    "sport_source": "huawei_health",
                    "metadata": {},
                }
            ],
            "events": [
                {
                    "summary": "Huawei Health Walk",
                    "start": "2026-09-10T07:00:00",
                    "end": "2026-09-10T08:00:00",
                    "description": "Walk event",
                    "event_type": "activity",
                    "source": "huawei_health",
                    "sport_type": "walk",
                    "metadata": {"activity_id": "activity-1"},
                }
            ],
        }

        data = client._build_huawei_health_data(payload)

        self.assertEqual(data.profile.username, "demo")
        self.assertEqual(data.summary.steps, 123)
        self.assertEqual(data.statistics.total_steps, 123)
        self.assertEqual(len(data.activities), 1)
        self.assertEqual(len(data.events), 1)


if __name__ == "__main__":
    unittest.main()
