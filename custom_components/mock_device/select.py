"""Select platform for Mock Device QA controls."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity

from .const import DOMAIN, PROFILES
from .entity import MockBaseEntity
from .models import ENTITY_SPECS


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    store = data["store"]
    async_add_entities(MockSelect(coordinator, entry, spec, store) for spec in ENTITY_SPECS if spec.platform == "select")


class MockSelect(MockBaseEntity, SelectEntity):
    """Profile selector for generated data patterns."""

    def __init__(self, coordinator, entry, spec, store):
        super().__init__(coordinator, entry, spec)
        self.store = store
        self._attr_options = list(spec.options or PROFILES)

    @property
    def current_option(self):
        return self.store.state.profile

    async def async_select_option(self, option: str) -> None:
        if option not in self.options:
            return
        self.store.state.profile = option
        await self.store.async_save()
        await self.coordinator.async_request_refresh()
