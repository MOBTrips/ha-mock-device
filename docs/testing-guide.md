# Testing Guide

## Recommended HMM QA flow

1. Install Mock Device through HACS as a custom integration.
2. Add the Mock Device integration in Home Assistant.
3. Confirm the generic devices appear first: Runtime, Meter, Service, Environmental, Flow, Distance, Consumable, Calendar, Event, Binary, Enum, Fault, and QA Console.
4. Use `button.mock_qa_console_seed_known_state` to start from a predictable baseline.
5. Import or map test tasks to the generic entities.
6. Use `number.mock_qa_console_speed_multiplier` and `select.mock_qa_console_profile` to accelerate schedule behavior.
7. Use trigger/reset buttons to test due, overdue, bad data, cycle completion, runtime reset, meter reset, and service reset.
8. Call `mock_device.export_state_snapshot` when capturing a bug report.

## Coverage targets

Mock Device is intended to cover combinations of:

- timebases: seconds, minutes, hours, days, weeks, months, years
- state classes: measurement, total_increasing, no state class
- sensor patterns: cumulative, resetting/session, threshold, date/timestamp, enum/text, binary, stale, unavailable, unknown, negative, zero, spike
- units: s, min, h, d, %, W, kW, kWh, gal, L, ft³, gal/min, L/min, ft³/min, psi, Pa, °F, °C, ft, m, mi, km, cycles, count

## Profiles

- `normal`: predictable running/idling and gradual changes
- `intermittent`: shorter on/off windows
- `bad_data`: intentionally emits bad/fault states
- `fast_forward`: forces very fast simulated time
- `long_cycle`: longer runtime cycles
