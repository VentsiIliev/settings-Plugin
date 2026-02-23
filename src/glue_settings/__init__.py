from PyQt6.QtWidgets import QWidget

from src.glue_settings.controller import GlueSettingsController
from src.glue_settings.model import GlueSettingsModel
from src.glue_settings.repository import IGlueSettingsRepository, IGlueTypeRepository
from src.glue_settings.view.glue_tab import glue_tab_factory


class GlueSettingsPlugin:
    def __init__(
        self,
        repo: IGlueSettingsRepository,
        glue_type_repo: IGlueTypeRepository,
    ):
        model = GlueSettingsModel(repo)
        view, glue_type_tab = glue_tab_factory()
        self._controller = GlueSettingsController(model, view, glue_type_tab, glue_type_repo)
        self._widget = view

    @property
    def widget(self) -> QWidget:
        return self._widget

    def load(self) -> None:
        self._controller.load()
