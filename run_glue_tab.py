import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow

from src.plugins.glue_settings import GlueSettingsPlugin
from src.plugins.glue_settings.glue_settings_data import GlueSettings


class MockGlueSettingsService:
    """Simple mock service without glue types for basic demonstration."""

    def __init__(self):
        self._settings = GlueSettings()

    def load_settings(self) -> GlueSettings:
        return self._settings

    def save_settings(self, settings: GlueSettings) -> None:
        self._settings = settings
        print(f"[service] Settings saved: spray_on={settings.spray_on}")

    def load_glue_types(self):
        return []

    def add_glue_type(self, name: str, description: str):
        raise NotImplementedError("Mock service does not support glue types")

    def update_glue_type(self, id_: str, name: str, description: str):
        raise NotImplementedError("Mock service does not support glue types")

    def remove_glue_type(self, id_: str):
        raise NotImplementedError("Mock service does not support glue types")


def main():
    app = QApplication(sys.argv)

    service = MockGlueSettingsService()
    plugin = GlueSettingsPlugin(service)


    win = QMainWindow()
    win.setWindowTitle("Glue Settings — schema-driven with service")
    win.resize(1280, 1024)
    win.setCentralWidget(plugin.widget)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

