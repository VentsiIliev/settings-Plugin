from src.plugins.glue_settings.model import GlueSettingsModel
from src.settings.settings_view.settings_view import SettingsView
from src.plugins.glue_settings.mapper import GlueSettingsMapper


class GlueSettingsController:
    def __init__(self, model: GlueSettingsModel, view: SettingsView):
        self._model = model
        self._view = view
        self._view.value_changed_signal.connect(self._on_value_changed)
        self._view.save_requested.connect(self._on_save_requested)

    def load(self) -> None:
        settings = self._model.load()
        flat = GlueSettingsMapper.to_flat_dict(settings)
        self._view.set_values(flat)

    def _on_value_changed(self, key: str, value, component: str) -> None:
        # Individual field changed - optionally auto-save or just mark as dirty
        pass

    def _on_save_requested(self, values: dict) -> None:
        # Save button clicked - save all values
        self._model.save(values)
        print(f"[controller] Settings saved successfully")
