from src.settings.settings_view.schema import SettingField, SettingGroup

SPRAY_GROUP = SettingGroup("Spray Settings", [
    SettingField("spray_width", "Spray Width", "double_spinbox", default=8.0, min_val=0, max_val=100, decimals=1, suffix=" mm", step=0.1, step_options=[0.1, 1, 5]),
    SettingField("spraying_height", "Spraying Height", "double_spinbox", default=10.0, min_val=0, max_val=100, decimals=1, suffix=" mm", step=0.1, step_options=[0.1, 1, 5]),
    SettingField("fan_speed", "Fan Speed", "double_spinbox", default=50.0, min_val=0, max_val=100, decimals=1, suffix=" %", step=1, step_options=[1, 5, 10]),
    SettingField("rz_angle", "RZ Angle", "spinbox", default=0, min_val=-180, max_val=180, suffix=" °", step=1, step_options=[1, 5, 10]),
    SettingField("spray_on", "Spray On", "toggle", default=False),
])

PUMP_GROUP = SettingGroup("Pump Settings", [
    SettingField("pump_speed", "Pump Speed", "double_spinbox", default=1000.0, min_val=0, max_val=10000, decimals=1, suffix=" rpm", step=10, step_options=[10, 50, 100]),
    SettingField("pump_reverse_time", "Pump Reverse Time", "double_spinbox", default=1.0, min_val=0, max_val=60, decimals=1, suffix=" s", step=0.1, step_options=[0.1, 1, 5]),
    SettingField("pump_speed_reverse", "Pump Speed Reverse", "double_spinbox", default=1000.0, min_val=0, max_val=10000, decimals=1, suffix=" rpm", step=10, step_options=[10, 50, 100]),
])

GENERATOR_GROUP = SettingGroup("Generator Settings", [
    SettingField("generator_glue_delay", "Generator-Glue Delay", "spinbox", default=1, min_val=0, max_val=100, suffix=" ms", step=1, step_options=[1, 5, 10]),
    SettingField("generator_timeout", "Generator Timeout", "double_spinbox", default=5.0, min_val=0, max_val=60, decimals=1, suffix=" s", step=0.1, step_options=[0.1, 1, 5]),
    SettingField("glue_type", "Glue Type", "combo", default="Type A", choices=["Type A", "Type B", "Type C"]),
])

TIMING_GROUP = SettingGroup("Timing Settings", [
    SettingField("time_before_motion", "Time Before Motion", "double_spinbox", default=1.0, min_val=0, max_val=60, decimals=1, suffix=" s", step=0.1, step_options=[0.1, 1, 5]),
    SettingField("time_before_stop", "Time Before Stop", "spinbox", default=1, min_val=0, max_val=100, suffix=" s", step=1, step_options=[1, 5, 10]),
    SettingField("reach_start_threshold", "Reach Start Threshold", "spinbox", default=1, min_val=0, max_val=100, step=1, step_options=[1, 5, 10]),
    SettingField("reach_end_threshold", "Reach End Threshold", "spinbox", default=1, min_val=0, max_val=100, step=1, step_options=[1, 5, 10]),
])

RAMP_GROUP = SettingGroup("Ramp Settings", [
    SettingField("initial_ramp_speed", "Initial Ramp Speed", "double_spinbox", default=5000.0, min_val=0, max_val=10000, decimals=1, suffix=" rpm", step=100, step_options=[100, 500, 1000]),
    SettingField("forward_ramp_steps", "Forward Ramp Steps", "spinbox", default=1, min_val=0, max_val=100, step=1, step_options=[1, 5, 10]),
    SettingField("reverse_ramp_steps", "Reverse Ramp Steps", "spinbox", default=1, min_val=0, max_val=100, step=1, step_options=[1, 5, 10]),
    SettingField("initial_ramp_speed_duration", "Initial Ramp Speed Duration", "spinbox", default=1, min_val=0, max_val=100, suffix=" ms", step=1, step_options=[1, 5, 10]),
])
