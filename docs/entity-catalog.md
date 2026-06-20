# Entity Catalog

Mock Device v0.1.0 creates about 100 entities across multiple synthetic devices. Entity IDs are intentionally stable so automated tests and importable task packs can map to them repeatedly.

## Mock QA Console

Controls generated data and QA scenarios.

| Entity | Type | Purpose |
|---|---|---|
| `select.mock_qa_console_profile` | select | normal, intermittent, bad_data, fast_forward, long_cycle |
| `number.mock_qa_console_speed_multiplier` | number | Accelerates simulated time from 1x to 1440x |
| `switch.mock_qa_console_automatic_faults` | switch | Enables periodic automatic fault windows |
| `button.mock_qa_console_reset_all` | button | Reset all persisted synthetic values |
| `button.mock_qa_console_reset_runtime` | button | Reset runtime counters |
| `button.mock_qa_console_reset_meters` | button | Reset meter/counter values |
| `button.mock_qa_console_reset_service_due` | button | Clear forced service-due state |
| `button.mock_qa_console_trigger_service_due` | button | Force service due |
| `button.mock_qa_console_trigger_service_overdue` | button | Force overdue state |
| `button.mock_qa_console_force_bad_data` | button | Trigger temporary bad data |
| `button.mock_qa_console_force_cycle` | button | Add one generated run cycle |
| `button.mock_qa_console_seed_known_state` | button | Set a predictable baseline |

## Synthetic Generator

Tests runtime schedules, cumulative counters, service due, power, energy, and maintenance history.

Key entities:

- `binary_sensor.synthetic_generator_running`
- `sensor.synthetic_generator_runtime_seconds`
- `sensor.synthetic_generator_runtime_minutes`
- `sensor.synthetic_generator_runtime_hours`
- `sensor.synthetic_generator_session_runtime_minutes`
- `sensor.synthetic_generator_cycle_count`
- `sensor.synthetic_generator_power`
- `sensor.synthetic_generator_energy`
- `binary_sensor.synthetic_generator_service_due`
- `sensor.synthetic_generator_service_status`
- `sensor.synthetic_generator_service_remaining_hours`
- `sensor.synthetic_generator_service_due_date`

## Other synthetic devices

- Synthetic UPS: battery, load, runtime remaining, replacement due, self-test status.
- Synthetic Pool Pump: runtime, power, energy, flow, pressure, filter service.
- Synthetic HVAC Filter: life remaining, used percent, airflow, pressure drop, service due.
- Synthetic Water Filter: gallons used, gallons/liters remaining, service due.
- Synthetic Energy Meter: W, kW, total kWh, session kWh, resetting counters, total cycles.
- Synthetic Environment Station: temperature F/C, humidity, pressure Pa/psi, distance ft/m.
- Synthetic Calendar Device: last completed, next due, due today, overdue.
- Synthetic NFC Device: tag present, last scan, scan count.
- Synthetic Fault Device: unknown, unavailable, negative duration, spiky power, unit-change value, error status.

## Common metadata entities

Most synthetic equipment devices also expose:

- firmware version
- hardware revision
- serial number
- last service date
- service count
- service reason
