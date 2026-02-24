from typing import Dict, Optional

from src.external_dependencies.robotConfig.MovementGroup import MovementGroup
from src.external_dependencies.robotConfig.robotConfigModel import RobotConfig, get_default_config
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings
from src.plugins.robot_settings.IRobotSettingsService import RobotSettingsService
from src.plugins.robot_settings.mapper import RobotCalibrationMapper, RobotSettingsMapper


class RobotSettingsModel:
    def __init__(self, service: RobotSettingsService):
        self._service = service
        self._config: Optional[RobotConfig] = None
        self._calibration: Optional[RobotCalibrationSettings] = None

    def load(self) -> tuple[RobotConfig, RobotCalibrationSettings]:
        self._config = self._service.load_config()
        self._calibration = self._service.load_calibration()
        return self._config, self._calibration

    def save(self, flat: dict, movement_groups: Dict[str, MovementGroup]) -> None:
        updated = RobotSettingsMapper.from_flat_dict(flat, self._config)
        updated.movement_groups = movement_groups
        self._service.save_config(updated)
        self._config = updated

        updated_calib = RobotCalibrationMapper.from_flat_dict(flat, self._calibration)
        self._service.save_calibration(updated_calib)
        self._calibration = updated_calib
