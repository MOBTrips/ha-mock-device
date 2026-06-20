"""Persistent state and deterministic data generator for Mock Device.

The generator is deliberately deterministic. Given the same persisted state, speed
multiplier, profile, and elapsed real time, testers should see predictable changes.
This makes it useful for repeatable release testing and bug reproduction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import math
from typing import Any

from homeassistant.helpers.storage import Store

from .const import DEFAULT_SPEED_MULTIPLIER, PROFILE_NORMAL

STORE_VERSION = 1
STORE_KEY = "mock_device_state"


def utcnow() -> datetime:
    """Return timezone-aware UTC now."""
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


@dataclass
class MockRuntimeState:
    """Mutable generator state persisted across Home Assistant restarts."""

    profile: str = PROFILE_NORMAL
    speed_multiplier: float = DEFAULT_SPEED_MULTIPLIER
    automatic_faults: bool = True
    simulated_time: datetime = field(default_factory=utcnow)
    last_update: datetime = field(default_factory=utcnow)
    tick: int = 0
    manual_bad_data_until_tick: int = 0
    forced_service_state: str | None = None

    runtime_seconds: float = 0.0
    pool_runtime_seconds: float = 0.0
    generator_cycles: int = 0
    pool_cycles: int = 0
    total_kwh: float = 0.0
    pool_kwh: float = 0.0
    energy_meter_kwh: float = 0.0
    energy_session_kwh: float = 0.0
    water_gallons_used: float = 0.0
    nfc_scan_count: int = 0
    service_count: int = 0

    def to_json(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["simulated_time"] = iso(self.simulated_time)
        data["last_update"] = iso(self.last_update)
        return data

    @classmethod
    def from_json(cls, data: dict[str, Any] | None) -> "MockRuntimeState":
        if not data:
            return cls()
        copied = dict(data)
        for key in ("simulated_time", "last_update"):
            if isinstance(copied.get(key), str):
                copied[key] = datetime.fromisoformat(copied[key])
        return cls(**{k: v for k, v in copied.items() if k in cls.__dataclass_fields__})


class MockDeviceStore:
    """Small wrapper around Home Assistant Store."""

    def __init__(self, hass):
        self._store = Store(hass, STORE_VERSION, STORE_KEY)
        self.state = MockRuntimeState()

    async def async_load(self) -> None:
        self.state = MockRuntimeState.from_json(await self._store.async_load())
        self.state.last_update = utcnow()

    async def async_save(self) -> None:
        await self._store.async_save(self.state.to_json())

    async def async_reset_all(self) -> None:
        self.state = MockRuntimeState(profile=self.state.profile, speed_multiplier=self.state.speed_multiplier, automatic_faults=self.state.automatic_faults)
        await self.async_save()


class MockDataGenerator:
    """Produces entity states from persisted generator state."""

    def __init__(self, store: MockDeviceStore):
        self.store = store
        self.values: dict[str, Any] = {}

    def update(self) -> dict[str, Any]:
        """Advance simulated time and calculate all entity values."""
        state = self.store.state
        now = utcnow()
        real_seconds = max(0.0, (now - state.last_update).total_seconds())
        state.last_update = now
        multiplier = state.speed_multiplier
        if state.profile == "fast_forward":
            multiplier = max(multiplier, 1440.0)
        elif state.profile == "long_cycle":
            multiplier = max(multiplier, 10.0)
        sim_seconds = real_seconds * multiplier
        state.simulated_time += timedelta(seconds=sim_seconds)
        state.tick += 1

        t = state.simulated_time.timestamp()
        hour_cycle = int(t // 3600)
        minute_cycle = int(t // 60)

        intermittent = state.profile == "intermittent"
        generator_running = (minute_cycle % (6 if intermittent else 10)) < (3 if intermittent else 7)
        pool_running = (minute_cycle % 12) < 8
        if state.profile == "long_cycle":
            generator_running = (hour_cycle % 8) < 6
            pool_running = (hour_cycle % 6) < 4

        if generator_running:
            state.runtime_seconds += sim_seconds
            state.total_kwh += sim_seconds / 3600 * 2.4
        if pool_running:
            state.pool_runtime_seconds += sim_seconds
            state.pool_kwh += sim_seconds / 3600 * 1.15
            state.water_gallons_used += sim_seconds / 60 * 42
        state.energy_meter_kwh += sim_seconds / 3600 * 0.85
        state.energy_session_kwh = (minute_cycle % 30) * 0.05
        state.generator_cycles = int(state.runtime_seconds // (45 * 60))
        state.pool_cycles = int(state.pool_runtime_seconds // (60 * 60))
        state.nfc_scan_count = int(state.tick // 20)

        service_remaining_hours = max(0, 100 - state.runtime_seconds / 3600)
        service_due = service_remaining_hours <= 0 or state.forced_service_state in ("due", "overdue")
        service_status = "overdue" if state.forced_service_state == "overdue" else ("due" if service_due else "ok")
        hvac_life = max(0, 100 - (state.tick % 500) / 5)
        water_remaining = max(0, 10000 - state.water_gallons_used)
        bad_window = state.profile == "bad_data" or state.tick < state.manual_bad_data_until_tick
        automatic_fault_window = state.automatic_faults and (state.tick % 40 in (0, 1))

        temp_c = 20 + 5 * math.sin(t / 1800)
        temp_f = temp_c * 9 / 5 + 32
        power = 2400 + 250 * math.sin(t / 120) if generator_running else 0
        pool_power = 1150 + 180 * math.sin(t / 90) if pool_running else 0

        due_date = state.simulated_time + timedelta(hours=service_remaining_hours)
        last_service = state.simulated_time - timedelta(days=14)

        values: dict[str, Any] = {
            "mock_qa_console_profile": state.profile,
            "mock_qa_console_speed_multiplier": state.speed_multiplier,
            "mock_qa_console_automatic_faults": state.automatic_faults,
            "mock_qa_console_tick": state.tick,
            "mock_qa_console_simulated_time": iso(state.simulated_time),
            "synthetic_generator_running": generator_running,
            "synthetic_generator_runtime_seconds": round(state.runtime_seconds, 1),
            "synthetic_generator_runtime_minutes": round(state.runtime_seconds / 60, 2),
            "synthetic_generator_runtime_hours": round(state.runtime_seconds / 3600, 3),
            "synthetic_generator_session_runtime_minutes": round((state.runtime_seconds / 60) % 45, 2),
            "synthetic_generator_cycle_count": state.generator_cycles,
            "synthetic_generator_power": round(power, 1),
            "synthetic_generator_energy": round(state.total_kwh, 3),
            "synthetic_generator_service_due": service_due,
            "synthetic_generator_service_status": service_status,
            "synthetic_generator_service_remaining_hours": round(service_remaining_hours, 2),
            "synthetic_generator_service_due_date": iso(due_date),
            "synthetic_ups_online": not bad_window,
            "synthetic_ups_load": round(25 + 20 * math.sin(t / 300), 1),
            "synthetic_ups_battery": round(max(0, 100 - (state.tick % 200) * 0.2), 1),
            "synthetic_ups_runtime_remaining": round(80 - (state.tick % 100) * 0.3, 1),
            "synthetic_ups_battery_replacement_due": (state.tick % 300) > 260 or state.forced_service_state in ("due", "overdue"),
            "synthetic_ups_battery_remaining_days": max(0, 365 - state.tick),
            "synthetic_ups_self_test_status": "failed" if bad_window else "passed",
            "synthetic_pool_pump_running": pool_running,
            "synthetic_pool_pump_power": round(pool_power, 1),
            "synthetic_pool_pump_energy": round(state.pool_kwh, 3),
            "synthetic_pool_pump_runtime_hours": round(state.pool_runtime_seconds / 3600, 3),
            "synthetic_pool_pump_flow_gpm": round(42 + 3 * math.sin(t / 200), 1) if pool_running else 0,
            "synthetic_pool_pump_flow_lpm": round((42 + 3 * math.sin(t / 200)) * 3.785, 1) if pool_running else 0,
            "synthetic_pool_pump_pressure_psi": round(14 + 2 * math.sin(t / 400), 1),
            "synthetic_pool_pump_filter_service_due": hvac_life <= 10 or state.forced_service_state in ("due", "overdue"),
            "synthetic_pool_pump_filter_remaining_percent": round(hvac_life, 1),
            "synthetic_hvac_filter_life_remaining": round(hvac_life, 1),
            "synthetic_hvac_filter_used_percent": round(100 - hvac_life, 1),
            "synthetic_hvac_filter_airflow_cfm": round(900 - (100 - hvac_life) * 2, 1),
            "synthetic_hvac_filter_pressure_drop": round(50 + (100 - hvac_life) * 1.5, 1),
            "synthetic_hvac_filter_service_due": hvac_life <= 10 or state.forced_service_state in ("due", "overdue"),
            "synthetic_water_filter_gallons_used": round(state.water_gallons_used, 1),
            "synthetic_water_filter_gallons_remaining": round(water_remaining, 1),
            "synthetic_water_filter_liters_remaining": round(water_remaining * 3.785, 1),
            "synthetic_water_filter_service_due": water_remaining <= 500 or state.forced_service_state in ("due", "overdue"),
            "synthetic_energy_meter_power_w": round(850 + 120 * math.sin(t / 150), 1),
            "synthetic_energy_meter_power_kw": round((850 + 120 * math.sin(t / 150)) / 1000, 3),
            "synthetic_energy_meter_total_kwh": round(state.energy_meter_kwh, 3),
            "synthetic_energy_meter_session_kwh": round(state.energy_session_kwh, 3),
            "synthetic_energy_meter_resetting_counter": minute_cycle % 30,
            "synthetic_energy_meter_total_cycles": state.tick,
            "synthetic_environment_temperature_f": round(temp_f, 1),
            "synthetic_environment_temperature_c": round(temp_c, 1),
            "synthetic_environment_humidity": round(45 + 10 * math.sin(t / 2400), 1),
            "synthetic_environment_pressure_pa": round(101325 + 600 * math.sin(t / 5000), 1),
            "synthetic_environment_pressure_psi": round(14.7 + 0.08 * math.sin(t / 5000), 3),
            "synthetic_environment_distance_ft": round(10 + math.sin(t / 600), 2),
            "synthetic_environment_distance_m": round((10 + math.sin(t / 600)) * 0.3048, 2),
            "synthetic_calendar_last_completed": iso(last_service),
            "synthetic_calendar_next_due": iso(state.simulated_time + timedelta(days=30)),
            "synthetic_calendar_due_today": minute_cycle % 90 > 75,
            "synthetic_calendar_overdue": state.forced_service_state == "overdue",
            "synthetic_nfc_tag_present": minute_cycle % 20 == 0,
            "synthetic_nfc_last_scan": iso(state.simulated_time - timedelta(minutes=minute_cycle % 20)),
            "synthetic_nfc_scan_count": state.nfc_scan_count,
            "synthetic_fault_unknown_state": "unknown" if bad_window else "normal",
            "synthetic_fault_unavailable_state": None if (bad_window or automatic_fault_window) else "available",
            "synthetic_fault_negative_duration": -5 if bad_window else 5,
            "synthetic_fault_spiky_power": 9999 if bad_window or state.tick % 31 == 0 else round(100 + 10 * math.sin(t / 50), 1),
            "synthetic_fault_unit_change_value": round((state.tick % 20) / 2, 1),
            "synthetic_fault_error_status": "error" if bad_window else "ok",
        }

        for device in ("generator", "ups", "pool_pump", "hvac_filter", "water_filter", "energy_meter", "environment", "calendar", "nfc", "fault"):
            prefix = {
                "generator":"synthetic_generator", "ups":"synthetic_ups", "pool_pump":"synthetic_pool_pump",
                "hvac_filter":"synthetic_hvac_filter", "water_filter":"synthetic_water_filter", "energy_meter":"synthetic_energy_meter",
                "environment":"synthetic_environment", "calendar":"synthetic_calendar", "nfc":"synthetic_nfc", "fault":"synthetic_fault"
            }[device]
            values[f"{prefix}_firmware_version"] = "0.1.0-mock"
            values[f"{prefix}_hardware_revision"] = "A1"
            values[f"{prefix}_serial_number"] = f"MOCK-{device.upper()}-0001"
            values[f"{prefix}_last_service_date"] = iso(last_service)
            values[f"{prefix}_service_count"] = state.service_count
            values[f"{prefix}_service_reason"] = "filter" if "filter" in device else ("runtime" if device in ("generator", "pool_pump") else "inspection")

        self.values = values
        return values

    async def reset_runtime(self) -> None:
        self.store.state.runtime_seconds = 0
        self.store.state.pool_runtime_seconds = 0
        await self.store.async_save()

    async def reset_meters(self) -> None:
        s = self.store.state
        s.total_kwh = s.pool_kwh = s.energy_meter_kwh = s.energy_session_kwh = 0
        s.water_gallons_used = 0
        s.generator_cycles = s.pool_cycles = 0
        await self.store.async_save()

    async def reset_service_due(self) -> None:
        s = self.store.state
        s.forced_service_state = None
        s.service_count += 1
        await self.store.async_save()

    async def trigger_service_due(self, overdue: bool = False) -> None:
        self.store.state.forced_service_state = "overdue" if overdue else "due"
        await self.store.async_save()

    async def force_bad_data(self) -> None:
        self.store.state.manual_bad_data_until_tick = self.store.state.tick + 8
        await self.store.async_save()

    async def force_cycle(self) -> None:
        s = self.store.state
        s.runtime_seconds += 45 * 60
        s.pool_runtime_seconds += 60 * 60
        await self.store.async_save()

    async def seed_known_state(self) -> None:
        profile = self.store.state.profile
        speed = self.store.state.speed_multiplier
        faults = self.store.state.automatic_faults
        self.store.state = MockRuntimeState(profile=profile, speed_multiplier=speed, automatic_faults=faults)
        self.store.state.runtime_seconds = 10 * 3600
        self.store.state.pool_runtime_seconds = 20 * 3600
        self.store.state.water_gallons_used = 2500
        await self.store.async_save()
