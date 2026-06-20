"""Diagnostics support for Mock Device."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry):
    """Return a snapshot useful for QA bug reports."""
    data = hass.data[DOMAIN][entry.entry_id]
    return {
        "integration": "mock_device",
        "entry_title": entry.title,
        "state": data["store"].state.to_json(),
        "values": data["generator"].values,
    }
