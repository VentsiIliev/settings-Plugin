from src.external_dependencies.robotConfig.robotConfigModel import RobotConfig
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings


class RobotSettingsMapper:
    """The only place that knows both schema keys and RobotConfig fields.

    Converts a RobotConfig into the flat dict expected by GenericSettingGroup.set_values().
    """

    @staticmethod
    def to_flat_dict(config: RobotConfig) -> dict:
        return {
            # Robot info
            "robot_ip":    config.robot_ip,
            "robot_tool":  config.robot_tool,
            "robot_user":  config.robot_user,
            "tcp_x_offset": config.tcp_x_offset,
            "tcp_y_offset": config.tcp_y_offset,
            # Global motion settings
            "global_velocity":     config.global_motion_settings.global_velocity,
            "global_acceleration": config.global_motion_settings.global_acceleration,
            "emergency_decel":     config.global_motion_settings.emergency_decel,
            "max_jog_step":        config.global_motion_settings.max_jog_step,
            # TCP step settings
            "tcp_x_step_distance": config.tcp_x_step_distance,
            "tcp_x_step_offset":   config.tcp_x_step_offset,
            "tcp_y_step_distance": config.tcp_y_step_distance,
            "tcp_y_step_offset":   config.tcp_y_step_offset,
            # Offset direction map
            "offset_pos_x": str(config.offset_direction_map.pos_x),
            "offset_neg_x": str(config.offset_direction_map.neg_x),
            "offset_pos_y": str(config.offset_direction_map.pos_y),
            "offset_neg_y": str(config.offset_direction_map.neg_y),
            # Safety limits
            "safety_x_min":  config.safety_limits.x_min,
            "safety_x_max":  config.safety_limits.x_max,
            "safety_y_min":  config.safety_limits.y_min,
            "safety_y_max":  config.safety_limits.y_max,
            "safety_z_min":  config.safety_limits.z_min,
            "safety_z_max":  config.safety_limits.z_max,
            "safety_rx_min": config.safety_limits.rx_min,
            "safety_rx_max": config.safety_limits.rx_max,
            "safety_ry_min": config.safety_limits.ry_min,
            "safety_ry_max": config.safety_limits.ry_max,
            "safety_rz_min": config.safety_limits.rz_min,
            "safety_rz_max": config.safety_limits.rz_max,
        }


class RobotCalibrationMapper:
    """Converts a RobotCalibrationSettings into the flat dict for the Calibration tab."""

    @staticmethod
    def to_flat_dict(settings: RobotCalibrationSettings) -> dict:
        return {
            # Adaptive movement
            "calib_min_step_mm":        settings.min_step_mm,
            "calib_max_step_mm":        settings.max_step_mm,
            "calib_target_error_mm":    settings.target_error_mm,
            "calib_max_error_ref":      settings.max_error_ref,
            "calib_k":                  settings.k,
            "calib_derivative_scaling": settings.derivative_scaling,
            # Marker detection
            "calib_z_target":     settings.z_target,
            "calib_required_ids": settings.required_ids,
        }
