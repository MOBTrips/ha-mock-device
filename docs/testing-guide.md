# Testing Guide

## Basic smoke test

1. Install Mock Device.
2. Add the integration from **Settings → Devices & services**.
3. Confirm these devices exist:
   - Synthetic Generator
   - Synthetic UPS
   - Synthetic Pool Pump
   - Synthetic HVAC Filter
   - Synthetic Water Filter
   - Synthetic Energy Meter
   - Synthetic Environment Station
   - Synthetic Fault Device
   - Mock QA Console
4. Confirm `sensor.mock_qa_console_tick` increments.
5. Confirm runtime and meter values increase over time.

## Accelerated time test

Set `number.mock_qa_console_speed_multiplier` to `60` to simulate roughly one minute per real second. Set it to `1440` for very fast date/service testing.

## Service-due test

1. Press `button.mock_qa_console_trigger_service_due`.
2. Confirm service-due binary sensors turn on.
3. Press `button.mock_qa_console_trigger_service_overdue`.
4. Confirm overdue/status entities change.
5. Press `button.mock_qa_console_reset_service_due`.
6. Confirm service-due states clear.

## Bad-data test

1. Press `button.mock_qa_console_force_bad_data`.
2. Confirm Synthetic Fault Device reports edge values.
3. Confirm consuming integrations handle unknown/unavailable/negative/spiky values safely.

## Persistence test

1. Let several counters increase.
2. Restart Home Assistant.
3. Confirm values resume from the prior persisted state instead of resetting.

## Diagnostics snapshot

Call the service:

```yaml
service: mock_device.export_state_snapshot
```

Then listen for the event:

```text
mock_device_state_snapshot
```

Home Assistant diagnostics for the config entry also includes the current generator state and values.
