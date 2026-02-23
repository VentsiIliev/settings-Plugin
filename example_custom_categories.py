"""
Custom Settings Categories Example

Demonstrates how to use custom categories instead of the default ones.

Run with:
    python example_custom_categories.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.settings.settings_menu.settings_menu import SettingsNavigationWidget
from src.settings.build_showcase import build_showcase




CUSTOM_CATEGORIES = [
    {
        "id": "users",
        "title": "User Management",
        "icon": "mdi.account-group",
        "description": "Manage users and permissions"
    },
    {
        "id": "database",
        "title": "Database",
        "icon": "mdi.database",
        "description": "Database configuration"
    },
    {
        "id": "api",
        "title": "API Settings",
        "icon": "mdi.api",
        "description": "API endpoints and keys"
    },
    {
        "id": "backup",
        "title": "Backup",
        "icon": "mdi.backup-restore",
        "description": "Backup and restore settings"
    },
    {
        "id": "logging",
        "title": "Logging",
        "icon": "mdi.text-box",
        "description": "Log settings and monitoring"
    }
]





def main():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Custom Settings Categories Example - Tab Change Notifications")
    window.resize(1200, 800)

    # Define factory map - functions that create widgets for each category
    factory_map = {
        "users": build_showcase,
        "database": build_showcase,
        "api": build_showcase,
        "backup": build_showcase,
        "logging": build_showcase,
    }

    # Create navigation widget with CUSTOM categories AND factory map
    # Views are automatically created!
    nav = SettingsNavigationWidget(
        categories=CUSTOM_CATEGORIES,
        factory_map=factory_map
    )

    # Connect to tab change signals
    def on_tab_changing(old_id: str, new_id: str):
        print(f"\n[Signal] tab_changing: {old_id} → {new_id}")

    def on_tab_changed(old_id: str, new_id: str):
        print(f"[Signal] tab_changed: {old_id} → {new_id}\n")

    nav.tab_changing.connect(on_tab_changing)
    nav.tab_changed.connect(on_tab_changed)

    window.setCentralWidget(nav)
    window.show()

    print("="*70)
    print("CUSTOM SETTINGS CATEGORIES - TAB CHANGE NOTIFICATIONS")
    print("="*70)
    print("\n✨ This example demonstrates tab change notifications!")
    print("\nFeatures:")
    print("  ✓ Widgets receive on_tab_activate() when shown")
    print("  ✓ Widgets receive on_tab_deactivate() when hidden")
    print("  ✓ Signals: tab_changing (before) and tab_changed (after)")
    print("  ✓ Console output shows notification flow")
    print("\nCustom categories defined:")
    for cat in CUSTOM_CATEGORIES:
        print(f"  • {cat['title']} ({cat['id']})")
    print("\n✨ Try this:")
    print("  1. Click on different category icons in the sidebar")
    print("  2. Watch the console for tab change notifications")
    print("  3. Observe the 'Status' indicator change in each tab")
    print("\nNotification flow:")
    print("  1. Signal: tab_changing (old_id, new_id)")
    print("  2. Call: old_widget.on_tab_deactivate()")
    print("  3. Switch tab (QStackedWidget)")
    print("  4. Call: new_widget.on_tab_activate()")
    print("  5. Signal: tab_changed (old_id, new_id)")
    print("\nAdvantages:")
    print("  ✓ Widgets can save state before being hidden")
    print("  ✓ Widgets can refresh data when becoming visible")
    print("  ✓ Clean lifecycle management")
    print("  ✓ Optional - widgets don't need to implement these methods")
    print("\n" + "="*70 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

