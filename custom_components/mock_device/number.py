"""Number platform for Mock Device QA controls."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity

from .const import DOMAIN
from .entity import MockBaseEntity
from .models import ENTITY_SPECS


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    store = data["store"]
    async_add_entities(MockNumber(coordinator, entry, spec, store) for spec in ENTITY_SPECS if spec.platform == "number")


class MockNumber(MockBaseEntity, NumberEntity):
    """Writable number used to control generator behavior."""

    def __init__(self, coordinator, entry, spec, store):
        super().__init__(coordinator, entry, spec)
        self.store = store
        self._attr_native_min_value = spec.native_min_value
        self._attr_native_max_value = spec.native_max_value
        self._attr_native_step = spec.native_step
        self._attr_native_unit_of_measurement = spec.unit

    @property
    def native_value(self):
        return self.store.state.speed_multiplier

    async def async_set_native_value(self, value: float) -> None:
        self.store.state.speed_multiplier = float(value)
        await self.store.async_save()
        await self.coordinator.async_request_refresh()
