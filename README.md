# Mock Device

Mock Device is a Home Assistant custom integration that creates generated synthetic devices and sensor data for QA, regression testing, and integration development.

It is intentionally **integration agnostic**. It can be used to test Home Maintenance Manager, dashboards, automations, template sensors, history/statistics behavior, import wizards, and other integrations that need predictable Home Assistant entities.

## v0.1.1 highlights

- 20 generated devices
- 260 generated entities
- Generic QA devices such as `Mock Runtime Device`, `Mock Meter Device`, and `Mock Service Device`
- Equipment-style demo devices such as `Synthetic Generator`, `Synthetic UPS`, and `Synthetic Pool Pump`
- Accelerated simulated time with a configurable speed multiplier
- Persistent generated state across Home Assistant restarts
- Service-due, remaining-life, due-date, and maintenance-history entities
- Automatic and manual fault injection
- Reset/trigger controls through the `Mock QA Console`
- Diagnostics snapshot service: `mock_device.export_state_snapshot`
- Clean unload/uninstall behavior with no helper entities, YAML, automations, or writes to other integrations

## Install with HACS custom repository

1. HACS → Integrations → three-dot menu → Custom repositories.
2. Repository: `MOBTrips/ha-mock-device`.
3. Category: **Integration**.
4. Add and install **Mock Device**.
5. Restart Home Assistant.
6. Settings → Devices & services → Add integration → **Mock Device**.

## Devices created

| Device | Entity count | Purpose |
|---|---:|---|
| Mock QA Console | 14 | Generated QA coverage |
| Mock Runtime Device | 18 | Generated QA coverage |
| Mock Meter Device | 16 | Generated QA coverage |
| Mock Service Device | 19 | Generated QA coverage |
| Mock Environmental Device | 14 | Generated QA coverage |
| Mock Flow Device | 13 | Generated QA coverage |
| Mock Distance Device | 11 | Generated QA coverage |
| Mock Consumable Device | 12 | Generated QA coverage |
| Mock Calendar Device | 12 | Generated QA coverage |
| Mock Event Device | 11 | Generated QA coverage |
| Mock Binary Device | 12 | Generated QA coverage |
| Mock Enum Status Device | 10 | Generated QA coverage |
| Mock Fault Device | 14 | Generated QA coverage |
| Synthetic Generator | 15 | Generated QA coverage |
| Synthetic UPS | 13 | Generated QA coverage |
| Synthetic Pool Pump | 15 | Generated QA coverage |
| Synthetic HVAC Filter | 11 | Generated QA coverage |
| Synthetic Water Filter | 10 | Generated QA coverage |
| Synthetic Energy Meter | 10 | Generated QA coverage |
| Synthetic Environment Station | 10 | Generated QA coverage |

## Platform count

| Platform | Count |
|---|---:|
| `select` | 1 |
| `number` | 1 |
| `switch` | 1 |
| `button` | 9 |
| `sensor` | 224 |
| `binary_sensor` | 24 |

## QA Console controls

The integration keeps normal test entities read-only. The `Mock QA Console` exposes a small set of controls:

- `button.mock_qa_console_reset_all`
- `button.mock_qa_console_reset_runtime`
- `button.mock_qa_console_reset_meters`
- `button.mock_qa_console_reset_service_due`
- `button.mock_qa_console_trigger_service_due`
- `button.mock_qa_console_trigger_service_overdue`
- `button.mock_qa_console_force_bad_data`
- `button.mock_qa_console_force_cycle`
- `button.mock_qa_console_seed_known_state`
- `select.mock_qa_console_profile`
- `number.mock_qa_console_speed_multiplier`
- `switch.mock_qa_console_automatic_faults`

## Simulated time

`number.mock_qa_console_speed_multiplier` controls accelerated time. The default is `60x`, meaning one real minute behaves like one simulated hour. The `fast_forward` profile forces at least `1440x`, useful when testing day/month/year logic.

## Uninstall behavior

Mock Device does not create Home Assistant helpers, automations, dashboards, or HMM data. Removing the integration entry unloads platforms and removes the integration service. Entity/device registry cleanup follows normal Home Assistant config-entry removal behavior.

## Documentation

- [Entity catalog](docs/entity-catalog.md)
- [Testing guide](docs/testing-guide.md)
- [Developer notes](docs/developer-notes.md)
- [Uninstall guide](docs/uninstall.md)
