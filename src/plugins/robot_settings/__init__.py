from PyQt6.QtWidgets import QWidget

from src.plugins.robot_settings.controller import RobotSettingsController
from src.plugins.robot_settings.model import RobotSettingsModel
from src.plugins.robot_settings.IRobotSettingsService import RobotSettingsService
from src.plugins.robot_settings.view.robot_tab import robot_tab_factory


class RobotSettingsPlugin:
    """
    Self-contained MVC plugin for robot settings.

    Implements ISettingsPlugin interface.

    Usage:
        plugin = RobotSettingsPlugin(service)
        plugin.load()
        window.setCentralWidget(plugin.widget)
    """

    def __init__(self, service: RobotSettingsService):
        self._service = service
        self._model = RobotSettingsModel(service)
        view, movement_tab = robot_tab_factory()
        self._controller = RobotSettingsController(self._model, view, movement_tab)
        self._widget = view

    @property
    def widget(self) -> QWidget:
        """Returns the main widget for this settings plugin."""
        return self._widget

    def load(self) -> None:
        """Load settings from the service and populate the UI."""
        self._controller.load()

    def save(self) -> None:
        """Explicitly save current settings."""
        if hasattr(self._controller, 'save'):
            self._controller.save()
        else:
            print("[RobotSettingsPlugin] Auto-save enabled - changes saved on Save button click")
