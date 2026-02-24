from src.plugins.glue_settings.glue_settings_data import GlueSettings


class GlueSettingsMapper:
    @staticmethod
    def to_flat_dict(settings: GlueSettings) -> dict:
        return {
            "spray_width": settings.spray_width,
            "spraying_height": settings.spraying_height,
            "fan_speed": settings.fan_speed,
            "generator_glue_delay": settings.generator_glue_delay,
            "pump_speed": settings.pump_speed,
            "pump_reverse_time": settings.pump_reverse_time,
            "pump_speed_reverse": settings.pump_speed_reverse,
            "rz_angle": settings.rz_angle,
            "glue_type": settings.glue_type,
            "generator_timeout": settings.generator_timeout,
            "time_before_motion": settings.time_before_motion,
            "reach_start_threshold": settings.reach_start_threshold,
            "time_before_stop": settings.time_before_stop,
            "reach_end_threshold": settings.reach_end_threshold,
            "initial_ramp_speed": settings.initial_ramp_speed,
            "forward_ramp_steps": settings.forward_ramp_steps,
            "reverse_ramp_steps": settings.reverse_ramp_steps,
            "initial_ramp_speed_duration": settings.initial_ramp_speed_duration,
            "spray_on": settings.spray_on,
        }

    @staticmethod
    def from_flat_dict(flat: dict, base: GlueSettings) -> GlueSettings:
        from copy import deepcopy
        s = deepcopy(base)

        s.spray_width = float(flat.get("spray_width", s.spray_width))
        s.spraying_height = float(flat.get("spraying_height", s.spraying_height))
        s.fan_speed = float(flat.get("fan_speed", s.fan_speed))
        s.generator_glue_delay = int(flat.get("generator_glue_delay", s.generator_glue_delay))
        s.pump_speed = float(flat.get("pump_speed", s.pump_speed))
        s.pump_reverse_time = float(flat.get("pump_reverse_time", s.pump_reverse_time))
        s.pump_speed_reverse = float(flat.get("pump_speed_reverse", s.pump_speed_reverse))
        s.rz_angle = int(flat.get("rz_angle", s.rz_angle))
        s.glue_type = flat.get("glue_type", s.glue_type)
        s.generator_timeout = float(flat.get("generator_timeout", s.generator_timeout))
        s.time_before_motion = float(flat.get("time_before_motion", s.time_before_motion))
        s.reach_start_threshold = int(flat.get("reach_start_threshold", s.reach_start_threshold))
        s.time_before_stop = int(flat.get("time_before_stop", s.time_before_stop))
        s.reach_end_threshold = int(flat.get("reach_end_threshold", s.reach_end_threshold))
        s.initial_ramp_speed = float(flat.get("initial_ramp_speed", s.initial_ramp_speed))
        s.forward_ramp_steps = int(flat.get("forward_ramp_steps", s.forward_ramp_steps))
        s.reverse_ramp_steps = int(flat.get("reverse_ramp_steps", s.reverse_ramp_steps))
        s.initial_ramp_speed_duration = int(flat.get("initial_ramp_speed_duration", s.initial_ramp_speed_duration))
        s.spray_on = bool(flat.get("spray_on", s.spray_on))

        return s
