import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import QApplication, QMainWindow

from src.glue_settings import GlueSettingsPlugin
from src.glue_settings.glue_settings_data import GlueSettings
from src.glue_settings.glue_type import GlueType
from src.settings.settings_view.settings_view import SettingsView


# ── In-memory repository implementations ──────────────────────────────────────

class _InMemorySettingsRepo:
    def __init__(self):
        self._data = GlueSettings()

    def load(self) -> GlueSettings:
        return self._data

    def save(self, settings: GlueSettings) -> None:
        self._data = settings
        print(f"[save]   {settings}")


class _InMemoryGlueTypeRepo:
    def __init__(self):
        self._types: list[GlueType] = [
            GlueType("3081c54c-fe04-424c-b5ae-28837d896a91", "TEST TYPE",  "TEST DESC"),
            GlueType("ff699e24-d0b1-4155-8922-aeaebe5d849d", "TEST TYPE 2","TEST DESC 2"),
            GlueType("1aae8866-7e93-43a7-aa36-94210a1e3246", "TEST TYPE 3","TEST DESC 3"),
            GlueType("63d3a970-1f93-4e0d-8396-e33740a53f84", "NewType",    ""),
        ]

    def load(self) -> list[GlueType]:
        return list(self._types)

    def add(self, name: str, description: str) -> GlueType:
        gt = GlueType(id=str(uuid.uuid4()), name=name, description=description)
        self._types.append(gt)
        print(f"[add]    {name!r}  {description!r}")
        return gt

    def update(self, id_: str, name: str, description: str) -> GlueType:
        for gt in self._types:
            if gt.id == id_:
                gt.name = name
                gt.description = description
                print(f"[update] {id_} → {name!r}  {description!r}")
                return gt
        raise KeyError(id_)

    def remove(self, id_: str) -> None:
        self._types[:] = [gt for gt in self._types if gt.id != id_]
        print(f"[remove] {id_}")


# ── Runner ─────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)

    plugin = GlueSettingsPlugin(
        repo=_InMemorySettingsRepo(),
        glue_type_repo=_InMemoryGlueTypeRepo(),
    )
    plugin.load()

    view: SettingsView = plugin.widget  # type: ignore[assignment]
    view.value_changed_signal.connect(
        lambda key, value, component: print(f"[signal] {key} = {value!r}")
    )

    win = QMainWindow()
    win.setWindowTitle("Glue Settings — schema-driven")
    win.resize(1280, 1024)
    win.setCentralWidget(view)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
