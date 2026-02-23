"""
CameraSettingsView — horizontal split panel (optimised for 1280×1024).

Left  (1/3 width): ClickableLabel preview  +  CameraControlsWidget
Right (2/3 width): schema-driven SettingsView (tabs: Core, Detection,
                   Calibration, Brightness, ArUco)

The persistence controller works with the inner SettingsView.
A separate ICameraActionsService handles the action controls (DI).
The application can also plug in a real camera feed via set_preview_widget().
"""
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.settings.settings_view.settings_view import SettingsView
from src.utils_widgets.clickable_label import ClickableLabel
from src.camera_settings.view.camera_controls_widget import CameraControlsWidget


class CameraSettingsView(QWidget):
    """
    Left (1/3): ClickableLabel + CameraControlsWidget
    Right (2/3): SettingsView tabs

    Expose points::

        view.preview_label   — ClickableLabel (None after set_preview_widget)
        view.controls        — CameraControlsWidget with raw_mode / capture / calibrate signals
        view.settings_view   — inner SettingsView for the persistence controller
    """

    def __init__(self, settings_view: SettingsView, parent=None):
        super().__init__(parent)
        self._settings_view = settings_view
        self._build_ui()

    # ── Build ──────────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_left_panel(), stretch=1)
        root.addWidget(self._settings_view,      stretch=2)

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet("background: #12121F;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._preview_label = ClickableLabel()
        self._preview_label.add_area("pickup_area")
        self._preview_label.add_area("spray_area")
        self._preview_label.add_area("brightness_area")
        layout.addWidget(self._preview_label, stretch=1)

        self._controls = CameraControlsWidget()
        self._controls.active_area_changed.connect(self._on_active_area_changed)
        layout.addWidget(self._controls, stretch=0)

        self._left_layout = layout
        return panel

    # ── Internal slots ─────────────────────────────────────────────────────────

    def _on_active_area_changed(self, name: str) -> None:
        if self._preview_label:
            self._preview_label.set_active_area(name if name else None)

    # ── Public API ─────────────────────────────────────────────────────────────

    def set_preview_widget(self, widget: QWidget) -> None:
        """Replace the ClickableLabel with a real camera feed widget."""
        self._preview_label.setParent(None)
        self._preview_label = None
        self._left_layout.insertWidget(0, widget, stretch=1)

    @property
    def preview_label(self) -> ClickableLabel | None:
        """ClickableLabel for brightness area corner editing, or None if replaced."""
        return self._preview_label

    @property
    def controls(self) -> CameraControlsWidget:
        """Action controls strip (raw mode, capture, calibrate signals)."""
        return self._controls

    @property
    def settings_view(self) -> SettingsView:
        """Inner SettingsView — used by the persistence controller."""
        return self._settings_view
