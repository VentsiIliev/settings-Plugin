from typing import Protocol

from src.external_dependencies.robotConfig.robotConfigModel import RobotConfig
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings


class IRobotSettingsRepository(Protocol):
    def load(self) -> RobotConfig: ...
    def save(self, config: RobotConfig) -> None: ...


class IRobotCalibrationRepository(Protocol):
    def load(self) -> RobotCalibrationSettings: ...
    def save(self, settings: RobotCalibrationSettings) -> None: ...
