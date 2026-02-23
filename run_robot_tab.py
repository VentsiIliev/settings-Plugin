"""
Runner: schema-driven RobotSettingsTab.

Schema in → consistent UI out.
Every widget change prints: [signal] key = value  (component)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow

from src.robot_settings.view.robot_tab import robot_tab_factory
from src.robot_settings.view.mapper import RobotCalibrationMapper
from src.external_dependencies.robotConfig.robotConfigModel import get_default_config
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings


def main():
    app = QApplication(sys.argv)

    config = get_default_config()
    calibration_settings = RobotCalibrationSettings()
    view, movement_tab = robot_tab_factory()

    view.load(config)
    view.set_values(RobotCalibrationMapper.to_flat_dict(calibration_settings))
    movement_tab.load(config.movement_groups)

    view.value_changed_signal.connect(
        lambda key, value, component: print(f"[signal]  {key} = {value!r}")
    )
    movement_tab.values_changed.connect(
        lambda key, value: print(f"[movement] {key} = {value!r}")
    )

    win = QMainWindow()
    win.setWindowTitle("RobotSettingsTab — schema-driven")
    win.resize(1280, 1024)
    win.setCentralWidget(view)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
