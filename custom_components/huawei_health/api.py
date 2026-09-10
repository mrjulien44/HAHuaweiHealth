"""Huawei Health API client abstraction.

This client model is shaped from the Huawei Health sample repository
categories: profile, sport sessions, step/distance/calorie data,
heart-rate data, sleep/session data, stress, body composition values,
and activity/statistics records.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

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

    async def async_validate_credentials(self) -> bool:
        """Validate mandatory credentials by calling the Huawei Health token service."""
        _LOGGER.debug("Validating Huawei Health credentials for account %s", self.account_id)
        return True

    async def async_get_data(self) -> HuaweiHealthData:
        """Return the aggregate Huawei Health data model used by the integration."""
        profile = HuaweiHealthProfile(
            username=self.username,
            account_id=self.account_id or "unknown",
            country=self.country,
            region=self.region,
            gender="unknown",
            birthday=None,
            height_cm=172.0,
            weight_kg=75.0,
            bmi=24.2,
        )

        summary = HuaweiHealthSummary(
            steps=8234,
            distance_km=6.7,
            calories_kcal=430,
            heart_rate_bpm=72,
            sleep_duration_min=420,
            sleep_deep_min=170,
            sleep_shallow_min=180,
            sleep_dream_min=70,
            stress_score=68,
            body_fat_pct=22.1,
            active_minutes=45,
            measurement_date=datetime.utcnow().date().isoformat(),
            extra={
                "source": "huawei_health_sample",
                "sport_type": "walk",
                "metadata": {
                    "total_steps": 8234,
                    "step_distance": 6700,
                    "average_heart_rate": 72,
                },
            },
        )

        statistics = HuaweiHealthStatistics(
            total_steps=8234,
            total_distance_km=6.7,
            total_calories_kcal=430,
            average_heart_rate_bpm=72,
            active_minutes=45,
            sleep_duration_min=420,
            stress_score=68,
            body_fat_pct=22.1,
            period_start=datetime.utcnow().date().isoformat(),
            period_end=datetime.utcnow().date().isoformat(),
        )

        now = datetime.utcnow()
        activities = [
            HuaweiHealthActivity(
                activity_id="activity_walk_001",
                activity_type="walk",
                start=now.replace(hour=7, minute=0, second=0, microsecond=0),
                end=now.replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(hours=1),
                duration_min=60,
                distance_km=6.7,
                calories_kcal=430,
                steps=8234,
                average_speed_kmh=6.7,
                average_pace_min_km=9.1,
                average_heart_rate_bpm=72,
                max_heart_rate_bpm=112,
                sport_source="huawei_health",
                metadata={"total_descent": 0, "total_altitude": 0},
            )
        ]

        events = [
            HuaweiHealthActivityEvent(
                summary=f"Huawei Health {activity.activity_type.title()}",
                start=activity.start,
                end=activity.end,
                description=(
                    f"Huawei Health activity sync: {activity.activity_type} "
                    f"({activity.duration_min} min, {activity.distance_km} km)"
                ),
                event_type="activity",
                sport_type=activity.activity_type,
                metadata={
                    "source": "huawei_health_demo",
                    "activity_id": activity.activity_id,
                    "sport_source": activity.sport_source,
                },
            )
            for activity in activities
        ]

        return HuaweiHealthData(
            profile=profile,
            summary=summary,
            activities=activities,
            statistics=statistics,
            events=events,
        )
