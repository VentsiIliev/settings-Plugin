from PyQt6.QtWidgets import QWidget

from src.plugins.glue_settings.controller import GlueSettingsController
from src.plugins.glue_settings.model import GlueSettingsModel
from src.plugins.glue_settings.IGlueSettingsService import GlueSettingsService
from src.plugins.glue_settings.view.glue_tab import glue_tab_factory
from src.plugins.base_settings_plugin.base_settings_plugin import BaseSettingsPlugin
from src.settings.settings_view import SettingsView


class GlueSettingsPlugin(BaseSettingsPlugin[GlueSettingsService, GlueSettingsModel, GlueSettingsController, QWidget]):
    def _create_model(self, service: GlueSettingsService) -> GlueSettingsModel:
        return GlueSettingsModel(service)

    def _create_view(self) -> QWidget:
        # factory returns (view, extra_tabs)
        return glue_tab_factory()[0]

    def _create_controller(self, model: GlueSettingsModel, view: SettingsView) -> GlueSettingsController:
        return GlueSettingsController(model, view)