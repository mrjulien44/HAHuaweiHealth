"""Real data model for the Huawei Health integration.

This file mirrors the categories shown by the Huawei Health sample demo:
- account/profile data
- health point summaries (steps, calories, distance, heart rate)
- sleep and stress records
- body composition data (height, weight, BMI)
- exercise and sport session events for the calendar
- statistics and activity records that can be exposed as sensors or services
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class HuaweiHealthProfile:
    """Huawei Health account profile metadata."""

    username: str
    account_id: str
    country: str
    region: str
    gender: str | None = None
    birthday: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    bmi: float | None = None


@dataclass(slots=True)
class HuaweiHealthActivity:
    """A single activity/sport record from Huawei Health."""

    activity_id: str
    activity_type: str
    start: datetime
    end: datetime
    duration_min: int
    distance_km: float | None = None
    calories_kcal: float | None = None
    steps: int | None = None
    average_speed_kmh: float | None = None
    average_pace_min_km: float | None = None
    average_heart_rate_bpm: int | None = None
    max_heart_rate_bpm: int | None = None
    sport_source: str = "huawei_health"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HuaweiHealthStatistics:
    """Statistics object that summarizes activity and medical metrics."""

    total_steps: int = 0
    total_distance_km: float = 0.0
    total_calories_kcal: float = 0.0
    average_heart_rate_bpm: int = 0
    active_minutes: int = 0
    sleep_duration_min: int = 0
    stress_score: int | None = None
    body_fat_pct: float | None = None
    period_start: str | None = None
    period_end: str | None = None


@dataclass(slots=True)
class HuaweiHealthSummary:
    """Daily or most-recent health summary."""

    steps: int = 0
    distance_km: float = 0.0
    calories_kcal: float = 0.0
    heart_rate_bpm: int = 0
    sleep_duration_min: int = 0
    sleep_deep_min: int = 0
    sleep_shallow_min: int = 0
    sleep_dream_min: int = 0
    stress_score: int | None = None
    body_fat_pct: float | None = None
    active_minutes: int = 0
    measurement_date: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HuaweiHealthActivityEvent:
    """Huawei Health activity or workout event for the calendar model."""

    summary: str
    start: datetime
    end: datetime
    description: str | None = None
    event_type: str = "activity"
    source: str = "huawei_health"
    sport_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class HuaweiHealthData:
    """Aggregate model returned by the Huawei Health client."""

    profile: HuaweiHealthProfile
    summary: HuaweiHealthSummary
    activities: list[HuaweiHealthActivity] = field(default_factory=list)
    statistics: HuaweiHealthStatistics = field(default_factory=HuaweiHealthStatistics)
    events: list[HuaweiHealthActivityEvent] = field(default_factory=list)
