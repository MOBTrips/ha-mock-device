"""Persistent state and deterministic data generator for Mock Device.

The generator is deliberately deterministic. Given the same persisted state,
speed multiplier, profile, and elapsed real time, testers should see predictable
changes. This makes the integration useful for repeatable QA, HMM task pack
mapping tests, and bug reproduction across Home Assistant restarts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import math
from typing import Any

from homeassistant.helpers.storage import Store

from .const import DEFAULT_SPEED_MULTIPLIER, PROFILE_NORMAL
from .models import DEVICES, slug

STORE_VERSION = 1
STORE_KEY = "mock_device_state"


def utcnow() -> datetime:
    """Return timezone-aware UTC now."""
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    """Return an ISO timestamp suitable for HA timestamp sensors."""
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
    session_seconds: float = 0.0
    total_count: int = 0
    total_cycles: int = 0
    total_gallons: float = 0.0
    total_kwh: float = 0.0
    total_cubic_feet: float = 0.0
    total_miles: float = 0.0
    event_count: int = 0
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
        self.state = MockRuntimeState(
            profile=self.state.profile,
            speed_multiplier=self.state.speed_multiplier,
            automatic_faults=self.state.automatic_faults,
        )
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
        minute_cycle = int(t // 60)
        hour_cycle = int(t // 3600)
        day_cycle = int(t // 86400)
        intermittent = state.profile == "intermittent"
        running = (minute_cycle % (6 if intermittent else 10)) < (3 if intermittent else 7)
        if state.profile == "long_cycle":
            running = (hour_cycle % 8) < 6

        bad_window = state.profile == "bad_data" or state.tick < state.manual_bad_data_until_tick
        automatic_fault_window = state.automatic_faults and (state.tick % 40 in (0, 1))

        if running:
            state.runtime_seconds += sim_seconds
            state.total_kwh += sim_seconds / 3600 * 1.25
            state.total_gallons += sim_seconds / 60 * 8.0
            state.total_cubic_feet += sim_seconds / 60 * 1.2
            state.total_miles += sim_seconds / 3600 * 0.03
        state.total_count += max(1, int(sim_seconds // 60))
        state.total_cycles = int(state.runtime_seconds // (45 * 60))
        state.session_seconds = (state.runtime_seconds % (45 * 60))
        state.event_count = int(state.tick // 5)

        used_pct = min(100.0, state.runtime_seconds / 3600)  # 100 simulated runtime hours to due
        remaining_pct = max(0.0, 100.0 - used_pct)
        remaining_hours = max(0.0, 100.0 - state.runtime_seconds / 3600)
        service_due = remaining_hours <= 0 or state.forced_service_state in ("due", "overdue")
        service_overdue = state.forced_service_state == "overdue" or remaining_hours <= -10
        service_status = "overdue" if service_overdue else ("due" if service_due else "ok")
        due_date = state.simulated_time + timedelta(hours=remaining_hours)
        last_service = state.simulated_time - timedelta(days=14)

        temp_c = 20 + 5 * math.sin(t / 1800)
        temp_f = temp_c * 9 / 5 + 32
        power_w = 900 + 160 * math.sin(t / 120) if running else 0
        flow_gpm = 38 + 4 * math.sin(t / 200) if running else 0
        pressure_in = 18 + 1.5 * math.sin(t / 300)
        pressure_out = 14 + 1.0 * math.sin(t / 300)
        session_count = minute_cycle % 30
        session_gallons = (state.total_gallons % 250)
        session_kwh = (state.total_kwh % 5)
        event_now = state.tick % 5 == 0
        fault_now = bad_window or state.tick % 37 == 0

        values: dict[str, Any] = {
            # Console
            "mock_qa_console_profile": state.profile,
            "mock_qa_console_speed_multiplier": state.speed_multiplier,
            "mock_qa_console_automatic_faults": state.automatic_faults,
            "mock_qa_console_tick": state.tick,
            "mock_qa_console_simulated_time": iso(state.simulated_time),

            # Generic runtime
            "mock_runtime_device_running": running,
            "mock_runtime_device_idle": not running,
            "mock_runtime_device_power_running": power_w > 25,
            "mock_runtime_device_runtime_seconds": round(state.runtime_seconds, 1),
            "mock_runtime_device_runtime_minutes": round(state.runtime_seconds / 60, 2),
            "mock_runtime_device_runtime_hours": round(state.runtime_seconds / 3600, 3),
            "mock_runtime_device_runtime_days": round(state.runtime_seconds / 86400, 4),
            "mock_runtime_device_session_seconds": round(state.session_seconds, 1),
            "mock_runtime_device_session_minutes": round(state.session_seconds / 60, 2),
            "mock_runtime_device_power_w": round(power_w, 1),
            "mock_runtime_device_power_kw": round(power_w / 1000, 3),
            "mock_runtime_device_cycle_count": state.total_cycles,

            # Generic meters
            "mock_meter_device_total_count": state.total_count,
            "mock_meter_device_session_count": session_count,
            "mock_meter_device_total_cycles": state.total_cycles,
            "mock_meter_device_session_cycles": session_count % 10,
            "mock_meter_device_total_gallons": round(state.total_gallons, 2),
            "mock_meter_device_session_gallons": round(session_gallons, 2),
            "mock_meter_device_total_liters": round(state.total_gallons * 3.78541, 2),
            "mock_meter_device_total_kwh": round(state.total_kwh, 4),
            "mock_meter_device_session_kwh": round(session_kwh, 4),
            "mock_meter_device_total_cubic_feet": round(state.total_cubic_feet, 3),

            # Generic service
            "mock_service_device_service_due": service_due,
            "mock_service_device_service_overdue": service_overdue,
            "mock_service_device_service_status": service_status,
            "mock_service_device_remaining_seconds": round(remaining_hours * 3600, 0),
            "mock_service_device_remaining_minutes": round(remaining_hours * 60, 1),
            "mock_service_device_remaining_hours": round(remaining_hours, 2),
            "mock_service_device_remaining_days": round(remaining_hours / 24, 2),
            "mock_service_device_remaining_cycles": max(0, 100 - state.total_cycles),
            "mock_service_device_used_percent": round(used_pct, 1),
            "mock_service_device_remaining_percent": round(remaining_pct, 1),
            "mock_service_device_due_date": iso(due_date),
            "mock_service_device_last_completed": iso(last_service),
            "mock_service_device_reason": "runtime" if service_due else "none",

            # Environmental
            "mock_environmental_device_temperature_f": round(temp_f, 1),
            "mock_environmental_device_temperature_c": round(temp_c, 1),
            "mock_environmental_device_humidity": round(45 + 10 * math.sin(t / 2400), 1),
            "mock_environmental_device_pressure_pa": round(101325 + 600 * math.sin(t / 5000), 1),
            "mock_environmental_device_pressure_psi": round(14.7 + 0.08 * math.sin(t / 5000), 3),
            "mock_environmental_device_illuminance": round(500 + 400 * max(0, math.sin(t / 3600)), 1),
            "mock_environmental_device_signal_strength": round(-65 + 5 * math.sin(t / 500), 1),
            "mock_environmental_device_battery": round(max(0, 100 - (state.tick % 500) * 0.1), 1),

            # Flow/distance/consumables
            "mock_flow_device_flow_gpm": round(flow_gpm, 1),
            "mock_flow_device_flow_lpm": round(flow_gpm * 3.78541, 1),
            "mock_flow_device_airflow_cfm": round(850 + 70 * math.sin(t / 350), 1),
            "mock_flow_device_pressure_in": round(pressure_in, 2),
            "mock_flow_device_pressure_out": round(pressure_out, 2),
            "mock_flow_device_pressure_drop_pa": round((pressure_in - pressure_out) * 6894.76, 1),
            "mock_flow_device_total_volume_gal": round(state.total_gallons, 2),
            "mock_distance_device_distance_ft": round(10 + math.sin(t / 600), 2),
            "mock_distance_device_distance_m": round((10 + math.sin(t / 600)) * 0.3048, 2),
            "mock_distance_device_total_miles": round(state.total_miles, 4),
            "mock_distance_device_total_km": round(state.total_miles * 1.60934, 4),
            "mock_distance_device_session_feet": round((state.total_miles * 5280) % 500, 1),
            "mock_consumable_device_life_remaining_percent": round(remaining_pct, 1),
            "mock_consumable_device_life_used_percent": round(used_pct, 1),
            "mock_consumable_device_days_remaining": round(remaining_hours / 24, 2),
            "mock_consumable_device_hours_remaining": round(remaining_hours, 2),
            "mock_consumable_device_replacement_due": service_due,
            "mock_consumable_device_consumable_type": "filter",

            # Calendar/event/binary/enum
            "mock_calendar_device_last_completed": iso(last_service),
            "mock_calendar_device_next_due": iso(state.simulated_time + timedelta(days=30)),
            "mock_calendar_device_due_today": minute_cycle % 90 > 75,
            "mock_calendar_device_overdue": service_overdue,
            "mock_calendar_device_day_of_month": state.simulated_time.day,
            "mock_calendar_device_week_of_year": int(state.simulated_time.strftime("%V")),
            "mock_event_device_cycle_complete": event_now,
            "mock_event_device_fault_occurred": fault_now,
            "mock_event_device_last_event": "fault" if fault_now else ("cycle_complete" if event_now else "none"),
            "mock_event_device_event_count": state.event_count,
            "mock_event_device_last_event_time": iso(state.simulated_time - timedelta(minutes=state.tick % 5)),
            "mock_binary_device_on_off": running,
            "mock_binary_device_opening": minute_cycle % 12 < 6,
            "mock_binary_device_moisture": minute_cycle % 45 in (0, 1, 2),
            "mock_binary_device_connectivity": not (bad_window or automatic_fault_window),
            "mock_binary_device_problem": fault_now,
            "mock_binary_device_safety": not fault_now,
            "mock_enum_status_device_status": "error" if fault_now else ("running" if running else "idle"),
            "mock_enum_status_device_mode": state.profile,
            "mock_enum_status_device_health": "bad" if fault_now else ("warning" if service_due else "good"),
            "mock_enum_status_device_service_state": service_status,

            # Fault injection
            "mock_fault_device_unknown_state": "unknown" if bad_window else "normal",
            "mock_fault_device_unavailable_state": None if (bad_window or automatic_fault_window) else "available",
            "mock_fault_device_negative_duration": -5 if bad_window else 5,
            "mock_fault_device_zero_value": 0,
            "mock_fault_device_spiky_power": 9999 if bad_window or state.tick % 31 == 0 else round(100 + 10 * math.sin(t / 50), 1),
            "mock_fault_device_stale_timestamp": iso(state.simulated_time - timedelta(days=90)),
            "mock_fault_device_unit_mismatch_value": round((state.tick % 20) / 2, 1),
            "mock_fault_device_error_status": "error" if bad_window else "ok",
        }

        # Equipment demo aliases use the same generator behavior with realistic names.
        values.update({
            "synthetic_generator_running": running,
            "synthetic_generator_runtime_hours": values["mock_runtime_device_runtime_hours"],
            "synthetic_generator_power": round(power_w * 2.5, 1),
            "synthetic_generator_energy": values["mock_meter_device_total_kwh"],
            "synthetic_generator_cycle_count": state.total_cycles,
            "synthetic_generator_service_due": service_due,
            "synthetic_generator_service_status": service_status,
            "synthetic_generator_service_remaining_hours": values["mock_service_device_remaining_hours"],
            "synthetic_generator_service_due_date": values["mock_service_device_due_date"],
            "synthetic_ups_online": not fault_now,
            "synthetic_ups_load": round(25 + 20 * math.sin(t / 300), 1),
            "synthetic_ups_battery": values["mock_environmental_device_battery"],
            "synthetic_ups_runtime_remaining": round(max(0, 90 - state.tick % 120), 1),
            "synthetic_ups_battery_replacement_due": service_due,
            "synthetic_ups_battery_remaining_days": values["mock_consumable_device_days_remaining"],
            "synthetic_ups_self_test_status": "failed" if fault_now else "passed",
            "synthetic_pool_pump_running": running,
            "synthetic_pool_pump_power": values["mock_runtime_device_power_w"],
            "synthetic_pool_pump_energy": values["mock_meter_device_total_kwh"],
            "synthetic_pool_pump_runtime_hours": values["mock_runtime_device_runtime_hours"],
            "synthetic_pool_pump_flow_gpm": values["mock_flow_device_flow_gpm"],
            "synthetic_pool_pump_flow_lpm": values["mock_flow_device_flow_lpm"],
            "synthetic_pool_pump_pressure_psi": values["mock_flow_device_pressure_in"],
            "synthetic_pool_pump_filter_service_due": service_due,
            "synthetic_pool_pump_filter_remaining_percent": values["mock_consumable_device_life_remaining_percent"],
            "synthetic_hvac_filter_life_remaining": values["mock_consumable_device_life_remaining_percent"],
            "synthetic_hvac_filter_used_percent": values["mock_consumable_device_life_used_percent"],
            "synthetic_hvac_filter_airflow_cfm": values["mock_flow_device_airflow_cfm"],
            "synthetic_hvac_filter_pressure_drop": values["mock_flow_device_pressure_drop_pa"],
            "synthetic_hvac_filter_service_due": service_due,
            "synthetic_water_filter_gallons_used": values["mock_meter_device_total_gallons"],
            "synthetic_water_filter_gallons_remaining": round(max(0, 10000 - state.total_gallons), 1),
            "synthetic_water_filter_liters_remaining": round(max(0, 10000 - state.total_gallons) * 3.78541, 1),
            "synthetic_water_filter_service_due": service_due,
            "synthetic_energy_meter_power_w": values["mock_runtime_device_power_w"],
            "synthetic_energy_meter_power_kw": values["mock_runtime_device_power_kw"],
            "synthetic_energy_meter_total_kwh": values["mock_meter_device_total_kwh"],
            "synthetic_energy_meter_session_kwh": values["mock_meter_device_session_kwh"],
            "synthetic_environment_temperature_f": values["mock_environmental_device_temperature_f"],
            "synthetic_environment_temperature_c": values["mock_environmental_device_temperature_c"],
            "synthetic_environment_humidity": values["mock_environmental_device_humidity"],
            "synthetic_environment_pressure_pa": values["mock_environmental_device_pressure_pa"],
        })

        for device in DEVICES:
            if device.key == "console":
                continue
            prefix = slug(device.name)
            values[f"{prefix}_firmware_version"] = "0.1.1-mock"
            values[f"{prefix}_hardware_revision"] = "A1"
            values[f"{prefix}_serial_number"] = f"MOCK-{device.key.upper()}-0001"
            values[f"{prefix}_last_service_date"] = iso(last_service)
            values[f"{prefix}_service_count"] = state.service_count
            values[f"{prefix}_service_reason"] = "runtime" if device.key in {"runtime", "generator", "pool_pump"} else ("filter" if "filter" in device.key or device.key == "consumable" else "inspection")

        self.values = values
        return values

    async def reset_runtime(self) -> None:
        self.store.state.runtime_seconds = 0
        self.store.state.session_seconds = 0
        await self.store.async_save()

    async def reset_meters(self) -> None:
        s = self.store.state
        s.total_count = s.total_cycles = 0
        s.total_gallons = s.total_kwh = s.total_cubic_feet = s.total_miles = 0
        await self.store.async_save()

    async def reset_service_due(self) -> None:
        s = self.store.state
        s.forced_service_state = None
        s.runtime_seconds = min(s.runtime_seconds, 10 * 3600)
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
        s.total_cycles += 1
        s.event_count += 1
        await self.store.async_save()

    async def seed_known_state(self) -> None:
        profile = self.store.state.profile
        speed = self.store.state.speed_multiplier
        faults = self.store.state.automatic_faults
        self.store.state = MockRuntimeState(profile=profile, speed_multiplier=speed, automatic_faults=faults)
        self.store.state.runtime_seconds = 10 * 3600
        self.store.state.total_count = 100
        self.store.state.total_cycles = 12
        self.store.state.total_gallons = 2500
        self.store.state.total_kwh = 42
        self.store.state.total_cubic_feet = 333
        self.store.state.total_miles = 5
        await self.store.async_save()
