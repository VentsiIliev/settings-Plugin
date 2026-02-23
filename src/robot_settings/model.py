from typing import Dict, Optional

from src.external_dependencies.robotConfig.MovementGroup import MovementGroup
from src.external_dependencies.robotConfig.robotConfigModel import RobotConfig
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings
from src.robot_settings.repository import IRobotCalibrationRepository, IRobotSettingsRepository
from src.robot_settings.mapper import RobotCalibrationMapper, RobotSettingsMapper


class RobotSettingsModel:
    def __init__(
        self,
        config_repo: IRobotSettingsRepository,
        calibration_repo: IRobotCalibrationRepository,
    ):
        self._config_repo      = config_repo
        self._calibration_repo = calibration_repo
        self._config:      Optional[RobotConfig]              = None
        self._calibration: Optional[RobotCalibrationSettings] = None

    def load(self) -> tuple[RobotConfig, RobotCalibrationSettings]:
        self._config      = self._config_repo.load()
        self._calibration = self._calibration_repo.load()
        return self._config, self._calibration

    def save(self, flat: dict, movement_groups: Dict[str, MovementGroup]) -> None:
        updated = RobotSettingsMapper.from_flat_dict(flat, self._config)
        updated.movement_groups = movement_groups
        self._config_repo.save(updated)
        self._config = updated

        updated_calib = RobotCalibrationMapper.from_flat_dict(flat, self._calibration)
        self._calibration_repo.save(updated_calib)
        self._calibration = updated_calib
