# HAHuaweiHealth

![Validation](https://github.com/mrjulien44/HAHuaweiHealth/actions/workflows/validate.yml/badge.svg)
![Hassfest](https://github.com/mrjulien44/HAHuaweiHealth/actions/workflows/validate.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/mrjulien44/HAHuaweiHealth)

Huawei Health integration for Home Assistant, designed to be installable through HACS.

> HACS-ready custom integration repository for Huawei Health. Install via the HACS store and add the integration from the Home Assistant UI.
> Repository: https://github.com/mrjulien44/HAHuaweiHealth
> HACS install shortcut: https://my.home-assistant.io/redirect/hacs_repository/?repository=mrjulien44/HAHuaweiHealth&category=integration

> For a code coverage badge, the repository is prepared for Codecov integration.

> Important: before using the integration, open the Huawei Health application and allow Health Kit access for the health data categories you want to synchronize. Without the Huawei Health app authorization, the integration cannot read the requested records.

This custom integration is built to work on Home Assistant and exposes a dedicated
calendar entity named `Huawei Health` for synchronized activity events.

Before using the integration, open the Huawei Health application and allow Health Kit
access for the data categories you want to synchronize. Without that Huawei Health
application authorization, the integration cannot read the health profile, activity,
body-composition, sleep, or stress records.

## Purpose

This repository contains a Home Assistant custom integration named `huawei_health`.
It is designed to collect user health information from Huawei Health APIs and expose
that data as Home Assistant sensors, a calendar entity, and typed model objects for
activities, statistics, and profile information.

## HACS installation

This repository is intended to be used as a custom repository in HACS:

You can install it with one click from the Home Assistant UI via My Home Assistant:

https://my.home-assistant.io/redirect/hacs_repository/?repository=mrjulien44/HAHuaweiHealth&category=integration


1. Add this repository to HACS as a custom integration repository.
2. Install the `Huawei Health` integration from the HACS store.
3. Restart Home Assistant.
4. Add the integration from Settings → Devices & Services → Add Integration.
5. Provide the mandatory account credentials in the config flow:
   - username
   - password
   - country
   - region
   - account_id

## Repository structure

The integration must live in the standard Home Assistant custom-component location:

```text
custom_components/
  huawei_health/
    __init__.py
    api.py
    calendar.py
    config_flow.py
    const.py
    manifest.json
    models.py
    sensor.py
    strings.json
    translations/en.json
```

The repository itself also needs the HACS metadata file at the root:

```text
hacs.json
```

## Mandatory configuration

The config flow requires the following fields:

- username
- password
- country
- region
- account_id

These are the mandatory configuration values needed to authenticate and identify the
Huawei Health account.

## Implementation notes

The scaffold currently ships a typed model in `models.py` and a placeholder adapter in `api.py`.
The next milestone is to replace the placeholder data extraction with real Huawei Health
API endpoints and the required OAuth2 token handling.

## Suggested Home Assistant Platform Mapping

- `sensor`: health values such as steps, distance, calories, heart rate, sleep,
  stress, body fat, and active minutes
- `calendar`: workouts and health events
- `statistics` and `activities` modeled in the internal `HuaweiHealthData` object
- Additional sensors can be added for weight, height, BMI, sleep depth,
  stress and body composition history

## Development

To load this integration locally:

1. Copy the `custom_components/huawei_health` folder into your Home Assistant
   `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration from the UI and provide the required account information.
