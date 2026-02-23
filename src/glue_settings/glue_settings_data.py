from dataclasses import dataclass


@dataclass
class GlueSettings:
    spray_width: float = 8.0
    spraying_height: float = 10.0
    fan_speed: float = 50.0
    generator_glue_delay: int = 1
    pump_speed: float = 1000.0
    pump_reverse_time: float = 1.0
    pump_speed_reverse: float = 1000.0
    rz_angle: int = 0
    glue_type: str = "Type A"
    generator_timeout: float = 5.0
    time_before_motion: float = 1.0
    reach_start_threshold: int = 1
    time_before_stop: int = 1
    reach_end_threshold: int = 1
    initial_ramp_speed: float = 5000.0
    forward_ramp_steps: int = 1
    reverse_ramp_steps: int = 1
    initial_ramp_speed_duration: int = 1
    spray_on: bool = False
