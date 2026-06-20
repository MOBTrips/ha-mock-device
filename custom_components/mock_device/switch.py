"""Switch platform for Mock Device QA controls."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entity import MockBaseEntity
from .models import ENTITY_SPECS


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    store = data["store"]
    async_add_entities(MockSwitch(coordinator, entry, spec, store) for spec in ENTITY_SPECS if spec.platform == "switch")


class MockSwitch(MockBaseEntity, SwitchEntity):
    """Switch used for enabling/disabling automatic fault windows."""

    def __init__(self, coordinator, entry, spec, store):
        super().__init__(coordinator, entry, spec)
        self.store = store

    @property
    def is_on(self):
        return self.store.state.automatic_faults

    async def async_turn_on(self, **kwargs) -> None:
        self.store.state.automatic_faults = True
        await self.store.async_save()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        self.store.state.automatic_faults = False
        await self.store.async_save()
        await self.coordinator.async_request_refresh()
