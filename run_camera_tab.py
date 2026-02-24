"""
Runner: Camera Settings Plugin using unified service pattern.

Demonstrates the CameraSettingsPlugin with a mock service that combines
both settings persistence and camera actions.
"""
import sys
from pathlib import Path
from pprint import pformat

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow

from src.plugins.camera_settings import CameraSettingsPlugin
from src.plugins.camera_settings.camera_settings_data import CameraSettingsData


class MockCameraSettingsService:
    """
    Mock service implementing ICameraSettingsService.

    Combines both settings persistence and camera actions.
    """

    def __init__(self):
        self._settings = CameraSettingsData()
        self._raw_mode = False

    # Settings persistence
    def load_settings(self) -> CameraSettingsData:
        print(f"[service] Loading camera settings")
        return self._settings

    def save_settings(self, settings: CameraSettingsData) -> None:
        self._settings = settings
        print(f"[service] Settings saved:\n{pformat(settings, indent=2)}")

    # Camera actions
    def set_raw_mode(self, enabled: bool) -> None:
        self._raw_mode = enabled
        print(f"[service] Raw mode: {'ON' if enabled else 'OFF'}")

    def capture_image(self) -> None:
        print(f"[service] Capturing image...")

    def calibrate_camera(self) -> None:
        print(f"[service] Starting camera calibration...")

    def calibrate_robot(self) -> None:
        print(f"[service] Starting robot calibration...")


def main():
    app = QApplication(sys.argv)

    # Create unified service and plugin
    service = MockCameraSettingsService()
    plugin = CameraSettingsPlugin(service)
    plugin.load()

    win = QMainWindow()
    win.setWindowTitle("Camera Settings — unified service pattern")
    win.resize(1400, 900)
    win.setCentralWidget(plugin.widget)
    win.show()

    print("=== Camera Settings Plugin ===")
    print("Using unified ICameraSettingsService interface")
    print("Try:")
    print("  • Toggle Raw Mode")
    print("  • Click Capture Image")
    print("  • Click Calibrate buttons")
    print("  • Change settings and click Save")
    print()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
