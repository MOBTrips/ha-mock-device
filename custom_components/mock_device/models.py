"""Entity and synthetic device definitions for Mock Device.

The integration is intentionally data-driven. Each row below represents a
stable entity ID that can be used by other integrations' QA packs. Keep keys
stable once released; add new keys instead of renaming old ones.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Platform = Literal["sensor", "binary_sensor", "button", "number", "select", "switch"]


@dataclass(frozen=True)
class MockDeviceSpec:
    """A synthetic Home Assistant device exposed by the integration."""

    key: str
    name: str
    manufacturer: str = "Mock Device"
    model: str = "Generated QA Device"
    sw_version: str = "0.1.1"
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
    # Generic QA devices are the primary target for integration-agnostic testing.
    MockDeviceSpec("runtime", "Mock Runtime Device", model="Generic Runtime QA Device"),
    MockDeviceSpec("meter", "Mock Meter Device", model="Generic Meter QA Device"),
    MockDeviceSpec("service", "Mock Service Device", model="Generic Service QA Device"),
    MockDeviceSpec("environmental", "Mock Environmental Device", model="Generic Environmental QA Device"),
    MockDeviceSpec("flow", "Mock Flow Device", model="Generic Flow QA Device"),
    MockDeviceSpec("distance", "Mock Distance Device", model="Generic Distance QA Device"),
    MockDeviceSpec("consumable", "Mock Consumable Device", model="Generic Consumable QA Device"),
    MockDeviceSpec("calendar", "Mock Calendar Device", model="Generic Calendar QA Device"),
    MockDeviceSpec("event", "Mock Event Device", model="Generic Event QA Device"),
    MockDeviceSpec("binary", "Mock Binary Device", model="Generic Binary QA Device"),
    MockDeviceSpec("enum", "Mock Enum Status Device", model="Generic Enum QA Device"),
    MockDeviceSpec("fault", "Mock Fault Device", model="Generic Fault Injection QA Device"),
    MockDeviceSpec("console", "Mock QA Console", model="QA Control Console"),
    # Equipment examples mirror common real-world HA integrations.
    MockDeviceSpec("generator", "Synthetic Generator", model="Synthetic Generator"),
    MockDeviceSpec("ups", "Synthetic UPS", model="Synthetic UPS"),
    MockDeviceSpec("pool_pump", "Synthetic Pool Pump", model="Synthetic Pool Pump"),
    MockDeviceSpec("hvac_filter", "Synthetic HVAC Filter", model="Synthetic HVAC Filter"),
    MockDeviceSpec("water_filter", "Synthetic Water Filter", model="Synthetic Water Filter"),
    MockDeviceSpec("energy_meter", "Synthetic Energy Meter", model="Synthetic Energy Meter"),
    MockDeviceSpec("environment", "Synthetic Environment Station", model="Synthetic Environment Station"),
)


def common_entities(device_key: str) -> list[EntitySpec]:
    prefix = slug(next(d.name for d in DEVICES if d.key == device_key))
    return [
        EntitySpec(f"{prefix}_firmware_version", "Firmware Version", "sensor", device_key, entity_category="diagnostic", icon="mdi:chip"),
        EntitySpec(f"{prefix}_hardware_revision", "Hardware Revision", "sensor", device_key, entity_category="diagnostic", icon="mdi:expansion-card"),
        EntitySpec(f"{prefix}_serial_number", "Serial Number", "sensor", device_key, entity_category="diagnostic", icon="mdi:identifier"),
        EntitySpec(f"{prefix}_last_service_date", "Last Service Date", "sensor", device_key, device_class="timestamp", icon="mdi:calendar-check"),
        EntitySpec(f"{prefix}_service_count", "Service Count", "sensor", device_key, state_class="total_increasing", icon="mdi:counter"),
        EntitySpec(f"{prefix}_service_reason", "Service Reason", "sensor", device_key, icon="mdi:wrench-clock"),
    ]


BASE_ENTITY_SPECS: list[EntitySpec] = [
    # QA console controls. Sensors remain read-only; these controls manipulate the generator.
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

    # Generic runtime coverage: timebase and runtime-detection combinations.
    EntitySpec("mock_runtime_device_running", "Running", "binary_sensor", "runtime", device_class="running"),
    EntitySpec("mock_runtime_device_idle", "Idle", "binary_sensor", "runtime"),
    EntitySpec("mock_runtime_device_power_running", "Power Running", "binary_sensor", "runtime", device_class="running"),
    EntitySpec("mock_runtime_device_runtime_seconds", "Runtime Seconds", "sensor", "runtime", unit="s", device_class="duration", state_class="total_increasing"),
    EntitySpec("mock_runtime_device_runtime_minutes", "Runtime Minutes", "sensor", "runtime", unit="min", device_class="duration", state_class="total_increasing"),
    EntitySpec("mock_runtime_device_runtime_hours", "Runtime Hours", "sensor", "runtime", unit="h", device_class="duration", state_class="total_increasing"),
    EntitySpec("mock_runtime_device_runtime_days", "Runtime Days", "sensor", "runtime", unit="d", device_class="duration", state_class="total_increasing"),
    EntitySpec("mock_runtime_device_session_seconds", "Session Seconds", "sensor", "runtime", unit="s", device_class="duration", state_class="measurement"),
    EntitySpec("mock_runtime_device_session_minutes", "Session Minutes", "sensor", "runtime", unit="min", device_class="duration", state_class="measurement"),
    EntitySpec("mock_runtime_device_power_w", "Power W", "sensor", "runtime", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("mock_runtime_device_power_kw", "Power kW", "sensor", "runtime", unit="kW", device_class="power", state_class="measurement"),
    EntitySpec("mock_runtime_device_cycle_count", "Cycle Count", "sensor", "runtime", state_class="total_increasing", icon="mdi:counter"),

    # Generic meter coverage: total increasing vs resetting/session and common units.
    EntitySpec("mock_meter_device_total_count", "Total Count", "sensor", "meter", state_class="total_increasing", icon="mdi:counter"),
    EntitySpec("mock_meter_device_session_count", "Session Count", "sensor", "meter", state_class="measurement", icon="mdi:counter"),
    EntitySpec("mock_meter_device_total_cycles", "Total Cycles", "sensor", "meter", unit="cycles", state_class="total_increasing", icon="mdi:counter"),
    EntitySpec("mock_meter_device_session_cycles", "Session Cycles", "sensor", "meter", unit="cycles", state_class="measurement", icon="mdi:counter"),
    EntitySpec("mock_meter_device_total_gallons", "Total Gallons", "sensor", "meter", unit="gal", device_class="volume", state_class="total_increasing"),
    EntitySpec("mock_meter_device_session_gallons", "Session Gallons", "sensor", "meter", unit="gal", device_class="volume", state_class="measurement"),
    EntitySpec("mock_meter_device_total_liters", "Total Liters", "sensor", "meter", unit="L", device_class="volume", state_class="total_increasing"),
    EntitySpec("mock_meter_device_total_kwh", "Total kWh", "sensor", "meter", unit="kWh", device_class="energy", state_class="total_increasing"),
    EntitySpec("mock_meter_device_session_kwh", "Session kWh", "sensor", "meter", unit="kWh", device_class="energy", state_class="measurement"),
    EntitySpec("mock_meter_device_total_cubic_feet", "Total Cubic Feet", "sensor", "meter", unit="ft³", device_class="volume", state_class="total_increasing"),

    # Device-reported service due coverage.
    EntitySpec("mock_service_device_service_due", "Service Due", "binary_sensor", "service", device_class="problem"),
    EntitySpec("mock_service_device_service_overdue", "Service Overdue", "binary_sensor", "service", device_class="problem"),
    EntitySpec("mock_service_device_service_status", "Service Status", "sensor", "service", icon="mdi:wrench"),
    EntitySpec("mock_service_device_remaining_seconds", "Remaining Seconds", "sensor", "service", unit="s", device_class="duration", state_class="measurement"),
    EntitySpec("mock_service_device_remaining_minutes", "Remaining Minutes", "sensor", "service", unit="min", device_class="duration", state_class="measurement"),
    EntitySpec("mock_service_device_remaining_hours", "Remaining Hours", "sensor", "service", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("mock_service_device_remaining_days", "Remaining Days", "sensor", "service", unit="d", device_class="duration", state_class="measurement"),
    EntitySpec("mock_service_device_remaining_cycles", "Remaining Cycles", "sensor", "service", unit="cycles", state_class="measurement", icon="mdi:counter"),
    EntitySpec("mock_service_device_used_percent", "Used Percent", "sensor", "service", unit="%", state_class="measurement"),
    EntitySpec("mock_service_device_remaining_percent", "Remaining Percent", "sensor", "service", unit="%", state_class="measurement"),
    EntitySpec("mock_service_device_due_date", "Due Date", "sensor", "service", device_class="timestamp"),
    EntitySpec("mock_service_device_last_completed", "Last Completed", "sensor", "service", device_class="timestamp"),
    EntitySpec("mock_service_device_reason", "Reason", "sensor", "service", icon="mdi:wrench-clock"),

    # Environmental/threshold values.
    EntitySpec("mock_environmental_device_temperature_f", "Temperature F", "sensor", "environmental", unit="°F", device_class="temperature", state_class="measurement"),
    EntitySpec("mock_environmental_device_temperature_c", "Temperature C", "sensor", "environmental", unit="°C", device_class="temperature", state_class="measurement"),
    EntitySpec("mock_environmental_device_humidity", "Humidity", "sensor", "environmental", unit="%", device_class="humidity", state_class="measurement"),
    EntitySpec("mock_environmental_device_pressure_pa", "Pressure Pa", "sensor", "environmental", unit="Pa", device_class="pressure", state_class="measurement"),
    EntitySpec("mock_environmental_device_pressure_psi", "Pressure PSI", "sensor", "environmental", unit="psi", device_class="pressure", state_class="measurement"),
    EntitySpec("mock_environmental_device_illuminance", "Illuminance", "sensor", "environmental", unit="lx", device_class="illuminance", state_class="measurement"),
    EntitySpec("mock_environmental_device_signal_strength", "Signal Strength", "sensor", "environmental", unit="dBm", device_class="signal_strength", state_class="measurement"),
    EntitySpec("mock_environmental_device_battery", "Battery", "sensor", "environmental", unit="%", device_class="battery", state_class="measurement"),

    # Flow, air, water, and pressure-differential coverage.
    EntitySpec("mock_flow_device_flow_gpm", "Flow GPM", "sensor", "flow", unit="gal/min", state_class="measurement"),
    EntitySpec("mock_flow_device_flow_lpm", "Flow LPM", "sensor", "flow", unit="L/min", state_class="measurement"),
    EntitySpec("mock_flow_device_airflow_cfm", "Airflow CFM", "sensor", "flow", unit="ft³/min", state_class="measurement"),
    EntitySpec("mock_flow_device_pressure_in", "Pressure In", "sensor", "flow", unit="psi", device_class="pressure", state_class="measurement"),
    EntitySpec("mock_flow_device_pressure_out", "Pressure Out", "sensor", "flow", unit="psi", device_class="pressure", state_class="measurement"),
    EntitySpec("mock_flow_device_pressure_drop_pa", "Pressure Drop Pa", "sensor", "flow", unit="Pa", device_class="pressure", state_class="measurement"),
    EntitySpec("mock_flow_device_total_volume_gal", "Total Volume gal", "sensor", "flow", unit="gal", device_class="volume", state_class="total_increasing"),

    # Distance/travel wear coverage.
    EntitySpec("mock_distance_device_distance_ft", "Distance ft", "sensor", "distance", unit="ft", device_class="distance", state_class="measurement"),
    EntitySpec("mock_distance_device_distance_m", "Distance m", "sensor", "distance", unit="m", device_class="distance", state_class="measurement"),
    EntitySpec("mock_distance_device_total_miles", "Total Miles", "sensor", "distance", unit="mi", device_class="distance", state_class="total_increasing"),
    EntitySpec("mock_distance_device_total_km", "Total Kilometers", "sensor", "distance", unit="km", device_class="distance", state_class="total_increasing"),
    EntitySpec("mock_distance_device_session_feet", "Session Feet", "sensor", "distance", unit="ft", device_class="distance", state_class="measurement"),

    # Consumable life coverage.
    EntitySpec("mock_consumable_device_life_remaining_percent", "Life Remaining Percent", "sensor", "consumable", unit="%", state_class="measurement"),
    EntitySpec("mock_consumable_device_life_used_percent", "Life Used Percent", "sensor", "consumable", unit="%", state_class="measurement"),
    EntitySpec("mock_consumable_device_days_remaining", "Days Remaining", "sensor", "consumable", unit="d", device_class="duration", state_class="measurement"),
    EntitySpec("mock_consumable_device_hours_remaining", "Hours Remaining", "sensor", "consumable", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("mock_consumable_device_replacement_due", "Replacement Due", "binary_sensor", "consumable", device_class="problem"),
    EntitySpec("mock_consumable_device_consumable_type", "Consumable Type", "sensor", "consumable", icon="mdi:filter"),

    # Calendar/date schedule coverage.
    EntitySpec("mock_calendar_device_last_completed", "Last Completed", "sensor", "calendar", device_class="timestamp"),
    EntitySpec("mock_calendar_device_next_due", "Next Due", "sensor", "calendar", device_class="timestamp"),
    EntitySpec("mock_calendar_device_due_today", "Due Today", "binary_sensor", "calendar", device_class="problem"),
    EntitySpec("mock_calendar_device_overdue", "Overdue", "binary_sensor", "calendar", device_class="problem"),
    EntitySpec("mock_calendar_device_day_of_month", "Day of Month", "sensor", "calendar", state_class="measurement", icon="mdi:calendar-today"),
    EntitySpec("mock_calendar_device_week_of_year", "Week of Year", "sensor", "calendar", state_class="measurement", icon="mdi:calendar-week"),

    # Event-like coverage using stable sensors and binaries.
    EntitySpec("mock_event_device_cycle_complete", "Cycle Complete", "binary_sensor", "event"),
    EntitySpec("mock_event_device_fault_occurred", "Fault Occurred", "binary_sensor", "event", device_class="problem"),
    EntitySpec("mock_event_device_last_event", "Last Event", "sensor", "event", icon="mdi:calendar-clock"),
    EntitySpec("mock_event_device_event_count", "Event Count", "sensor", "event", state_class="total_increasing", icon="mdi:counter"),
    EntitySpec("mock_event_device_last_event_time", "Last Event Time", "sensor", "event", device_class="timestamp"),

    # Boolean state coverage.
    EntitySpec("mock_binary_device_on_off", "On Off", "binary_sensor", "binary"),
    EntitySpec("mock_binary_device_opening", "Opening", "binary_sensor", "binary", device_class="opening"),
    EntitySpec("mock_binary_device_moisture", "Moisture", "binary_sensor", "binary", device_class="moisture"),
    EntitySpec("mock_binary_device_connectivity", "Connectivity", "binary_sensor", "binary", device_class="connectivity"),
    EntitySpec("mock_binary_device_problem", "Problem", "binary_sensor", "binary", device_class="problem"),
    EntitySpec("mock_binary_device_safety", "Safety", "binary_sensor", "binary", device_class="safety"),

    # Enum/text state coverage.
    EntitySpec("mock_enum_status_device_status", "Status", "sensor", "enum", icon="mdi:list-status"),
    EntitySpec("mock_enum_status_device_mode", "Mode", "sensor", "enum", icon="mdi:tune"),
    EntitySpec("mock_enum_status_device_health", "Health", "sensor", "enum", icon="mdi:heart-pulse"),
    EntitySpec("mock_enum_status_device_service_state", "Service State", "sensor", "enum", icon="mdi:wrench"),

    # Fault injection and bad data coverage.
    EntitySpec("mock_fault_device_unknown_state", "Unknown State", "sensor", "fault", icon="mdi:help-circle"),
    EntitySpec("mock_fault_device_unavailable_state", "Unavailable State", "sensor", "fault", icon="mdi:cloud-off-outline"),
    EntitySpec("mock_fault_device_negative_duration", "Negative Duration", "sensor", "fault", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("mock_fault_device_zero_value", "Zero Value", "sensor", "fault", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("mock_fault_device_spiky_power", "Spiky Power", "sensor", "fault", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("mock_fault_device_stale_timestamp", "Stale Timestamp", "sensor", "fault", device_class="timestamp"),
    EntitySpec("mock_fault_device_unit_mismatch_value", "Unit Mismatch Value", "sensor", "fault", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("mock_fault_device_error_status", "Error Status", "sensor", "fault", icon="mdi:alert"),
]

# Equipment demo devices. These intentionally overlap with generic coverage while
# using real-world names that are easier to reason about during manual QA.
BASE_ENTITY_SPECS += [
    EntitySpec("synthetic_generator_running", "Running", "binary_sensor", "generator", device_class="running"),
    EntitySpec("synthetic_generator_runtime_hours", "Runtime Hours", "sensor", "generator", unit="h", device_class="duration", state_class="total_increasing"),
    EntitySpec("synthetic_generator_power", "Power", "sensor", "generator", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_generator_energy", "Energy", "sensor", "generator", unit="kWh", device_class="energy", state_class="total_increasing"),
    EntitySpec("synthetic_generator_cycle_count", "Cycle Count", "sensor", "generator", state_class="total_increasing", icon="mdi:counter"),
    EntitySpec("synthetic_generator_service_due", "Service Due", "binary_sensor", "generator", device_class="problem"),
    EntitySpec("synthetic_generator_service_status", "Service Status", "sensor", "generator", icon="mdi:wrench"),
    EntitySpec("synthetic_generator_service_remaining_hours", "Service Remaining Hours", "sensor", "generator", unit="h", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_generator_service_due_date", "Service Due Date", "sensor", "generator", device_class="timestamp"),
    EntitySpec("synthetic_ups_online", "Online", "binary_sensor", "ups", device_class="connectivity"),
    EntitySpec("synthetic_ups_load", "Load", "sensor", "ups", unit="%", state_class="measurement"),
    EntitySpec("synthetic_ups_battery", "Battery", "sensor", "ups", unit="%", device_class="battery", state_class="measurement"),
    EntitySpec("synthetic_ups_runtime_remaining", "Runtime Remaining", "sensor", "ups", unit="min", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_ups_battery_replacement_due", "Battery Replacement Due", "binary_sensor", "ups", device_class="problem"),
    EntitySpec("synthetic_ups_battery_remaining_days", "Battery Remaining Days", "sensor", "ups", unit="d", device_class="duration", state_class="measurement"),
    EntitySpec("synthetic_ups_self_test_status", "Self Test Status", "sensor", "ups", icon="mdi:clipboard-check"),
    EntitySpec("synthetic_pool_pump_running", "Running", "binary_sensor", "pool_pump", device_class="running"),
    EntitySpec("synthetic_pool_pump_power", "Power", "sensor", "pool_pump", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_energy", "Energy", "sensor", "pool_pump", unit="kWh", device_class="energy", state_class="total_increasing"),
    EntitySpec("synthetic_pool_pump_runtime_hours", "Runtime Hours", "sensor", "pool_pump", unit="h", device_class="duration", state_class="total_increasing"),
    EntitySpec("synthetic_pool_pump_flow_gpm", "Flow GPM", "sensor", "pool_pump", unit="gal/min", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_flow_lpm", "Flow LPM", "sensor", "pool_pump", unit="L/min", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_pressure_psi", "Pressure PSI", "sensor", "pool_pump", unit="psi", device_class="pressure", state_class="measurement"),
    EntitySpec("synthetic_pool_pump_filter_service_due", "Filter Service Due", "binary_sensor", "pool_pump", device_class="problem"),
    EntitySpec("synthetic_pool_pump_filter_remaining_percent", "Filter Remaining Percent", "sensor", "pool_pump", unit="%", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_life_remaining", "Life Remaining", "sensor", "hvac_filter", unit="%", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_used_percent", "Used Percent", "sensor", "hvac_filter", unit="%", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_airflow_cfm", "Airflow", "sensor", "hvac_filter", unit="ft³/min", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_pressure_drop", "Pressure Drop", "sensor", "hvac_filter", unit="Pa", device_class="pressure", state_class="measurement"),
    EntitySpec("synthetic_hvac_filter_service_due", "Service Due", "binary_sensor", "hvac_filter", device_class="problem"),
    EntitySpec("synthetic_water_filter_gallons_used", "Gallons Used", "sensor", "water_filter", unit="gal", device_class="volume", state_class="total_increasing"),
    EntitySpec("synthetic_water_filter_gallons_remaining", "Gallons Remaining", "sensor", "water_filter", unit="gal", device_class="volume", state_class="measurement"),
    EntitySpec("synthetic_water_filter_liters_remaining", "Liters Remaining", "sensor", "water_filter", unit="L", device_class="volume", state_class="measurement"),
    EntitySpec("synthetic_water_filter_service_due", "Service Due", "binary_sensor", "water_filter", device_class="problem"),
    EntitySpec("synthetic_energy_meter_power_w", "Power W", "sensor", "energy_meter", unit="W", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_energy_meter_power_kw", "Power kW", "sensor", "energy_meter", unit="kW", device_class="power", state_class="measurement"),
    EntitySpec("synthetic_energy_meter_total_kwh", "Total kWh", "sensor", "energy_meter", unit="kWh", device_class="energy", state_class="total_increasing"),
    EntitySpec("synthetic_energy_meter_session_kwh", "Session kWh", "sensor", "energy_meter", unit="kWh", device_class="energy", state_class="measurement"),
    EntitySpec("synthetic_environment_temperature_f", "Temperature F", "sensor", "environment", unit="°F", device_class="temperature", state_class="measurement"),
    EntitySpec("synthetic_environment_temperature_c", "Temperature C", "sensor", "environment", unit="°C", device_class="temperature", state_class="measurement"),
    EntitySpec("synthetic_environment_humidity", "Humidity", "sensor", "environment", unit="%", device_class="humidity", state_class="measurement"),
    EntitySpec("synthetic_environment_pressure_pa", "Pressure Pa", "sensor", "environment", unit="Pa", device_class="pressure", state_class="measurement"),
]

ENTITY_SPECS: tuple[EntitySpec, ...] = tuple(
    BASE_ENTITY_SPECS + sum([common_entities(d.key) for d in DEVICES if d.key != "console"], [])
)
