from src.plugins.robot_settings.model import RobotSettingsModel
from src.plugins.robot_settings.view.movement_groups_tab import MovementGroupsTab
from src.settings.settings_view.settings_view import SettingsView


class RobotSettingsController:
    def __init__(
        self,
        model: RobotSettingsModel,
        view: SettingsView,
        movement_tab: MovementGroupsTab,
    ):
        self._model        = model
        self._view         = view
        self._movement_tab = movement_tab

        self._view.value_changed_signal.connect(self._on_field_changed)
        self._view.save_requested.connect(self._on_save_requested)
        self._movement_tab.values_changed.connect(self._on_movement_changed)

    def load(self) -> None:
        config, calibration = self._model.load()
        self._view.load(config)
        self._movement_tab.load(config.movement_groups)

    def _on_field_changed(self, key: str, value, component: str) -> None:
        # Individual field changed
        print(f"[controller] Field changed: {key} = {value!r}")

    def _on_save_requested(self, values: dict) -> None:
        # Save button clicked - save all values
        flat = self._view.get_values()
        movement_groups = self._movement_tab.get_values()
        self._model.save(flat, movement_groups)
        print(f"[controller] Robot settings saved successfully")

    def _on_movement_changed(self, key: str, value) -> None:
        # Movement group changed
        print(f"[controller] Movement changed: {key} = {value!r}")
