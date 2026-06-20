"""Base entity helpers for Mock Device."""

from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .models import DEVICES, EntitySpec

DEVICE_BY_KEY = {d.key: d for d in DEVICES}


class MockBaseEntity(CoordinatorEntity):
    """Shared behavior for all generated entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, spec: EntitySpec):
        super().__init__(coordinator)
        self.entry = entry
        self.spec = spec
        device = DEVICE_BY_KEY[spec.device_key]
        self._attr_unique_id = f"{DOMAIN}_{spec.key}"
        self._attr_name = spec.name
        self._attr_icon = spec.icon
        if spec.entity_category:
            self._attr_entity_category = spec.entity_category
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.key)},
            name=device.name,
            manufacturer=device.manufacturer,
            model=device.model,
            sw_version=device.sw_version,
            hw_version=device.hw_version,
        )

    @property
    def available(self) -> bool:
        # The dedicated unavailable test entity intentionally reports unavailable
        # by returning None from the data generator.
        if self.spec.key == "synthetic_fault_unavailable_state":
            return self.coordinator.data.get(self.spec.key) is not None
        return super().available
