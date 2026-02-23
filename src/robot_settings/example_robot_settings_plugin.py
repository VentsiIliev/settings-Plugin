import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow
from src.robot_settings import RobotSettingsPlugin
from src.external_dependencies.robotConfig.robotConfigModel import get_default_config
from src.external_dependencies.robotConfig.robot_calibration_settings import RobotCalibrationSettings

class MockConfigRepo:
    def load(self):
        print(f"[MockConfigRepo] Loading config...")
        return get_default_config()
    def save(self, config):

        print(f"[MockConfigRepo] Saving config: {config}")

class MockCalibrationRepo:
    def load(self):
        print(f"[MockCalibrationRepo] Loading calibration...")
        return RobotCalibrationSettings()
    def save(self, settings):
        print(f"[MockCalibrationRepo] Saving calibration: {settings}")

app = QApplication(sys.argv)
plugin = RobotSettingsPlugin(MockConfigRepo(), MockCalibrationRepo())
plugin.load()

window = QMainWindow()
window.setCentralWidget(plugin.widget)
window.resize(1280, 1024)
window.show()

sys.exit(app.exec())
