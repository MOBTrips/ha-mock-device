# Mock Device for Home Assistant

Mock Device is a test-only Home Assistant custom integration that creates realistic synthetic devices with generated data. It is intended for validating Home Assistant integrations, dashboards, automations, maintenance systems, and edge-case handling without creating manual helpers or needing real hardware.

The initial design was created to support Home Maintenance Manager QA, but the integration is intentionally generic and can be reused by any Home Assistant project.

## What it creates

Mock Device creates multiple synthetic devices, including:

- Synthetic Generator
- Synthetic UPS
- Synthetic Pool Pump
- Synthetic HVAC Filter
- Synthetic Water Filter
- Synthetic Energy Meter
- Synthetic Environment Station
- Synthetic Calendar Device
- Synthetic NFC Device
- Synthetic Fault Device
- Mock QA Console

These devices expose read-only sensors and binary sensors for runtime, meters, service-due states, maintenance history, environmental values, date/time values, and bad-data behavior. The QA Console exposes controls for reset, acceleration, profile selection, and fault injection.

## Key features

- No external account or hardware
- No manually created helpers
- Stable entity IDs for repeatable testing
- Accelerated simulated time
- Persistent synthetic state across Home Assistant restarts
- Service-due and overdue simulation
- Maintenance history simulation
- Automatic and manual fault injection
- Diagnostics export support
- Clean unload and clean uninstall behavior
- HACS custom repository ready

## Installation

### HACS custom repository

1. Add this repository to HACS as a custom repository.
2. Choose category **Integration**.
3. Install **Mock Device**.
4. Restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration**.
6. Search for **Mock Device**.
7. Add it. No credentials are required.

### Manual installation

Copy this folder into your Home Assistant config directory:

```text
custom_components/mock_device
```

Then restart Home Assistant and add the integration from the UI.

## Entity naming

Entity IDs are designed to be stable for QA task packs and automated tests. Example:

```text
sensor.synthetic_generator_runtime_hours
binary_sensor.synthetic_generator_service_due
button.mock_qa_console_reset_all
number.mock_qa_console_speed_multiplier
select.mock_qa_console_profile
```

For v0.1.0, the integration is designed for a single config entry. Duplicate setup is intentionally blocked to avoid duplicate entity suffixes.

## Documentation

- [Entity catalog](docs/entity-catalog.md)
- [Testing guide](docs/testing-guide.md)
- [Uninstall guide](docs/uninstall.md)
- [Developer notes](docs/developer-notes.md)

## Important warning

This integration generates fake data. Do not use it for real monitoring, real alerts, safety decisions, equipment control, or production maintenance decisions.
