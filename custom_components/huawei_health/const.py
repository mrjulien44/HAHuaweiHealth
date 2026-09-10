"""Constants for the Huawei Health custom component."""

DOMAIN = "huawei_health"
PLATFORMS = ["sensor", "calendar"]

DEFAULT_NAME = "Huawei Health"
DEFAULT_REGION = "global"
DEFAULT_BASE_URL = "https://openapi.huawei.com"

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_REGION = "region"
CONF_COUNTRY = "country"
CONF_ACCESS_TOKEN = "access_token"
CONF_REFRESH_TOKEN = "refresh_token"
CONF_ACCOUNT_ID = "account_id"

API_TIMEOUT = 30
SCAN_INTERVAL = 300

SENSOR_TYPES = {
    "steps": {
        "key": "steps",
        "name": "Steps",
        "unit": "steps",
        "icon": "mdi:shoe-print",
    },
    "distance": {
        "key": "distance",
        "name": "Distance",
        "unit": "km",
        "icon": "mdi:map-marker-distance",
    },
    "calories": {
        "key": "calories",
        "name": "Calories",
        "unit": "kcal",
        "icon": "mdi:fire",
    },
    "heart_rate": {
        "key": "heart_rate",
        "name": "Heart Rate",
        "unit": "bpm",
        "icon": "mdi:heart-pulse",
    },
    "sleep_duration": {
        "key": "sleep_duration",
        "name": "Sleep Duration",
        "unit": "min",
        "icon": "mdi:bed",
    },
    "weight": {
        "key": "weight",
        "name": "Weight",
        "unit": "kg",
        "icon": "mdi:scale-bathroom",
    },
    "height": {
        "key": "height",
        "name": "Height",
        "unit": "cm",
        "icon": "mdi:ruler",
    },
    "bmi": {
        "key": "bmi",
        "name": "BMI",
        "unit": "kg/m²",
        "icon": "mdi:body",
    },
    "sleep_deep": {
        "key": "sleep_deep",
        "name": "Sleep Deep",
        "unit": "min",
        "icon": "mdi:moon-waning-crescent",
    },
    "sleep_shallow": {
        "key": "sleep_shallow",
        "name": "Sleep Shallow",
        "unit": "min",
        "icon": "mdi:moon-last-quarter",
    },
    "sleep_dream": {
        "key": "sleep_dream",
        "name": "Sleep Dream",
        "unit": "min",
        "icon": "mdi:weather-night",
    },
    "stress_score": {
        "key": "stress_score",
        "name": "Stress Score",
        "unit": "score",
        "icon": "mdi:heart-broken",
    },
    "body_fat_pct": {
        "key": "body_fat_pct",
        "name": "Body Fat",
        "unit": "%",
        "icon": "mdi:human",
    },
}
