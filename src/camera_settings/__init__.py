from PyQt6.QtWidgets import QWidget

from src.camera_settings.controller import CameraSettingsController
from src.camera_settings.model import CameraSettingsModel
from src.camera_settings.repository import ICameraSettingsRepository
from src.camera_settings.view.camera_tab import camera_tab_factory


class CameraSettingsPlugin:
    def __init__(self, repo: ICameraSettingsRepository):
        model = CameraSettingsModel(repo)
        view  = camera_tab_factory()
        self._controller = CameraSettingsController(model, view)
        self._widget = view

    @property
    def widget(self) -> QWidget:
        return self._widget

    def load(self) -> None:
        self._controller.load()
