import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import QApplication, QMainWindow

from src.plugins.glue_settings import GlueSettingsPlugin, GlueSettingsService
from src.plugins.glue_settings.glue_settings_data import GlueSettings
from src.plugins.glue_settings.glue_type import GlueType
from src.settings.settings_view.settings_view import SettingsView


class FakeGlueSettingsService(GlueSettingsService):
    """Mock service for demonstration purposes."""

    def __init__(self):
        self._settings = GlueSettings()
        self._types: list[GlueType] = [
            GlueType("3081c54c-fe04-424c-b5ae-28837d896a91", "TEST TYPE",  "TEST DESC"),
            GlueType("ff699e24-d0b1-4155-8922-aeaebe5d849d", "TEST TYPE 2","TEST DESC 2"),
            GlueType("1aae8866-7e93-43a7-aa36-94210a1e3246", "TEST TYPE 3","TEST DESC 3"),
            GlueType("63d3a970-1f93-4e0d-8396-e33740a53f84", "NewType",    ""),
        ]

    def load_settings(self) -> GlueSettings:
        return self._settings

    def save_settings(self, settings: GlueSettings) -> None:
        self._settings = settings
        print(f"[service] Settings saved: {settings} ")

    def load_glue_types(self) -> list[GlueType]:
        return list(self._types)

    def add_glue_type(self, name: str, description: str) -> GlueType:
        gt = GlueType(id=str(uuid.uuid4()), name=name, description=description)
        self._types.append(gt)
        print(f"[service] Glue type added: {name!r}")
        return gt

    def update_glue_type(self, id_: str, name: str, description: str) -> GlueType:
        for gt in self._types:
            if gt.id == id_:
                gt.name = name
                gt.description = description
                print(f"[service] Glue type updated: {id_} → {name!r}")
                return gt
        raise KeyError(id_)

    def remove_glue_type(self, id_: str) -> None:
        self._types[:] = [gt for gt in self._types if gt.id != id_]
        print(f"[service] Glue type removed: {id_}")


def main():
    app = QApplication(sys.argv)

    service = FakeGlueSettingsService()
    plugin = GlueSettingsPlugin(service)
    # plugin.load()

    view: SettingsView = plugin.widget
    view.value_changed_signal.connect(
        lambda key, value, component: print(f"[signal] {key} = {value!r}")
    )

    win = QMainWindow()
    win.setWindowTitle("Glue Settings — schema-driven with service")
    win.resize(1280, 1024)
    win.setCentralWidget(view)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
