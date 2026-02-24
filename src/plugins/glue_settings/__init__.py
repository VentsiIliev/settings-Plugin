from PyQt6.QtWidgets import QWidget

from src.plugins.glue_settings.controller import GlueSettingsController
from src.plugins.glue_settings.model import GlueSettingsModel
from src.plugins.glue_settings.IGlueSettingsService import GlueSettingsService
from src.plugins.glue_settings.view.glue_tab import glue_tab_factory
from src.plugins.base_settings_plugin.base_settings_plugin import BaseSettingsPlugin
from src.settings.settings_view import SettingsView


class GlueSettingsPlugin(BaseSettingsPlugin[GlueSettingsService, GlueSettingsModel, GlueSettingsController, QWidget]):

    def __init__(self, service: GlueSettingsService):
        self._glue_type_tab = None
        super().__init__(service)

    def _create_model(self, service: GlueSettingsService) -> GlueSettingsModel:
        return GlueSettingsModel(service)

    def _create_view(self) -> QWidget:
        view_result = glue_tab_factory()
        if isinstance(view_result, tuple):
            view, glue_type_tab = view_result
            self._glue_type_tab = glue_type_tab
            self._connect_glue_type_signals()
            self._reload_glue_types()
            return view
        return view_result

    def _create_controller(self, model: GlueSettingsModel, view: SettingsView) -> GlueSettingsController:
        return GlueSettingsController(model, view)

    def _connect_glue_type_signals(self):
        self._glue_type_tab.add_requested.connect(self._on_add_glue_type)
        self._glue_type_tab.update_requested.connect(self._on_update_glue_type)
        self._glue_type_tab.remove_requested.connect(self._on_remove_glue_type)

    def _on_add_glue_type(self, name: str, description: str):
        try:
            self._service.add_glue_type(name, description)
            self._reload_glue_types()
        except Exception as e:
            print(f"[GlueSettingsPlugin] Error adding glue type: {e}")

    def _on_update_glue_type(self, id_: str, name: str, description: str):
        try:
            self._service.update_glue_type(id_, name, description)
            self._reload_glue_types()
        except Exception as e:
            print(f"[GlueSettingsPlugin] Error updating glue type: {e}")

    def _on_remove_glue_type(self, id_: str):
        try:
            self._service.remove_glue_type(id_)
            self._reload_glue_types()
        except Exception as e:
            print(f"[GlueSettingsPlugin] Error removing glue type: {e}")

    def _reload_glue_types(self):
        try:
            glue_types = self._service.load_glue_types()
            self._glue_type_tab.load_types(glue_types)
        except Exception as e:
            print(f"[GlueSettingsPlugin] Error reloading glue types: {e}")

    def load(self) -> None:
        super().load()
        if self._glue_type_tab:
            self._reload_glue_types()
