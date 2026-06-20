"""Entity and synthetic device definitions for Mock Device.

This file is intentionally data-driven. Adding future coverage should usually mean
adding an EntitySpec row rather than writing a new entity class.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Platform = Literal["sensor", "binary_sensor", "button", "number", "select", "switch"]


@dataclass(frozen=True)
class MockDeviceSpec:
    """A synthetic HA device exposed by the integration."""

    key: str
    name: str
    manufacturer: str = "Mock Device"
    model: str = "Synthetic Equipment"
    sw_version: str = "0.1.0"
    hw_version: str = "A1"


@dataclass(frozen=True)
class EntitySpec:
    """Description of one generated Home Assistant entity."""

    key: str
    name: str
    platform: Platform
    device_key: str
    unit: str | None = None
    device_class: str | None = None
    state_class: str | None = None
    entity_category: str | None = None
    icon: str | None = None
    options: tuple[str, ...] | None = None
    native_min_value: float | None = None
    native_max_value: float | None = None
    native_step: float | None = None
    initial: Any = None


def slug(name: str) -> str:
    """Return the stable slug used in entity IDs."""
    return name.lower().replace(" ", "_").replace("/", "_").replace("-", "_")


DEVICES: tuple[MockDeviceSpec, ...] = (
    MockDeviceSpec("generator", "Synthetic Generator", model="Synthetic Generator"),
    MockDeviceSpec("ups", "Synthetic UPS", model="Synthetic UPS"),
    MockDeviceSpec("pool_pump", "Synthetic Pool Pump", model="Synthetic Pool Pump"),
    MockDeviceSpec("hvac_filter", "Synthetic HVAC Filter", model="Synthetic HVAC Filter"),
    MockDeviceSpec("water_filter", "Synthetic Water Filter", model="Synthetic Water Filter"),
    MockDeviceSpec("energy_meter", "Synthetic Energy Meter", model="Synthetic Energy Meter"),
    MockDeviceSpec("environment", "Synthetic Environment Station", model="Synthetic Environment Station"),
    MockDeviceSpec("calendar", "Synthetic Calendar Device", model="Synthetic Calendar Device"),
    MockDeviceSpec("nfc", "Synthetic NFC Device", model="Synthetic NFC Device"),
    MockDeviceSpec("fault", "Synthetic Fault Device", model="Synthetic Fault Device"),
    MockDeviceSpec("console", "Mock QA Console", model="QA Console"),
)


def common_equipment_entities(device_key: str) -> list[EntitySpec]:
    prefix = slug(next(d.name for d in DEVICES if d.key == device_key))
    return [
        EntitySpec(f"{prefix}_firmware_version", "Firmware Version", "sensor", device_key, entity_category="diagnostic", icon="mdi:chip"),
        EntitySpec(f"{prefix}_hardware_revision", "Hardware Revision", "sensor", device_key, entity_category="diagnostic", icon="mdi:expansion-card"),
        EntitySpec(f"{prefix}_serial_number", "Serial Number", "sensor", device_key, entity_category="diagnostic", icon="mdi:identifier"),
        EntitySpec(f"{prefix}_last_service_date", "Last Service Date", "sensor", device_key, device_class="timestamp", icon="mdi:calendar-check"),
        EntitySpec(f"{prefix}_service_count", "Service Count", "sensor", device_key, state_class="total_increasing", icon="mdi:counter"),
        EntitySpec(f"{prefix}_service_reason", "Service Reason", "sensor", device_key, icon="mdi:wrench-clock"),
    ]


ENTITY_SPECS: tuple[EntitySpec, ...] = tuple([
    # QA console controls. These are the only writable entities in v0.1.0.
    EntitySpec("mock_qa_console_profile", "Profile", "select", "console", options=("normal", "intermittent", "bad_data", "fast_forward", "long_cycle"), entity_category="config"),
    EntitySpec("mock_qa_console_speed_multiplier", "Speed Multiplier", "number", "console", unit="x", native_min_value=1, native_max_value=1440, native_step=1, entity_category="config", icon="mdi:speedometer"),
    EntitySpec("mock_qa_console_automatic_faults", "Automatic Faults", "switch", "console", entity_category="config", icon="mdi:alert-circle-outline"),
    EntitySpec("mock_qa_console_reset_all", "Reset All", "button", "console", icon="mdi:restore"),
    EntitySpec("mock_qa_console_reset_runtime", "Reset Runtime", "button", "console", icon="mdi:timer-refresh"),
    EntitySpec("mock_qa_console_reset_meters", "Reset Meters", "button", "console", icon="mdi:counter"),
    EntitySpec("mock_qa_console_reset_service_due", "Reset Service Due", "button", "console", icon="mdi:wrench-check"),
    EntitySpec("mock_qa_console_trigger_service_due", "Trigger Service Due", "button", "console", icon="mdi:wrench-alert"),
    EntitySpec("mock_qa_console_trigger_service_overdue", "Trigger Service Overdue", "button", "console", icon="mdi:calendar-alert"),
    EntitySpec("mock_qa_console_force_bad_data", "Force Bad Data", "button", "console", icon="mdi:bug"),
    EntitySpec("mock_qa_console_force_cycle", "Force Cycle", "button", "console", icon="mdi:reload"),
    EntitySpec("mock_qa_console_seed_known_state", "Seed Known State", "button", "console", icon="mdi:seed"),
    EntitySpec("mock_qa_console_tick", "Update Tick", "sensor", "console", state_class="total_increasing", entity_category="diagnostic", icon="mdi:clock-fast"),
    EntitySpec("mock_qa_console_simulated_time", "Simulated Time", "sensor", "console", device_class="timestamp", entity_category="diagnostic", icon="mdi:clock-outline"),

    # Synthetic Generator
    EntitySpec("synthetic_generator_running", "Running", "binary_sensor", "generator", device_class="running"),
    EntitySpec("synthetic_generator_runtime_seconds", "Runtime Seconds", "sensor", "generator", unit="s", device_class="duration", state_class="total_increasing"),
    EntitySpec("synthetic_generator_runtime_minutes", "Runtime Minutes", "sensor", "generator", unit="min", device_class="duration", state_class="total_increasing"),
    EntitySpec("synthetic_generator_runtime_hours", "Runtime Hours", "sensor", "generator", unit="h", device_class="duration", state_class="total_increasing"),
    EntitySpec("synthetic_generator_session_runtime_minutes", "Session Runtime Minutes", "sensor", "generator", unit="min", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_generator_cycle_count", "Cycle Count", "sensor", "generator", state_class="total_increasing", icon="mdi:counter"),
    EntitySpec("synthetic_generator_power", "Power", "sensor", "generator", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_generator_energy", "Energy", "sensor", "generator", unit="kWh", device_class="energy", state_class="total_increasing"),
    EntitySpec("synthetic_generator_service_due", "Service Due", "binary_sensor", "generator", device_class="problem"),
    EntitySpec("synthetic_generator_service_status", "Service Status", "sensor", "generator", icon="mdi:wrench"),
    EntitySpec("synthetic_generator_service_remaining_hours", "Service Remaining Hours", "sensor", "generator", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_generator_service_due_date", "Service Due Date", "sensor", "generator", device_class="timestamp"),

    # UPS
    EntitySpec("synthetic_ups_online", "Online", "binary_sensor", "ups", device_class="connectivity"),
    EntitySpec("synthetic_ups_load", "Load", "sensor", "ups", unit="%", state_class="measurement"),
    EntitySpec("synthetic_ups_battery", "Battery", "sensor", "ups", unit="%", device_class="battery", state_class="measurement"),
    EntitySpec("synthetic_ups_runtime_remaining", "Runtime Remaining", "sensor", "ups", unit="min", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_ups_battery_replacement_due", "Battery Replacement Due", "binary_sensor", "ups", device_class="problem"),
    EntitySpec("synthetic_ups_battery_remaining_days", "Battery Remaining Days", "sensor", "ups", unit="d", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_ups_self_test_status", "Self Test Status", "sensor", "ups", icon="mdi:clipboard-check"),

    # Pool pump
    EntitySpec("synthetic_pool_pump_running", "Running", "binary_sensor", "pool_pump", device_class="running"),
    EntitySpec("synthetic_pool_pump_power", "Power", "sensor", "pool_pump", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_energy", "Energy", "sensor", "pool_pump", unit="kWh", device_class="energy", state_class="total_increasing"),
    EntitySpec("synthetic_pool_pump_runtime_hours", "Runtime Hours", "sensor", "pool_pump", unit="h", device_class="duration", state_class="total_increasing"),
    EntitySpec("synthetic_pool_pump_flow_gpm", "Flow GPM", "sensor", "pool_pump", unit="gal/min", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_flow_lpm", "Flow LPM", "sensor", "pool_pump", unit="L/min", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_pressure_psi", "Pressure PSI", "sensor", "pool_pump", unit="psi", device_class="pressure", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_filter_service_due", "Filter Service Due", "binary_sensor", "pool_pump", device_class="problem"),
    EntitySpec("synthetic_pool_pump_filter_remaining_percent", "Filter Remaining Percent", "sensor", "pool_pump", unit="%", state_class="measurement"),

    # Filter devices
    EntitySpec("synthetic_hvac_filter_life_remaining", "Life Remaining", "sensor", "hvac_filter", unit="%", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_used_percent", "Used Percent", "sensor", "hvac_filter", unit="%", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_airflow_cfm", "Airflow", "sensor", "hvac_filter", unit="ft³/min", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_pressure_drop", "Pressure Drop", "sensor", "hvac_filter", unit="Pa", device_class="pressure", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_service_due", "Service Due", "binary_sensor", "hvac_filter", device_class="problem"),
    EntitySpec("synthetic_water_filter_gallons_used", "Gallons Used", "sensor", "water_filter", unit="gal", device_class="volume", state_class="total_increasing"),
    EntitySpec("synthetic_water_filter_gallons_remaining", "Gallons Remaining", "sensor", "water_filter", unit="gal", device_class="volume", state_class="measurement"),
    EntitySpec("synthetic_water_filter_liters_remaining", "Liters Remaining", "sensor", "water_filter", unit="L", device_class="volume", state_class="measurement"),
    EntitySpec("synthetic_water_filter_service_due", "Service Due", "binary_sensor", "water_filter", device_class="problem"),

    # Energy meter
    EntitySpec("synthetic_energy_meter_power_w", "Power W", "sensor", "energy_meter", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_energy_meter_power_kw", "Power kW", "sensor", "energy_meter", unit="kW", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_energy_meter_total_kwh", "Total kWh", "sensor", "energy_meter", unit="kWh", device_class="energy", state_class="total_increasing"),
    EntitySpec("synthetic_energy_meter_session_kwh", "Session kWh", "sensor", "energy_meter", unit="kWh", device_class="energy", state_class="measurement"),
    EntitySpec("synthetic_energy_meter_resetting_counter", "Resetting Counter", "sensor", "energy_meter", state_class="measurement", icon="mdi:counter"),
    EntitySpec("synthetic_energy_meter_total_cycles", "Total Cycles", "sensor", "energy_meter", state_class="total_increasing", icon="mdi:counter"),

    # Environment
    EntitySpec("synthetic_environment_temperature_f", "Temperature F", "sensor", "environment", unit="°F", device_class="temperature", state_class="measurement"),
    EntitySpec("synthetic_environment_temperature_c", "Temperature C", "sensor", "environment", unit="°C", device_class="temperature", state_class="measurement"),
    EntitySpec("synthetic_environment_humidity", "Humidity", "sensor", "environment", unit="%", device_class="humidity", state_class="measurement"),
    EntitySpec("synthetic_environment_pressure_pa", "Pressure Pa", "sensor", "environment", unit="Pa", device_class="pressure", state_class="measurement"),
    EntitySpec("synthetic_environment_pressure_psi", "Pressure PSI", "sensor", "environment", unit="psi", device_class="pressure", state_class="measurement"),
    EntitySpec("synthetic_environment_distance_ft", "Distance FT", "sensor", "environment", unit="ft", device_class="distance", state_class="measurement"),
    EntitySpec("synthetic_environment_distance_m", "Distance M", "sensor", "environment", unit="m", device_class="distance", state_class="measurement"),

    # Calendar / NFC placeholders for future HMM and automation QA.
    EntitySpec("synthetic_calendar_last_completed", "Last Completed", "sensor", "calendar", device_class="timestamp"),
    EntitySpec("synthetic_calendar_next_due", "Next Due", "sensor", "calendar", device_class="timestamp"),
    EntitySpec("synthetic_calendar_due_today", "Due Today", "binary_sensor", "calendar", device_class="problem"),
    EntitySpec("synthetic_calendar_overdue", "Overdue", "binary_sensor", "calendar", device_class="problem"),
    EntitySpec("synthetic_nfc_tag_present", "Tag Present", "binary_sensor", "nfc", device_class="presence"),
    EntitySpec("synthetic_nfc_last_scan", "Last Scan", "sensor", "nfc", device_class="timestamp"),
    EntitySpec("synthetic_nfc_scan_count", "Scan Count", "sensor", "nfc", state_class="total_increasing", icon="mdi:nfc"),

    # Fault / bad data device.
    EntitySpec("synthetic_fault_unknown_state", "Unknown State", "sensor", "fault", icon="mdi:help-circle"),
    EntitySpec("synthetic_fault_unavailable_state", "Unavailable State", "sensor", "fault", icon="mdi:cloud-off-outline"),
    EntitySpec("synthetic_fault_negative_duration", "Negative Duration", "sensor", "fault", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_fault_spiky_power", "Spiky Power", "sensor", "fault", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_fault_unit_change_value", "Unit Change Value", "sensor", "fault", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_fault_error_status", "Error Status", "sensor", "fault", icon="mdi:alert"),
] + sum([common_equipment_entities(d.key) for d in DEVICES if d.key != "console"], []))
