"""
Custom Settings Categories Example

Demonstrates how to use custom categories instead of the default ones.

Run with:
    python example_custom_categories.py
"""
import sys
from pathlib import Path

from src.settings.settings_menu.build_showcase import build_settings_menu_showcase

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow
from src.settings.settings_menu.settings_menu import SettingsNavigationWidget
from src.settings.settings_view.build_showcase import build_showcase







def main():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Custom Settings Categories Example - Tab Change Notifications")
    window.resize(1200, 800)



    # Create navigation widget with CUSTOM categories AND factory map
    # Views are automatically created!
    nav = build_settings_menu_showcase()

    # Connect to tab change signals
    def on_tab_changing(old_id: str, new_id: str):
        print(f"\n[Signal] tab_changing: {old_id} → {new_id}")

    def on_tab_changed(old_id: str, new_id: str):
        print(f"[Signal] tab_changed: {old_id} → {new_id}\n")

    nav.tab_changing.connect(on_tab_changing)
    nav.tab_changed.connect(on_tab_changed)

    window.setCentralWidget(nav)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

