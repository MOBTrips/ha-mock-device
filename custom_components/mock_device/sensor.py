"""Sensor platform for Mock Device."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN
from .entity import MockBaseEntity
from .models import ENTITY_SPECS


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    async_add_entities(MockSensor(coordinator, entry, spec) for spec in ENTITY_SPECS if spec.platform == "sensor")


class MockSensor(MockBaseEntity, SensorEntity):
    """Read-only generated sensor."""

    def __init__(self, coordinator, entry, spec):
        super().__init__(coordinator, entry, spec)
        self._attr_native_unit_of_measurement = spec.unit
        self._attr_device_class = spec.device_class
        self._attr_state_class = spec.state_class

    @property
    def native_value(self):
        return self.coordinator.data.get(self.spec.key)
