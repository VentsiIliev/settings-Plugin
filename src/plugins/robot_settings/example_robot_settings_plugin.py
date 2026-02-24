import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow
from src.plugins.robot_settings import RobotSettingsPlugin, RobotSettingsService
from src.external_dependencies.robotConfig.robotConfigModel import get_default_config
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings

class FakeRobotSettingsService(RobotSettingsService):
    def load_config(self):
        print("Loading default config")

        return get_default_config()

    def save_config(self, config):
        print(f"Saving config: {config}")

    def load_calibration(self):
        print("Loading default calibration")

        return RobotCalibrationSettings()

    def save_calibration(self, calibration):
        print(f"Saving calibration: {calibration}")

app = QApplication(sys.argv)
plugin = RobotSettingsPlugin(service=FakeRobotSettingsService())
plugin.load()

window = QMainWindow()
window.setCentralWidget(plugin.widget)
window.resize(1280, 1024)
window.show()

sys.exit(app.exec())
