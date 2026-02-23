from typing import Protocol

from src.camera_settings.camera_settings_data import CameraSettingsData


class ICameraSettingsRepository(Protocol):
    def load(self) -> CameraSettingsData: ...
    def save(self, settings: CameraSettingsData) -> None: ...
