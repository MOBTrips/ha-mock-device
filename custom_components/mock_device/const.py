"""Constants for the Mock Device integration."""

DOMAIN = "mock_device"
PLATFORMS = ["sensor", "binary_sensor", "button", "number", "select", "switch"]

CONF_SINGLE_INSTANCE_ID = "mock_device_single_instance"
DEFAULT_SCAN_INTERVAL_SECONDS = 15
DEFAULT_SPEED_MULTIPLIER = 60.0

PROFILE_NORMAL = "normal"
PROFILE_INTERMITTENT = "intermittent"
PROFILE_BAD_DATA = "bad_data"
PROFILE_FAST_FORWARD = "fast_forward"
PROFILE_LONG_CYCLE = "long_cycle"
PROFILES = [
    PROFILE_NORMAL,
    PROFILE_INTERMITTENT,
    PROFILE_BAD_DATA,
    PROFILE_FAST_FORWARD,
    PROFILE_LONG_CYCLE,
]

EVENT_STATE_SNAPSHOT = "mock_device_state_snapshot"
