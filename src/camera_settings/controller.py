from src.camera_settings.model import CameraSettingsModel
from src.camera_settings.mapper import CameraSettingsMapper
from src.settings.settings_view.settings_view import SettingsView


class CameraSettingsController:
    def __init__(self, model: CameraSettingsModel, view: SettingsView):
        self._model = model
        self._view  = view
        self._view.save_requested.connect(self._on_save)

    def load(self) -> None:
        settings = self._model.load()
        self._view.set_values(CameraSettingsMapper.to_flat_dict(settings))

    def _on_save(self, flat: dict) -> None:
        self._model.save(flat)
