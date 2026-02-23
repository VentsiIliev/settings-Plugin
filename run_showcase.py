"""
Settings UI Showcase - All Widget Types Demo

Demonstrates all available widget types in the schema-driven settings system.
This is built using the build_showcase() function from src/settings/build_showcase.py

Run with:
    python run_showcase.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow
from src.settings.settings_view.build_showcase import build_showcase


def main():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Settings UI Showcase - All Widget Types")
    window.resize(1200, 800)

    # Build the showcase widget
    showcase = build_showcase()

    window.setCentralWidget(showcase)
    window.show()

    print("="*70)
    print("SETTINGS UI SHOWCASE")
    print("="*70)
    print("\nDemonstrates ALL available widget types:")
    print("\n📊 Spinbox Group:")
    print("  • Basic integer spinbox")
    print("  • Spinbox with range limits")
    print("  • Spinbox with suffix (units)")
    print("\n📏 Double Spinbox Group:")
    print("  • Basic float spinbox")
    print("  • Double with custom decimals")
    print("  • Double with min/max/suffix")
    print("\n✏️  Text Input Group:")
    print("  • Line edit for text input")
    print("  • IP address field")
    print("  • URL field")
    print("\n🎛️  Combo Box Group:")
    print("  • Dropdown selection")
    print("  • Theme selector")
    print("  • Mode selector")
    print("\n📋 Integer List Group:")
    print("  • List of integers")
    print("  • Configuration arrays")
    print("\nEach tab demonstrates a different widget category.")
    print("All widgets are auto-generated from schemas!")
    print("\nTry:")
    print("  • Switch between tabs to see different widget types")
    print("  • Adjust values and see live changes in console")
    print("  • Observe how schema definitions create complete UI")
    print("="*70 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
