"""Binary sensor platform for Mock Device."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN
from .entity import MockBaseEntity
from .models import ENTITY_SPECS


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    async_add_entities(MockBinarySensor(coordinator, entry, spec) for spec in ENTITY_SPECS if spec.platform == "binary_sensor")


class MockBinarySensor(MockBaseEntity, BinarySensorEntity):
    """Read-only generated binary sensor."""

    def __init__(self, coordinator, entry, spec):
        super().__init__(coordinator, entry, spec)
        self._attr_device_class = spec.device_class

    @property
    def is_on(self):
        return bool(self.coordinator.data.get(self.spec.key))
