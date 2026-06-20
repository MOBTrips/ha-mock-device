# Uninstall Guide

1. Settings → Devices & services → Mock Device.
2. Delete the Mock Device config entry.
3. Restart Home Assistant if HACS asks you to.
4. Remove the custom repository from HACS if desired.

Mock Device does not create helpers, automations, dashboards, or HMM storage records. Any remaining disabled/stale entity registry entries can be removed through Home Assistant's normal entity cleanup tools.
