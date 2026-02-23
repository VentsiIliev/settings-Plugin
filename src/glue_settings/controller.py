from src.glue_settings.model import GlueSettingsModel
from src.glue_settings.repository import IGlueTypeRepository
from src.glue_settings.view.glue_type_tab import GlueTypeTab
from src.settings.settings_view.settings_view import SettingsView
from src.glue_settings.mapper import GlueSettingsMapper


class GlueSettingsController:
    def __init__(
        self,
        model: GlueSettingsModel,
        view: SettingsView,
        glue_type_tab: GlueTypeTab,
        glue_type_repo: IGlueTypeRepository,
    ):
        self._model          = model
        self._view           = view
        self._glue_type_tab  = glue_type_tab
        self._glue_type_repo = glue_type_repo

        self._view.save_requested.connect(self._on_save)
        self._glue_type_tab.add_requested.connect(self._on_type_add)
        self._glue_type_tab.update_requested.connect(self._on_type_update)
        self._glue_type_tab.remove_requested.connect(self._on_type_remove)

    def load(self) -> None:
        settings = self._model.load()
        self._view.set_values(GlueSettingsMapper.to_flat_dict(settings))
        self._glue_type_tab.load_types(self._glue_type_repo.load())

    # ── Glue settings ──────────────────────────────────────────────────────────

    def _on_save(self, flat: dict) -> None:
        self._model.save(flat)

    # ── Glue type CRUD ─────────────────────────────────────────────────────────

    def _on_type_add(self, name: str, description: str) -> None:
        self._glue_type_repo.add(name, description)
        self._glue_type_tab.load_types(self._glue_type_repo.load())

    def _on_type_update(self, id: str, name: str, description: str) -> None:
        self._glue_type_repo.update(id, name, description)
        self._glue_type_tab.load_types(self._glue_type_repo.load())

    def _on_type_remove(self, id: str) -> None:
        self._glue_type_repo.remove(id)
        self._glue_type_tab.load_types(self._glue_type_repo.load())
