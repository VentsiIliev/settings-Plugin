from src.robot_settings.model import RobotSettingsModel
from src.robot_settings.mapper import RobotCalibrationMapper
from src.settings.settings_view import SettingsView
from src.robot_settings.view.movement_groups_tab import MovementGroupsTab


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

        self._view.save_requested.connect(self._on_save)

    def load(self) -> None:
        config, calibration = self._model.load()
        self._view.load(config)
        self._movement_tab.load(config.movement_groups)
        if calibration is not None:
            self._view.set_values(RobotCalibrationMapper.to_flat_dict(calibration))

    def _on_save(self, flat: dict) -> None:
        self._model.save(flat, self._movement_tab.get_values())
