from typing import Tuple
from PyQt6.QtWidgets import QWidget

from src.plugins.base_settings_plugin.base_settings_plugin import BaseSettingsPlugin
from src.plugins.robot_settings.controller import RobotSettingsController
from src.plugins.robot_settings.model import RobotSettingsModel
from src.plugins.robot_settings.IRobotSettingsService import RobotSettingsService
from src.plugins.robot_settings.view.robot_tab import robot_tab_factory
from src.settings.settings_view.settings_view import SettingsView
from src.plugins.robot_settings.view.movement_groups_tab import MovementGroupsTab


class RobotSettingsPlugin(BaseSettingsPlugin[
    RobotSettingsService,
    RobotSettingsModel,
    RobotSettingsController,
    Tuple[SettingsView, MovementGroupsTab]
]):
    """
    Self-contained MVC plugin for robot settings.

    Inherits from the BaseSettingsPlugin and implements the required factory methods.

    Usage:
        plugin = RobotSettingsPlugin(service)
        plugin.load()
        window.setCentralWidget(plugin.widget)
    """

    def _create_model(self, service: RobotSettingsService) -> RobotSettingsModel:
        """Create and return the model instance."""
        return RobotSettingsModel(service)

    def _create_view(self) -> Tuple[SettingsView, MovementGroupsTab]:
        """Create and return the view instance (returns tuple)."""
        return robot_tab_factory()

    def _create_controller(self, model: RobotSettingsModel, view: Tuple[SettingsView, MovementGroupsTab]) -> RobotSettingsController:
        """Create and return the controller instance."""
        # view is a tuple (SettingsView, MovementGroupsTab)
        settings_view, movement_tab = view
        return RobotSettingsController(model, settings_view, movement_tab)
