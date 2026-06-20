# Uninstall Guide

Mock Device is designed for clean removal.

## Normal uninstall

1. Go to **Settings → Devices & services**.
2. Open **Mock Device**.
3. Delete the integration entry.
4. Restart Home Assistant if HACS or HA asks you to.
5. Remove the custom repository from HACS if desired.

## What should be removed

- All Mock Device entities
- All synthetic devices
- Update coordinator/timer listeners
- The `mock_device.export_state_snapshot` service

## What is intentionally not created

Mock Device does not create:

- helpers
- automations
- scripts
- Home Maintenance Manager data
- YAML packages
- external files outside normal Home Assistant integration storage

## Persistent storage note

The integration uses Home Assistant's normal storage helper to persist generated state. Removing the integration entry removes the active devices/entities. Home Assistant may retain historical entity registry/statistics records according to normal HA behavior.
