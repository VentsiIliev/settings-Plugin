from typing import Optional

from src.camera_settings.camera_settings_data import CameraSettingsData
from src.camera_settings.mapper import CameraSettingsMapper
from src.camera_settings.repository import ICameraSettingsRepository


class CameraSettingsModel:
    def __init__(self, repo: ICameraSettingsRepository):
        self._repo = repo
        self._settings: Optional[CameraSettingsData] = None

    def load(self) -> CameraSettingsData:
        self._settings = self._repo.load()
        return self._settings

    def save(self, flat: dict) -> None:
        updated = CameraSettingsMapper.from_flat_dict(flat, self._settings)
        self._repo.save(updated)
        self._settings = updated
