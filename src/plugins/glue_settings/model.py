from typing import Optional

from src.plugins.glue_settings.glue_settings_data import GlueSettings
from src.plugins.glue_settings.IGlueSettingsService import GlueSettingsService
from src.plugins.glue_settings.mapper import GlueSettingsMapper


class GlueSettingsModel:
    def __init__(self, service: GlueSettingsService):
        self._service = service
        self._settings: Optional[GlueSettings] = None

    def load(self) -> GlueSettings:
        self._settings = self._service.load_settings()
        return self._settings

    def save(self, flat: dict) -> None:
        # Use current settings as base, or create default if not loaded yet
        base = self._settings if self._settings is not None else GlueSettings()
        updated = GlueSettingsMapper.from_flat_dict(flat, base)
        self._service.save_settings(updated)
        self._settings = updated
