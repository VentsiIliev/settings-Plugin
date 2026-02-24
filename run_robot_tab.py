"""
Runner: schema-driven RobotSettingsTab using service pattern.

Schema in → consistent UI out.
Every widget change prints: [signal] key = value  (component)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow

from src.plugins.robot_settings import RobotSettingsPlugin
from src.external_dependencies.robotConfig.robotConfigModel import get_default_config
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings


class MockRobotSettingsService:
    """Mock service for demonstration purposes."""

    def __init__(self):
        self._config = get_default_config()
        self._calibration = RobotCalibrationSettings()

    def load_config(self):
        return self._config

    def save_config(self, config):
        self._config = config
        print(f"[service] Config saved: {config.robot_ip}")

    def load_calibration(self):
        return self._calibration

    def save_calibration(self, calibration):
        self._calibration = calibration
        print(f"[service] Calibration saved")


def main():
    app = QApplication(sys.argv)

    service = MockRobotSettingsService()
    plugin = RobotSettingsPlugin(service)
    plugin.load()

    win = QMainWindow()
    win.setWindowTitle("RobotSettingsTab — schema-driven with service")
    win.resize(1280, 1024)
    win.setCentralWidget(plugin.widget)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
