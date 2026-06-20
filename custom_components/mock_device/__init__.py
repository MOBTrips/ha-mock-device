"""Mock Device integration.

This module owns setup, unload, coordinator lifecycle, and the optional state snapshot
service. Platform-specific entity classes live in their own files.
"""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DEFAULT_SCAN_INTERVAL_SECONDS, DOMAIN, EVENT_STATE_SNAPSHOT, PLATFORMS
from .store import MockDeviceStore, MockDataGenerator

_LOGGER = logging.getLogger(__name__)


MockDeviceConfigEntry = ConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: MockDeviceConfigEntry) -> bool:
    """Set up Mock Device from a config entry."""
    store = MockDeviceStore(hass)
    await store.async_load()
    generator = MockDataGenerator(store)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=_async_update_data(generator, store),
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL_SECONDS),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "store": store,
        "generator": generator,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_export_state_snapshot(call: ServiceCall) -> None:
        """Fire an event containing the current synthetic state snapshot.

        Home Assistant diagnostics also exposes this data, but the service is useful
        during live QA because it creates a timestamped event without requiring file
        access.
        """
        snapshot = {
            "entry_id": entry.entry_id,
            "state": store.state.to_json(),
            "values": generator.values,
        }
        hass.bus.async_fire(EVENT_STATE_SNAPSHOT, snapshot)

    if not hass.services.has_service(DOMAIN, "export_state_snapshot"):
        hass.services.async_register(DOMAIN, "export_state_snapshot", async_export_state_snapshot)

    return True


def _async_update_data(generator: MockDataGenerator, store: MockDeviceStore):
    async def _update_data():
        data = generator.update()
        # Persist after every update. The data is small and persistence is important
        # because this integration is specifically meant to test restart behavior.
        await store.async_save()
        return data
    return _update_data


async def async_unload_entry(hass: HomeAssistant, entry: MockDeviceConfigEntry) -> bool:
    """Unload Mock Device cleanly."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if not hass.data.get(DOMAIN):
            hass.services.async_remove(DOMAIN, "export_state_snapshot")
    return unload_ok
