# Entity Catalog

Stable entity IDs are part of the QA contract. Avoid renaming them once released.

| Entity ID | Platform | Device | Unit | Device class | State class |
|---|---|---|---|---|---|
| `select.mock_qa_console_profile` | select | Mock QA Console |  |  |  |
| `number.mock_qa_console_speed_multiplier` | number | Mock QA Console | x |  |  |
| `switch.mock_qa_console_automatic_faults` | switch | Mock QA Console |  |  |  |
| `button.mock_qa_console_reset_all` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_reset_runtime` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_reset_meters` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_reset_service_due` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_trigger_service_due` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_trigger_service_overdue` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_force_bad_data` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_force_cycle` | button | Mock QA Console |  |  |  |
| `button.mock_qa_console_seed_known_state` | button | Mock QA Console |  |  |  |
| `sensor.mock_qa_console_tick` | sensor | Mock QA Console |  |  | total_increasing |
| `sensor.mock_qa_console_simulated_time` | sensor | Mock QA Console |  | timestamp |  |
| `binary_sensor.mock_runtime_device_running` | binary_sensor | Mock Runtime Device |  | running |  |
| `binary_sensor.mock_runtime_device_idle` | binary_sensor | Mock Runtime Device |  |  |  |
| `binary_sensor.mock_runtime_device_power_running` | binary_sensor | Mock Runtime Device |  | running |  |
| `sensor.mock_runtime_device_runtime_seconds` | sensor | Mock Runtime Device | s | duration | total_increasing |
| `sensor.mock_runtime_device_runtime_minutes` | sensor | Mock Runtime Device | min | duration | total_increasing |
| `sensor.mock_runtime_device_runtime_hours` | sensor | Mock Runtime Device | h | duration | total_increasing |
| `sensor.mock_runtime_device_runtime_days` | sensor | Mock Runtime Device | d | duration | total_increasing |
| `sensor.mock_runtime_device_session_seconds` | sensor | Mock Runtime Device | s | duration | measurement |
| `sensor.mock_runtime_device_session_minutes` | sensor | Mock Runtime Device | min | duration | measurement |
| `sensor.mock_runtime_device_power_w` | sensor | Mock Runtime Device | W | power | measurement |
| `sensor.mock_runtime_device_power_kw` | sensor | Mock Runtime Device | kW | power | measurement |
| `sensor.mock_runtime_device_cycle_count` | sensor | Mock Runtime Device |  |  | total_increasing |
| `sensor.mock_meter_device_total_count` | sensor | Mock Meter Device |  |  | total_increasing |
| `sensor.mock_meter_device_session_count` | sensor | Mock Meter Device |  |  | measurement |
| `sensor.mock_meter_device_total_cycles` | sensor | Mock Meter Device | cycles |  | total_increasing |
| `sensor.mock_meter_device_session_cycles` | sensor | Mock Meter Device | cycles |  | measurement |
| `sensor.mock_meter_device_total_gallons` | sensor | Mock Meter Device | gal | volume | total_increasing |
| `sensor.mock_meter_device_session_gallons` | sensor | Mock Meter Device | gal | volume | measurement |
| `sensor.mock_meter_device_total_liters` | sensor | Mock Meter Device | L | volume | total_increasing |
| `sensor.mock_meter_device_total_kwh` | sensor | Mock Meter Device | kWh | energy | total_increasing |
| `sensor.mock_meter_device_session_kwh` | sensor | Mock Meter Device | kWh | energy | measurement |
| `sensor.mock_meter_device_total_cubic_feet` | sensor | Mock Meter Device | ft³ | volume | total_increasing |
| `binary_sensor.mock_service_device_service_due` | binary_sensor | Mock Service Device |  | problem |  |
| `binary_sensor.mock_service_device_service_overdue` | binary_sensor | Mock Service Device |  | problem |  |
| `sensor.mock_service_device_service_status` | sensor | Mock Service Device |  |  |  |
| `sensor.mock_service_device_remaining_seconds` | sensor | Mock Service Device | s | duration | measurement |
| `sensor.mock_service_device_remaining_minutes` | sensor | Mock Service Device | min | duration | measurement |
| `sensor.mock_service_device_remaining_hours` | sensor | Mock Service Device | h | duration | measurement |
| `sensor.mock_service_device_remaining_days` | sensor | Mock Service Device | d | duration | measurement |
| `sensor.mock_service_device_remaining_cycles` | sensor | Mock Service Device | cycles |  | measurement |
| `sensor.mock_service_device_used_percent` | sensor | Mock Service Device | % |  | measurement |
| `sensor.mock_service_device_remaining_percent` | sensor | Mock Service Device | % |  | measurement |
| `sensor.mock_service_device_due_date` | sensor | Mock Service Device |  | timestamp |  |
| `sensor.mock_service_device_last_completed` | sensor | Mock Service Device |  | timestamp |  |
| `sensor.mock_service_device_reason` | sensor | Mock Service Device |  |  |  |
| `sensor.mock_environmental_device_temperature_f` | sensor | Mock Environmental Device | °F | temperature | measurement |
| `sensor.mock_environmental_device_temperature_c` | sensor | Mock Environmental Device | °C | temperature | measurement |
| `sensor.mock_environmental_device_humidity` | sensor | Mock Environmental Device | % | humidity | measurement |
| `sensor.mock_environmental_device_pressure_pa` | sensor | Mock Environmental Device | Pa | pressure | measurement |
| `sensor.mock_environmental_device_pressure_psi` | sensor | Mock Environmental Device | psi | pressure | measurement |
| `sensor.mock_environmental_device_illuminance` | sensor | Mock Environmental Device | lx | illuminance | measurement |
| `sensor.mock_environmental_device_signal_strength` | sensor | Mock Environmental Device | dBm | signal_strength | measurement |
| `sensor.mock_environmental_device_battery` | sensor | Mock Environmental Device | % | battery | measurement |
| `sensor.mock_flow_device_flow_gpm` | sensor | Mock Flow Device | gal/min |  | measurement |
| `sensor.mock_flow_device_flow_lpm` | sensor | Mock Flow Device | L/min |  | measurement |
| `sensor.mock_flow_device_airflow_cfm` | sensor | Mock Flow Device | ft³/min |  | measurement |
| `sensor.mock_flow_device_pressure_in` | sensor | Mock Flow Device | psi | pressure | measurement |
| `sensor.mock_flow_device_pressure_out` | sensor | Mock Flow Device | psi | pressure | measurement |
| `sensor.mock_flow_device_pressure_drop_pa` | sensor | Mock Flow Device | Pa | pressure | measurement |
| `sensor.mock_flow_device_total_volume_gal` | sensor | Mock Flow Device | gal | volume | total_increasing |
| `sensor.mock_distance_device_distance_ft` | sensor | Mock Distance Device | ft | distance | measurement |
| `sensor.mock_distance_device_distance_m` | sensor | Mock Distance Device | m | distance | measurement |
| `sensor.mock_distance_device_total_miles` | sensor | Mock Distance Device | mi | distance | total_increasing |
| `sensor.mock_distance_device_total_km` | sensor | Mock Distance Device | km | distance | total_increasing |
| `sensor.mock_distance_device_session_feet` | sensor | Mock Distance Device | ft | distance | measurement |
| `sensor.mock_consumable_device_life_remaining_percent` | sensor | Mock Consumable Device | % |  | measurement |
| `sensor.mock_consumable_device_life_used_percent` | sensor | Mock Consumable Device | % |  | measurement |
| `sensor.mock_consumable_device_days_remaining` | sensor | Mock Consumable Device | d | duration | measurement |
| `sensor.mock_consumable_device_hours_remaining` | sensor | Mock Consumable Device | h | duration | measurement |
| `binary_sensor.mock_consumable_device_replacement_due` | binary_sensor | Mock Consumable Device |  | problem |  |
| `sensor.mock_consumable_device_consumable_type` | sensor | Mock Consumable Device |  |  |  |
| `sensor.mock_calendar_device_last_completed` | sensor | Mock Calendar Device |  | timestamp |  |
| `sensor.mock_calendar_device_next_due` | sensor | Mock Calendar Device |  | timestamp |  |
| `binary_sensor.mock_calendar_device_due_today` | binary_sensor | Mock Calendar Device |  | problem |  |
| `binary_sensor.mock_calendar_device_overdue` | binary_sensor | Mock Calendar Device |  | problem |  |
| `sensor.mock_calendar_device_day_of_month` | sensor | Mock Calendar Device |  |  | measurement |
| `sensor.mock_calendar_device_week_of_year` | sensor | Mock Calendar Device |  |  | measurement |
| `binary_sensor.mock_event_device_cycle_complete` | binary_sensor | Mock Event Device |  |  |  |
| `binary_sensor.mock_event_device_fault_occurred` | binary_sensor | Mock Event Device |  | problem |  |
| `sensor.mock_event_device_last_event` | sensor | Mock Event Device |  |  |  |
| `sensor.mock_event_device_event_count` | sensor | Mock Event Device |  |  | total_increasing |
| `sensor.mock_event_device_last_event_time` | sensor | Mock Event Device |  | timestamp |  |
| `binary_sensor.mock_binary_device_on_off` | binary_sensor | Mock Binary Device |  |  |  |
| `binary_sensor.mock_binary_device_opening` | binary_sensor | Mock Binary Device |  | opening |  |
| `binary_sensor.mock_binary_device_moisture` | binary_sensor | Mock Binary Device |  | moisture |  |
| `binary_sensor.mock_binary_device_connectivity` | binary_sensor | Mock Binary Device |  | connectivity |  |
| `binary_sensor.mock_binary_device_problem` | binary_sensor | Mock Binary Device |  | problem |  |
| `binary_sensor.mock_binary_device_safety` | binary_sensor | Mock Binary Device |  | safety |  |
| `sensor.mock_enum_status_device_status` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_enum_status_device_mode` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_enum_status_device_health` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_enum_status_device_service_state` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_fault_device_unknown_state` | sensor | Mock Fault Device |  |  |  |
| `sensor.mock_fault_device_unavailable_state` | sensor | Mock Fault Device |  |  |  |
| `sensor.mock_fault_device_negative_duration` | sensor | Mock Fault Device | h | duration | measurement |
| `sensor.mock_fault_device_zero_value` | sensor | Mock Fault Device | h | duration | measurement |
| `sensor.mock_fault_device_spiky_power` | sensor | Mock Fault Device | W | power | measurement |
| `sensor.mock_fault_device_stale_timestamp` | sensor | Mock Fault Device |  | timestamp |  |
| `sensor.mock_fault_device_unit_mismatch_value` | sensor | Mock Fault Device | h | duration | measurement |
| `sensor.mock_fault_device_error_status` | sensor | Mock Fault Device |  |  |  |
| `binary_sensor.synthetic_generator_running` | binary_sensor | Synthetic Generator |  | running |  |
| `sensor.synthetic_generator_runtime_hours` | sensor | Synthetic Generator | h | duration | total_increasing |
| `sensor.synthetic_generator_power` | sensor | Synthetic Generator | W | power | measurement |
| `sensor.synthetic_generator_energy` | sensor | Synthetic Generator | kWh | energy | total_increasing |
| `sensor.synthetic_generator_cycle_count` | sensor | Synthetic Generator |  |  | total_increasing |
| `binary_sensor.synthetic_generator_service_due` | binary_sensor | Synthetic Generator |  | problem |  |
| `sensor.synthetic_generator_service_status` | sensor | Synthetic Generator |  |  |  |
| `sensor.synthetic_generator_service_remaining_hours` | sensor | Synthetic Generator | h | duration | measurement |
| `sensor.synthetic_generator_service_due_date` | sensor | Synthetic Generator |  | timestamp |  |
| `binary_sensor.synthetic_ups_online` | binary_sensor | Synthetic UPS |  | connectivity |  |
| `sensor.synthetic_ups_load` | sensor | Synthetic UPS | % |  | measurement |
| `sensor.synthetic_ups_battery` | sensor | Synthetic UPS | % | battery | measurement |
| `sensor.synthetic_ups_runtime_remaining` | sensor | Synthetic UPS | min | duration | measurement |
| `binary_sensor.synthetic_ups_battery_replacement_due` | binary_sensor | Synthetic UPS |  | problem |  |
| `sensor.synthetic_ups_battery_remaining_days` | sensor | Synthetic UPS | d | duration | measurement |
| `sensor.synthetic_ups_self_test_status` | sensor | Synthetic UPS |  |  |  |
| `binary_sensor.synthetic_pool_pump_running` | binary_sensor | Synthetic Pool Pump |  | running |  |
| `sensor.synthetic_pool_pump_power` | sensor | Synthetic Pool Pump | W | power | measurement |
| `sensor.synthetic_pool_pump_energy` | sensor | Synthetic Pool Pump | kWh | energy | total_increasing |
| `sensor.synthetic_pool_pump_runtime_hours` | sensor | Synthetic Pool Pump | h | duration | total_increasing |
| `sensor.synthetic_pool_pump_flow_gpm` | sensor | Synthetic Pool Pump | gal/min |  | measurement |
| `sensor.synthetic_pool_pump_flow_lpm` | sensor | Synthetic Pool Pump | L/min |  | measurement |
| `sensor.synthetic_pool_pump_pressure_psi` | sensor | Synthetic Pool Pump | psi | pressure | measurement |
| `binary_sensor.synthetic_pool_pump_filter_service_due` | binary_sensor | Synthetic Pool Pump |  | problem |  |
| `sensor.synthetic_pool_pump_filter_remaining_percent` | sensor | Synthetic Pool Pump | % |  | measurement |
| `sensor.synthetic_hvac_filter_life_remaining` | sensor | Synthetic HVAC Filter | % |  | measurement |
| `sensor.synthetic_hvac_filter_used_percent` | sensor | Synthetic HVAC Filter | % |  | measurement |
| `sensor.synthetic_hvac_filter_airflow_cfm` | sensor | Synthetic HVAC Filter | ft³/min |  | measurement |
| `sensor.synthetic_hvac_filter_pressure_drop` | sensor | Synthetic HVAC Filter | Pa | pressure | measurement |
| `binary_sensor.synthetic_hvac_filter_service_due` | binary_sensor | Synthetic HVAC Filter |  | problem |  |
| `sensor.synthetic_water_filter_gallons_used` | sensor | Synthetic Water Filter | gal | volume | total_increasing |
| `sensor.synthetic_water_filter_gallons_remaining` | sensor | Synthetic Water Filter | gal | volume | measurement |
| `sensor.synthetic_water_filter_liters_remaining` | sensor | Synthetic Water Filter | L | volume | measurement |
| `binary_sensor.synthetic_water_filter_service_due` | binary_sensor | Synthetic Water Filter |  | problem |  |
| `sensor.synthetic_energy_meter_power_w` | sensor | Synthetic Energy Meter | W | power | measurement |
| `sensor.synthetic_energy_meter_power_kw` | sensor | Synthetic Energy Meter | kW | power | measurement |
| `sensor.synthetic_energy_meter_total_kwh` | sensor | Synthetic Energy Meter | kWh | energy | total_increasing |
| `sensor.synthetic_energy_meter_session_kwh` | sensor | Synthetic Energy Meter | kWh | energy | measurement |
| `sensor.synthetic_environment_temperature_f` | sensor | Synthetic Environment Station | °F | temperature | measurement |
| `sensor.synthetic_environment_temperature_c` | sensor | Synthetic Environment Station | °C | temperature | measurement |
| `sensor.synthetic_environment_humidity` | sensor | Synthetic Environment Station | % | humidity | measurement |
| `sensor.synthetic_environment_pressure_pa` | sensor | Synthetic Environment Station | Pa | pressure | measurement |
| `sensor.mock_runtime_device_firmware_version` | sensor | Mock Runtime Device |  |  |  |
| `sensor.mock_runtime_device_hardware_revision` | sensor | Mock Runtime Device |  |  |  |
| `sensor.mock_runtime_device_serial_number` | sensor | Mock Runtime Device |  |  |  |
| `sensor.mock_runtime_device_last_service_date` | sensor | Mock Runtime Device |  | timestamp |  |
| `sensor.mock_runtime_device_service_count` | sensor | Mock Runtime Device |  |  | total_increasing |
| `sensor.mock_runtime_device_service_reason` | sensor | Mock Runtime Device |  |  |  |
| `sensor.mock_meter_device_firmware_version` | sensor | Mock Meter Device |  |  |  |
| `sensor.mock_meter_device_hardware_revision` | sensor | Mock Meter Device |  |  |  |
| `sensor.mock_meter_device_serial_number` | sensor | Mock Meter Device |  |  |  |
| `sensor.mock_meter_device_last_service_date` | sensor | Mock Meter Device |  | timestamp |  |
| `sensor.mock_meter_device_service_count` | sensor | Mock Meter Device |  |  | total_increasing |
| `sensor.mock_meter_device_service_reason` | sensor | Mock Meter Device |  |  |  |
| `sensor.mock_service_device_firmware_version` | sensor | Mock Service Device |  |  |  |
| `sensor.mock_service_device_hardware_revision` | sensor | Mock Service Device |  |  |  |
| `sensor.mock_service_device_serial_number` | sensor | Mock Service Device |  |  |  |
| `sensor.mock_service_device_last_service_date` | sensor | Mock Service Device |  | timestamp |  |
| `sensor.mock_service_device_service_count` | sensor | Mock Service Device |  |  | total_increasing |
| `sensor.mock_service_device_service_reason` | sensor | Mock Service Device |  |  |  |
| `sensor.mock_environmental_device_firmware_version` | sensor | Mock Environmental Device |  |  |  |
| `sensor.mock_environmental_device_hardware_revision` | sensor | Mock Environmental Device |  |  |  |
| `sensor.mock_environmental_device_serial_number` | sensor | Mock Environmental Device |  |  |  |
| `sensor.mock_environmental_device_last_service_date` | sensor | Mock Environmental Device |  | timestamp |  |
| `sensor.mock_environmental_device_service_count` | sensor | Mock Environmental Device |  |  | total_increasing |
| `sensor.mock_environmental_device_service_reason` | sensor | Mock Environmental Device |  |  |  |
| `sensor.mock_flow_device_firmware_version` | sensor | Mock Flow Device |  |  |  |
| `sensor.mock_flow_device_hardware_revision` | sensor | Mock Flow Device |  |  |  |
| `sensor.mock_flow_device_serial_number` | sensor | Mock Flow Device |  |  |  |
| `sensor.mock_flow_device_last_service_date` | sensor | Mock Flow Device |  | timestamp |  |
| `sensor.mock_flow_device_service_count` | sensor | Mock Flow Device |  |  | total_increasing |
| `sensor.mock_flow_device_service_reason` | sensor | Mock Flow Device |  |  |  |
| `sensor.mock_distance_device_firmware_version` | sensor | Mock Distance Device |  |  |  |
| `sensor.mock_distance_device_hardware_revision` | sensor | Mock Distance Device |  |  |  |
| `sensor.mock_distance_device_serial_number` | sensor | Mock Distance Device |  |  |  |
| `sensor.mock_distance_device_last_service_date` | sensor | Mock Distance Device |  | timestamp |  |
| `sensor.mock_distance_device_service_count` | sensor | Mock Distance Device |  |  | total_increasing |
| `sensor.mock_distance_device_service_reason` | sensor | Mock Distance Device |  |  |  |
| `sensor.mock_consumable_device_firmware_version` | sensor | Mock Consumable Device |  |  |  |
| `sensor.mock_consumable_device_hardware_revision` | sensor | Mock Consumable Device |  |  |  |
| `sensor.mock_consumable_device_serial_number` | sensor | Mock Consumable Device |  |  |  |
| `sensor.mock_consumable_device_last_service_date` | sensor | Mock Consumable Device |  | timestamp |  |
| `sensor.mock_consumable_device_service_count` | sensor | Mock Consumable Device |  |  | total_increasing |
| `sensor.mock_consumable_device_service_reason` | sensor | Mock Consumable Device |  |  |  |
| `sensor.mock_calendar_device_firmware_version` | sensor | Mock Calendar Device |  |  |  |
| `sensor.mock_calendar_device_hardware_revision` | sensor | Mock Calendar Device |  |  |  |
| `sensor.mock_calendar_device_serial_number` | sensor | Mock Calendar Device |  |  |  |
| `sensor.mock_calendar_device_last_service_date` | sensor | Mock Calendar Device |  | timestamp |  |
| `sensor.mock_calendar_device_service_count` | sensor | Mock Calendar Device |  |  | total_increasing |
| `sensor.mock_calendar_device_service_reason` | sensor | Mock Calendar Device |  |  |  |
| `sensor.mock_event_device_firmware_version` | sensor | Mock Event Device |  |  |  |
| `sensor.mock_event_device_hardware_revision` | sensor | Mock Event Device |  |  |  |
| `sensor.mock_event_device_serial_number` | sensor | Mock Event Device |  |  |  |
| `sensor.mock_event_device_last_service_date` | sensor | Mock Event Device |  | timestamp |  |
| `sensor.mock_event_device_service_count` | sensor | Mock Event Device |  |  | total_increasing |
| `sensor.mock_event_device_service_reason` | sensor | Mock Event Device |  |  |  |
| `sensor.mock_binary_device_firmware_version` | sensor | Mock Binary Device |  |  |  |
| `sensor.mock_binary_device_hardware_revision` | sensor | Mock Binary Device |  |  |  |
| `sensor.mock_binary_device_serial_number` | sensor | Mock Binary Device |  |  |  |
| `sensor.mock_binary_device_last_service_date` | sensor | Mock Binary Device |  | timestamp |  |
| `sensor.mock_binary_device_service_count` | sensor | Mock Binary Device |  |  | total_increasing |
| `sensor.mock_binary_device_service_reason` | sensor | Mock Binary Device |  |  |  |
| `sensor.mock_enum_status_device_firmware_version` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_enum_status_device_hardware_revision` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_enum_status_device_serial_number` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_enum_status_device_last_service_date` | sensor | Mock Enum Status Device |  | timestamp |  |
| `sensor.mock_enum_status_device_service_count` | sensor | Mock Enum Status Device |  |  | total_increasing |
| `sensor.mock_enum_status_device_service_reason` | sensor | Mock Enum Status Device |  |  |  |
| `sensor.mock_fault_device_firmware_version` | sensor | Mock Fault Device |  |  |  |
| `sensor.mock_fault_device_hardware_revision` | sensor | Mock Fault Device |  |  |  |
| `sensor.mock_fault_device_serial_number` | sensor | Mock Fault Device |  |  |  |
| `sensor.mock_fault_device_last_service_date` | sensor | Mock Fault Device |  | timestamp |  |
| `sensor.mock_fault_device_service_count` | sensor | Mock Fault Device |  |  | total_increasing |
| `sensor.mock_fault_device_service_reason` | sensor | Mock Fault Device |  |  |  |
| `sensor.synthetic_generator_firmware_version` | sensor | Synthetic Generator |  |  |  |
| `sensor.synthetic_generator_hardware_revision` | sensor | Synthetic Generator |  |  |  |
| `sensor.synthetic_generator_serial_number` | sensor | Synthetic Generator |  |  |  |
| `sensor.synthetic_generator_last_service_date` | sensor | Synthetic Generator |  | timestamp |  |
| `sensor.synthetic_generator_service_count` | sensor | Synthetic Generator |  |  | total_increasing |
| `sensor.synthetic_generator_service_reason` | sensor | Synthetic Generator |  |  |  |
| `sensor.synthetic_ups_firmware_version` | sensor | Synthetic UPS |  |  |  |
| `sensor.synthetic_ups_hardware_revision` | sensor | Synthetic UPS |  |  |  |
| `sensor.synthetic_ups_serial_number` | sensor | Synthetic UPS |  |  |  |
| `sensor.synthetic_ups_last_service_date` | sensor | Synthetic UPS |  | timestamp |  |
| `sensor.synthetic_ups_service_count` | sensor | Synthetic UPS |  |  | total_increasing |
| `sensor.synthetic_ups_service_reason` | sensor | Synthetic UPS |  |  |  |
| `sensor.synthetic_pool_pump_firmware_version` | sensor | Synthetic Pool Pump |  |  |  |
| `sensor.synthetic_pool_pump_hardware_revision` | sensor | Synthetic Pool Pump |  |  |  |
| `sensor.synthetic_pool_pump_serial_number` | sensor | Synthetic Pool Pump |  |  |  |
| `sensor.synthetic_pool_pump_last_service_date` | sensor | Synthetic Pool Pump |  | timestamp |  |
| `sensor.synthetic_pool_pump_service_count` | sensor | Synthetic Pool Pump |  |  | total_increasing |
| `sensor.synthetic_pool_pump_service_reason` | sensor | Synthetic Pool Pump |  |  |  |
| `sensor.synthetic_hvac_filter_firmware_version` | sensor | Synthetic HVAC Filter |  |  |  |
| `sensor.synthetic_hvac_filter_hardware_revision` | sensor | Synthetic HVAC Filter |  |  |  |
| `sensor.synthetic_hvac_filter_serial_number` | sensor | Synthetic HVAC Filter |  |  |  |
| `sensor.synthetic_hvac_filter_last_service_date` | sensor | Synthetic HVAC Filter |  | timestamp |  |
| `sensor.synthetic_hvac_filter_service_count` | sensor | Synthetic HVAC Filter |  |  | total_increasing |
| `sensor.synthetic_hvac_filter_service_reason` | sensor | Synthetic HVAC Filter |  |  |  |
| `sensor.synthetic_water_filter_firmware_version` | sensor | Synthetic Water Filter |  |  |  |
| `sensor.synthetic_water_filter_hardware_revision` | sensor | Synthetic Water Filter |  |  |  |
| `sensor.synthetic_water_filter_serial_number` | sensor | Synthetic Water Filter |  |  |  |
| `sensor.synthetic_water_filter_last_service_date` | sensor | Synthetic Water Filter |  | timestamp |  |
| `sensor.synthetic_water_filter_service_count` | sensor | Synthetic Water Filter |  |  | total_increasing |
| `sensor.synthetic_water_filter_service_reason` | sensor | Synthetic Water Filter |  |  |  |
| `sensor.synthetic_energy_meter_firmware_version` | sensor | Synthetic Energy Meter |  |  |  |
| `sensor.synthetic_energy_meter_hardware_revision` | sensor | Synthetic Energy Meter |  |  |  |
| `sensor.synthetic_energy_meter_serial_number` | sensor | Synthetic Energy Meter |  |  |  |
| `sensor.synthetic_energy_meter_last_service_date` | sensor | Synthetic Energy Meter |  | timestamp |  |
| `sensor.synthetic_energy_meter_service_count` | sensor | Synthetic Energy Meter |  |  | total_increasing |
| `sensor.synthetic_energy_meter_service_reason` | sensor | Synthetic Energy Meter |  |  |  |
| `sensor.synthetic_environment_station_firmware_version` | sensor | Synthetic Environment Station |  |  |  |
| `sensor.synthetic_environment_station_hardware_revision` | sensor | Synthetic Environment Station |  |  |  |
| `sensor.synthetic_environment_station_serial_number` | sensor | Synthetic Environment Station |  |  |  |
| `sensor.synthetic_environment_station_last_service_date` | sensor | Synthetic Environment Station |  | timestamp |  |
| `sensor.synthetic_environment_station_service_count` | sensor | Synthetic Environment Station |  |  | total_increasing |
| `sensor.synthetic_environment_station_service_reason` | sensor | Synthetic Environment Station |  |  |  |
