from PyQt6.QtWidgets import QWidget

from src.robot_settings.controller import RobotSettingsController
from src.robot_settings.model import RobotSettingsModel
from src.robot_settings.repository import IRobotCalibrationRepository, IRobotSettingsRepository
from src.robot_settings.view.robot_tab import robot_tab_factory


class RobotSettingsPlugin:
    """
    Self-contained MVC plugin for robot settings.

    Usage:
        plugin = RobotSettingsPlugin(config_repo, calibration_repo)
        plugin.load()
        window.setCentralWidget(plugin.widget)
    """

    def __init__(
        self,
        config_repo: IRobotSettingsRepository,
        calibration_repo: IRobotCalibrationRepository,
    ):
        model = RobotSettingsModel(config_repo, calibration_repo)
        view, movement_tab = robot_tab_factory()
        self._controller = RobotSettingsController(model, view, movement_tab)
        self._widget = view

    @property
    def widget(self) -> QWidget:
        return self._widget

    def load(self) -> None:
        self._controller.load()
