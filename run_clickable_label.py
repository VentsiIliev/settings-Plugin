import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

from src.utils_widgets.clickable_label import ClickableLabel


def create_test_frame(width: int = 1280, height: int = 720) -> QPixmap:
    """Create a test camera frame with grid pattern."""
    pixmap = QPixmap(width, height)
    pixmap.fill(QColor("black"))

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Draw grid
    pen = painter.pen()
    pen.setColor(QColor(220, 220, 220))
    pen.setWidth(1)
    painter.setPen(pen)

    grid_size = 100
    for x in range(0, width, grid_size):
        painter.drawLine(x, 0, x, height)
    for y in range(0, height, grid_size):
        painter.drawLine(0, y, width, y)

    # Draw center crosshair
    pen.setColor(QColor(150, 150, 150))
    pen.setWidth(2)
    painter.setPen(pen)
    cx, cy = width // 2, height // 2
    painter.drawLine(cx - 50, cy, cx + 50, cy)
    painter.drawLine(cx, cy - 50, cx, cy + 50)

    # Draw text
    painter.setPen(QColor(80, 80, 80))
    painter.drawText(20, 40, f"Test Frame: {width}×{height}")

    painter.end()
    return pixmap


def main():
    app = QApplication(sys.argv)

    # Create main window
    win = QMainWindow()
    win.setWindowTitle("ClickableLabel Demo — Camera Preview with Areas")
    win.resize(1400, 900)
    win.setStyleSheet("background-color: white;")

    # Central widget with layout
    central = QWidget()
    central.setStyleSheet("background-color: white;")
    main_layout = QVBoxLayout(central)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)

    # Create the clickable label
    label = ClickableLabel()

    # Add two areas with initial corners (normalized [0, 1] coordinates)
    label.add_area("pickup_area", QColor(80, 220, 100))    # green
    label.add_area("spray_area", QColor(255, 140, 50))     # orange

    # Set initial corners for pickup area (rectangle in top-left)
    label.set_area_corners("pickup_area", [
        (0.1, 0.1),   # top-left
        (0.4, 0.1),   # top-right
        (0.4, 0.4),   # bottom-right
        (0.1, 0.4),   # bottom-left
    ])

    # Set initial corners for spray area (rectangle in bottom-right)
    label.set_area_corners("spray_area", [
        (0.6, 0.6),   # top-left
        (0.9, 0.6),   # top-right
        (0.9, 0.9),   # bottom-right
        (0.6, 0.9),   # bottom-left
    ])

    # Set active area for editing
    label.set_active_area("pickup_area")

    # Load test frame
    frame = create_test_frame(1280, 720)
    label.set_frame(frame)

    # Connect signals
    def on_corner_updated(area_name: str, idx: int, xn: float, yn: float):
        px = int(xn * 1280)
        py = int(yn * 720)
        print(f"[corner_updated] {area_name}, corner #{idx+1}: ({xn:.3f}, {yn:.3f}) = pixel ({px}, {py})")

    def on_empty_clicked(area_name: str, xn: float, yn: float):
        px = int(xn * 1280)
        py = int(yn * 720)
        print(f"[empty_clicked] {area_name}: ({xn:.3f}, {yn:.3f}) = pixel ({px}, {py})")

    label.corner_updated.connect(on_corner_updated)
    label.empty_clicked.connect(on_empty_clicked)

    main_layout.addWidget(label, stretch=1)

    # Control buttons
    button_layout = QHBoxLayout()
    button_layout.setSpacing(10)

    def set_pickup_active():
        label.set_active_area("pickup_area")
        print("[action] Set pickup_area as active")

    def set_spray_active():
        label.set_active_area("spray_area")
        print("[action] Set spray_area as active")

    def set_view_only():
        label.set_active_area(None)
        print("[action] Set to view-only mode (no editing)")

    def clear_pickup():
        label.clear_area("pickup_area")
        print("[action] Cleared pickup_area corners")

    def clear_spray():
        label.clear_area("spray_area")
        print("[action] Cleared spray_area corners")

    def print_corners():
        pickup = label.get_area_corners("pickup_area")
        spray = label.get_area_corners("spray_area")
        print(f"\n[corners] pickup_area: {pickup}")
        print(f"[corners] spray_area: {spray}\n")

    btn_pickup = QPushButton("Edit Pickup Area")
    btn_spray = QPushButton("Edit Spray Area")
    btn_view = QPushButton("View Only")
    btn_clear_pickup = QPushButton("Clear Pickup")
    btn_clear_spray = QPushButton("Clear Spray")
    btn_print = QPushButton("Print Corners")

    btn_pickup.clicked.connect(set_pickup_active)
    btn_spray.clicked.connect(set_spray_active)
    btn_view.clicked.connect(set_view_only)
    btn_clear_pickup.clicked.connect(clear_pickup)
    btn_clear_spray.clicked.connect(clear_spray)
    btn_print.clicked.connect(print_corners)

    button_layout.addWidget(btn_pickup)
    button_layout.addWidget(btn_spray)
    button_layout.addWidget(btn_view)
    button_layout.addStretch()
    button_layout.addWidget(btn_clear_pickup)
    button_layout.addWidget(btn_clear_spray)
    button_layout.addWidget(btn_print)

    main_layout.addLayout(button_layout)

    # Instructions
    print("=== ClickableLabel Demo ===")
    print("Instructions:")
    print("  • Click 'Edit Pickup Area' or 'Edit Spray Area' to select which area to edit")
    print("  • Click on the image to add corners (up to 4 per area)")
    print("  • Drag existing corners to move them")
    print("  • Click 'View Only' to disable editing")
    print("  • Click coordinates are shown in the top-left corner of the image")
    print("  • All signals are printed to the console")
    print()

    win.setCentralWidget(central)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

