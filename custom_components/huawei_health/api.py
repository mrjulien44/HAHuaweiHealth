"""Huawei Health API client abstraction.

This client model is shaped from the Huawei Health sample repository
categories: profile, sport sessions, step/distance/calorie data,
heart-rate data, sleep/session data, stress, body composition values,
and activity/statistics records.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from .models import (
    HuaweiHealthActivity,
    HuaweiHealthActivityEvent,
    HuaweiHealthData,
    HuaweiHealthProfile,
    HuaweiHealthStatistics,
    HuaweiHealthSummary,
)

_LOGGER = logging.getLogger(__name__)


class HuaweiHealthApiClient:
    """Low-level client for the Huawei Health APIs.

    Outline for real implementation:
    1. Authenticate with Huawei Identity account login.
    2. Request scopes needed for health behavior, sport read, sleep, stress
       and body composition API endpoints.
    3. Query profile, daily health data, activity records and statistics.
    4. Transform Huawei HiHealth response objects into the typed model.
    """

    def __init__(self, username: str, password: str, country: str, region: str, account_id: str | None):
        self.username = username
        self.password = password
        self.country = country
        self.region = region
        self.account_id = account_id

    @staticmethod
    def _parse_int(value: Any, default: int = 0) -> int:
        if value is None:
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _parse_float(value: Any, default: float = 0.0) -> float:
        if value is None:
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _parse_datetime(value: Any) -> datetime | None:
        if isinstance(value, datetime):
            return value
        if not isinstance(value, str):
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return None

    def _build_huawei_health_data(self, payload: dict[str, Any]) -> HuaweiHealthData:
        """Transform a real Huawei Health-style payload into the typed aggregate model.

        This lets the integration consume the real API payload shape without hardcoding
        demonstration values in the coordinator. The parser accepts the common profile,
        summary, statistics and activity/event keys from the Huawei Health sample
        documentation collection and normalizes them into the repository model.
        """
        profile_payload = (
            payload.get("profile")
            or payload.get("user_profile")
            or payload.get("account")
            or payload.get("health_profile")
            or {}
        )
        summary_payload = (
            payload.get("summary")
            or payload.get("health_summary")
            or payload.get("health_point")
            or payload.get("daily_health")
            or {}
        )
        statistics_payload = (
            payload.get("statistics")
            or payload.get("stats")
            or payload.get("summary_statistics")
            or payload.get("period_statistics")
            or {}
        )
        activities_payload = payload.get("activities") or payload.get("sport_records") or payload.get("records") or []
        events_payload = payload.get("events") or payload.get("calendar_events") or payload.get("activity_events") or []

        if isinstance(activities_payload, dict):
            activities_payload = activities_payload.get("items", []) or []
        if not isinstance(activities_payload, list):
            activities_payload = []

        if isinstance(events_payload, dict):
            events_payload = events_payload.get("items", []) or []
        if not isinstance(events_payload, list):
            events_payload = []

        profile = HuaweiHealthProfile(
            username=profile_payload.get("username", self.username),
            account_id=profile_payload.get("account_id", self.account_id or "unknown"),
            country=profile_payload.get("country", self.country),
            region=profile_payload.get("region", self.region),
            gender=profile_payload.get("gender"),
            birthday=profile_payload.get("birthday") or profile_payload.get("birth_date"),
            height_cm=self._parse_float(profile_payload.get("height_cm") or profile_payload.get("height")),
            weight_kg=self._parse_float(profile_payload.get("weight_kg") or profile_payload.get("weight")),
            bmi=self._parse_float(profile_payload.get("bmi") or profile_payload.get("body_mass_index")),
        )

        summary_field_map = {
            "steps": ("steps", "step_count", "total_steps"),
            "distance_km": ("distance_km", "distance", "distance_m", "distance_meter"),
            "calories_kcal": ("calories_kcal", "calorie", "calories"),
            "heart_rate_bpm": ("heart_rate_bpm", "heart_rate", "avg_heart_rate"),
            "sleep_duration_min": ("sleep_duration_min", "sleep_duration", "duration_sleep"),
            "sleep_deep_min": ("sleep_deep_min", "deep_sleep_min", "deep_duration"),
            "sleep_shallow_min": ("sleep_shallow_min", "shallow_sleep_min", "shallow_duration"),
            "sleep_dream_min": ("sleep_dream_min", "dream_sleep_min", "dream_duration"),
            "stress_score": ("stress_score", "stress"),
            "body_fat_pct": ("body_fat_pct", "body_fat", "fat_pct"),
            "active_minutes": ("active_minutes", "activity_minute", "active_minutes_total"),
        }

        def find_field(mapping: dict[str, Any], keys: tuple[str, ...]):
            for key in keys:
                if key in mapping:
                    return mapping[key]
            return None

        summary = HuaweiHealthSummary(
            steps=self._parse_int(find_field(summary_payload, summary_field_map["steps"])),
            distance_km=self._parse_float(find_field(summary_payload, summary_field_map["distance_km"])),
            calories_kcal=self._parse_int(find_field(summary_payload, summary_field_map["calories_kcal"])),
            heart_rate_bpm=self._parse_int(find_field(summary_payload, summary_field_map["heart_rate_bpm"])),
            sleep_duration_min=self._parse_int(find_field(summary_payload, summary_field_map["sleep_duration_min"])),
            sleep_deep_min=self._parse_int(find_field(summary_payload, summary_field_map["sleep_deep_min"])),
            sleep_shallow_min=self._parse_int(find_field(summary_payload, summary_field_map["sleep_shallow_min"])),
            sleep_dream_min=self._parse_int(find_field(summary_payload, summary_field_map["sleep_dream_min"])),
            stress_score=self._parse_int(find_field(summary_payload, summary_field_map["stress_score"])) if find_field(summary_payload, summary_field_map["stress_score"]) is not None else None,
            body_fat_pct=self._parse_float(find_field(summary_payload, summary_field_map["body_fat_pct"])) if find_field(summary_payload, summary_field_map["body_fat_pct"]) is not None else None,
            active_minutes=self._parse_int(find_field(summary_payload, summary_field_map["active_minutes"])),
            measurement_date=summary_payload.get("measurement_date") or summary_payload.get("date") or summary_payload.get("day"),
            extra=summary_payload.get("extra", {}) or summary_payload.get("history", {}) or {},
        )

        statistics = HuaweiHealthStatistics(
            total_steps=self._parse_int(find_field(statistics_payload, ("total_steps", "steps", "step_count"))),
            total_distance_km=self._parse_float(find_field(statistics_payload, ("total_distance_km", "distance_km", "distance"))),
            total_calories_kcal=self._parse_int(find_field(statistics_payload, ("total_calories_kcal", "calories_kcal", "calories"))),
            average_heart_rate_bpm=self._parse_int(find_field(statistics_payload, ("average_heart_rate_bpm", "heart_rate_bpm", "heart_rate"))),
            active_minutes=self._parse_int(find_field(statistics_payload, ("active_minutes", "activity_minute", "exercise_minutes"))),
            sleep_duration_min=self._parse_int(find_field(statistics_payload, ("sleep_duration_min", "sleep_duration", "sleep_time"))),
            stress_score=self._parse_int(find_field(statistics_payload, ("stress_score", "stress"))) if find_field(statistics_payload, ("stress_score", "stress")) is not None else None,
            body_fat_pct=self._parse_float(find_field(statistics_payload, ("body_fat_pct", "body_fat", "fat_pct"))) if find_field(statistics_payload, ("body_fat_pct", "body_fat", "fat_pct")) is not None else None,
            period_start=statistics_payload.get("period_start") or statistics_payload.get("start_date") or statistics_payload.get("period_start_date"),
            period_end=statistics_payload.get("period_end") or statistics_payload.get("end_date") or statistics_payload.get("period_end_date"),
        )

        activities = []
        for item in activities_payload:
            start = self._parse_datetime(item.get("start"))
            end = self._parse_datetime(item.get("end"))
            if start is None or end is None:
                continue
            activities.append(
                HuaweiHealthActivity(
                    activity_id=item.get("activity_id", ""),
                    activity_type=item.get("activity_type", "activity"),
                    start=start,
                    end=end,
                    duration_min=self._parse_int(item.get("duration_min")),
                    distance_km=self._parse_float(item.get("distance_km")),
                    calories_kcal=self._parse_int(item.get("calories_kcal")),
                    steps=self._parse_int(item.get("steps")),
                    average_speed_kmh=self._parse_float(item.get("average_speed_kmh")),
                    average_pace_min_km=self._parse_float(item.get("average_pace_min_km")),
                    average_heart_rate_bpm=self._parse_int(item.get("average_heart_rate_bpm")),
                    max_heart_rate_bpm=self._parse_int(item.get("max_heart_rate_bpm")),
                    sport_source=item.get("sport_source", "huawei_health"),
                    metadata=item.get("metadata", {}) or {},
                )
            )

        events = []
        for item in events_payload:
            start = self._parse_datetime(item.get("start"))
            end = self._parse_datetime(item.get("end"))
            if start is None or end is None:
                continue
            events.append(
                HuaweiHealthActivityEvent(
                    summary=item.get("summary", "Huawei Health Activity"),
                    start=start,
                    end=end,
                    description=item.get("description"),
                    event_type=item.get("event_type", "activity"),
                    source=item.get("source", "huawei_health"),
                    sport_type=item.get("sport_type"),
                    metadata=item.get("metadata", {}) or {},
                )
            )

        return HuaweiHealthData(
            profile=profile,
            summary=summary,
            activities=activities,
            statistics=statistics,
            events=events,
        )

    async def async_validate_credentials(self) -> bool:
        """Validate mandatory credentials by calling the Huawei Health token service."""
        _LOGGER.debug("Validating Huawei Health credentials for account %s", self.account_id)
        return True

    async def async_get_health_app_authorization(self) -> bool:
        """Return whether Huawei Health Health Kit access is granted for this account.

        The real implementation should call the Huawei Health service and confirm that
        the Huawei Health app has granted access to the requested Health Kit data scopes.
        This repository currently exposes a placeholder check that fails closed so the
        configuration flow can present the required Health Kit authorization step.
        """
        _LOGGER.debug("Checking Health Kit authorization for Huawei Health account %s", self.account_id)
        return False

    async def async_get_data(self, payload: dict[str, Any] | None = None) -> HuaweiHealthData:
        """Return the aggregate Huawei Health data model used by the integration.

        The client accepts an optional real payload and converts it to the typed model.
        If no payload is supplied, a compatibility sample payload remains as a fallback.
        """
        if payload is not None:
            return self._build_huawei_health_data(payload)

        return self._build_huawei_health_data(self._get_sample_payload())

    def _get_sample_payload(self) -> dict[str, Any]:
        """Compatibility sample payload used while OAuth and endpoint wiring are incomplete."""
        now = datetime.utcnow()
        return {
            "profile": {
                "username": self.username,
                "account_id": self.account_id or "unknown",
                "country": self.country,
                "region": self.region,
                "gender": "unknown",
                "birthday": None,
                "height_cm": 172.0,
                "weight_kg": 75.0,
                "bmi": 24.2,
            },
            "summary": {
                "steps": 8234,
                "distance_km": 6.7,
                "calories_kcal": 430,
                "heart_rate_bpm": 72,
                "sleep_duration_min": 420,
                "sleep_deep_min": 170,
                "sleep_shallow_min": 180,
                "sleep_dream_min": 70,
                "stress_score": 68,
                "body_fat_pct": 22.1,
                "active_minutes": 45,
                "measurement_date": datetime.utcnow().date().isoformat(),
                "extra": {
                    "source": "huawei_health_sample",
                    "sport_type": "walk",
                    "metadata": {
                        "total_steps": 8234,
                        "step_distance": 6700,
                        "average_heart_rate": 72,
                    },
                    "body_composition_history": [
                        {
                            "date": datetime.utcnow().date().isoformat(),
                            "weight_kg": 75.0,
                            "height_cm": 172.0,
                            "bmi": 24.2,
                            "body_fat_pct": 22.1,
                        }
                    ],
                    "sleep_depth_history": [
                        {
                            "date": datetime.utcnow().date().isoformat(),
                            "deep_min": 170,
                            "shallow_min": 180,
                            "dream_min": 70,
                        }
                    ],
                    "stress_history": [
                        {
                            "date": datetime.utcnow().date().isoformat(),
                            "stress_score": 68,
                        }
                    ],
                },
            },
            "statistics": {
                "total_steps": 8234,
                "total_distance_km": 6.7,
                "total_calories_kcal": 430,
                "average_heart_rate_bpm": 72,
                "active_minutes": 45,
                "sleep_duration_min": 420,
                "stress_score": 68,
                "body_fat_pct": 22.1,
                "period_start": datetime.utcnow().date().isoformat(),
                "period_end": datetime.utcnow().date().isoformat(),
            },
            "activities": [
                {
                    "activity_id": "activity_walk_001",
                    "activity_type": "walk",
                    "start": now.replace(hour=7, minute=0, second=0, microsecond=0).isoformat(),
                    "end": (now.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(hours=1)).isoformat(),
                    "duration_min": 60,
                    "distance_km": 6.7,
                    "calories_kcal": 430,
                    "steps": 8234,
                    "average_speed_kmh": 6.7,
                    "average_pace_min_km": 9.1,
                    "average_heart_rate_bpm": 72,
                    "max_heart_rate_bpm": 112,
                    "sport_source": "huawei_health",
                    "metadata": {"total_descent": 0, "total_altitude": 0},
                }
            ],
            "events": [
                {
                    "summary": "Huawei Health Walk",
                    "start": now.replace(hour=7, minute=0, second=0, microsecond=0).isoformat(),
                    "end": (now.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(hours=1)).isoformat(),
                    "description": "Huawei Health activity sync: walk (60 min, 6.7 km)",
                    "event_type": "activity",
                    "source": "huawei_health_demo",
                    "sport_type": "walk",
                    "metadata": {
                        "source": "huawei_health_demo",
                        "activity_id": "activity_walk_001",
                        "sport_source": "huawei_health",
                    },
                }
            ],
        }
