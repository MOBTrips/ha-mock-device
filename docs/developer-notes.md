# Developer Notes

## Architecture

Mock Device is intentionally data-driven:

- `models.py` defines synthetic devices and entity specs.
- `store.py` owns persisted runtime state and deterministic value generation.
- platform files (`sensor.py`, `binary_sensor.py`, `button.py`, `number.py`, `select.py`, `switch.py`) expose Home Assistant entities.
- `diagnostics.py` exports snapshots for bug reports.

To add a new read-only entity, add an `EntitySpec` in `models.py` and a value in `MockDataGenerator.update()`.

## Stability rules

Stable entity IDs are a core requirement. Avoid changing existing `EntitySpec.key` values after release unless a migration plan is added.

## Single instance rule

v0.1.0 intentionally supports one config entry. This avoids Home Assistant suffixes such as `_2`, which would break repeatable QA task packs.

## Persistence

Generated counters persist via `homeassistant.helpers.storage.Store`. This is intentional because many integrations need to validate restart/restore behavior.

## Fault generation

Faults can be both automatic and manual:

- automatic faults are enabled/disabled with the QA Console switch
- manual faults are triggered with `button.mock_qa_console_force_bad_data`

## Clean unload

`async_unload_entry` unloads all platforms and removes the snapshot service when the last entry is unloaded.
