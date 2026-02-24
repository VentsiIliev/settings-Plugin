"""
Example: Creating a new settings plugin using the common interface.

This demonstrates how to create a camera settings plugin following
the established architecture pattern.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dataclasses import dataclass
from typing import Protocol
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

# Step 1: Define your data model
@dataclass
class CameraSettings:
    brightness: int = 50
    contrast: int = 50
    exposure: int = 100
    fps: int = 30
    resolution: str = "1920x1080"


# Step 2: Define your service protocol
class CameraSettingsService(Protocol):
    """Service interface for camera settings."""
    def load_settings(self) -> CameraSettings: ...
    def save_settings(self, settings: CameraSettings) -> None: ...


# Step 3: Create mapper
class CameraSettingsMapper:
    @staticmethod
    def to_flat_dict(settings: CameraSettings) -> dict:
        return {
            "brightness": settings.brightness,
            "contrast": settings.contrast,
            "exposure": settings.exposure,
            "fps": settings.fps,
            "resolution": settings.resolution,
        }

    @staticmethod
    def from_flat_dict(flat: dict, base: CameraSettings) -> CameraSettings:
        from copy import deepcopy
        s = deepcopy(base)
        s.brightness = int(flat.get("brightness", s.brightness))
        s.contrast = int(flat.get("contrast", s.contrast))
        s.exposure = int(flat.get("exposure", s.exposure))
        s.fps = int(flat.get("fps", s.fps))
        s.resolution = flat.get("resolution", s.resolution)
        return s


# Step 4: Create model
class CameraSettingsModel:
    def __init__(self, service: CameraSettingsService):
        self._service = service
        self._settings = None

    def load(self) -> CameraSettings:
        self._settings = self._service.load_settings()
        return self._settings

    def save(self, flat: dict) -> None:
        updated = CameraSettingsMapper.from_flat_dict(flat, self._settings)
        self._service.save_settings(updated)
        self._settings = updated


# Step 5: Create controller
from src.settings.settings_view.settings_view import SettingsView

class CameraSettingsController:
    def __init__(self, model: CameraSettingsModel, view: SettingsView):
        self._model = model
        self._view = view
        self._view.value_changed_signal.connect(self._on_value_changed)
        self._view.save_requested.connect(self._on_save_requested)

    def load(self) -> None:
        settings = self._model.load()
        flat = CameraSettingsMapper.to_flat_dict(settings)
        self._view.set_values(flat)

    def _on_value_changed(self, key: str, value, component: str) -> None:
        print(f"[controller] Field changed: {key} = {value!r}")

    def _on_save_requested(self, values: dict) -> None:
        self._model.save(values)
        print(f"[controller] Camera settings saved successfully")


# Step 6: Create view factory
from src.settings.settings_view.schema import SettingField, SettingGroup

def camera_tab_factory() -> SettingsView:
    CAMERA_GROUP = SettingGroup("Camera Settings", [
        SettingField("brightness", "Brightness", "spinbox", default=50, min_val=0, max_val=100, suffix=" %", step=1, step_options=[1, 5, 10]),
        SettingField("contrast", "Contrast", "spinbox", default=50, min_val=0, max_val=100, suffix=" %", step=1, step_options=[1, 5, 10]),
        SettingField("exposure", "Exposure", "spinbox", default=100, min_val=1, max_val=1000, suffix=" ms", step=1, step_options=[1, 10, 50]),
        SettingField("fps", "Frame Rate", "spinbox", default=30, min_val=1, max_val=120, suffix=" fps", step=1, step_options=[1, 5, 10]),
        SettingField("resolution", "Resolution", "combo", default="1920x1080", choices=["640x480", "1280x720", "1920x1080", "3840x2160"]),
    ])

    view = SettingsView(
        component_name="CameraSettings",
        mapper=CameraSettingsMapper.to_flat_dict,
    )
    view.add_tab("General", [CAMERA_GROUP])
    return view


# Step 7: Create the plugin (OPTION A - Manual Implementation)
class CameraSettingsPlugin:
    """
    Camera settings plugin.

    Implements ISettingsPlugin interface.
    """

    def __init__(self, service: CameraSettingsService):
        self._service = service
        self._model = CameraSettingsModel(service)
        self._view = camera_tab_factory()
        self._controller = CameraSettingsController(self._model, self._view)
        self._widget = self._view

    @property
    def widget(self) -> QWidget:
        return self._widget

    def load(self) -> None:
        self._controller.load()

    def save(self) -> None:
        if hasattr(self._controller, 'save'):
            self._controller.save()
        else:
            print("[CameraSettingsPlugin] Auto-save enabled")


# Mock service for testing
class MockCameraService:
    def __init__(self):
        self._settings = CameraSettings()

    def load_settings(self) -> CameraSettings:
        return self._settings

    def save_settings(self, settings: CameraSettings) -> None:
        self._settings = settings
        print(f"[service] Camera settings saved: brightness={settings.brightness}, fps={settings.fps}")


# Demo application
def main():
    app = QApplication(sys.argv)

    # Create service and plugin
    service = MockCameraService()
    plugin = CameraSettingsPlugin(service)
    plugin.load()

    # Show in window
    win = QMainWindow()
    win.setWindowTitle("Camera Settings Plugin — Common Interface Example")
    win.resize(1280, 800)
    win.setCentralWidget(plugin.widget)
    win.show()

    print("=== Camera Settings Plugin Example ===")
    print("This demonstrates how to create a new settings plugin")
    print("following the common ISettingsPlugin interface.")
    print()
    print("Try changing values and clicking Save!")
    print()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

