"""Button platform for Mock Device QA controls."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity

from .const import DOMAIN
from .entity import MockBaseEntity
from .models import ENTITY_SPECS


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    generator = data["generator"]
    store = data["store"]
    async_add_entities(MockButton(coordinator, entry, spec, generator, store) for spec in ENTITY_SPECS if spec.platform == "button")


class MockButton(MockBaseEntity, ButtonEntity):
    """Button that changes generator state for QA."""

    def __init__(self, coordinator, entry, spec, generator, store):
        super().__init__(coordinator, entry, spec)
        self.generator = generator
        self.store = store

    async def async_press(self) -> None:
        key = self.spec.key
        if key.endswith("reset_all"):
            await self.store.async_reset_all()
        elif key.endswith("reset_runtime"):
            await self.generator.reset_runtime()
        elif key.endswith("reset_meters"):
            await self.generator.reset_meters()
        elif key.endswith("reset_service_due"):
            await self.generator.reset_service_due()
        elif key.endswith("trigger_service_due"):
            await self.generator.trigger_service_due(False)
        elif key.endswith("trigger_service_overdue"):
            await self.generator.trigger_service_due(True)
        elif key.endswith("force_bad_data"):
            await self.generator.force_bad_data()
        elif key.endswith("force_cycle"):
            await self.generator.force_cycle()
        elif key.endswith("seed_known_state"):
            await self.generator.seed_known_state()
        await self.coordinator.async_request_refresh()
