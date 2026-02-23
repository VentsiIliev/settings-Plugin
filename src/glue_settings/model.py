from typing import Optional

from src.glue_settings.glue_settings_data import GlueSettings
from src.glue_settings.repository import IGlueSettingsRepository
from src.glue_settings.mapper import GlueSettingsMapper


class GlueSettingsModel:
    def __init__(self, repo: IGlueSettingsRepository):
        self._repo = repo
        self._settings: Optional[GlueSettings] = None

    def load(self) -> GlueSettings:
        self._settings = self._repo.load()
        return self._settings

    def save(self, flat: dict) -> None:
        updated = GlueSettingsMapper.from_flat_dict(flat, self._settings)
        self._repo.save(updated)
        self._settings = updated
