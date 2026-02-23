from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QWidget

from src.camera_settings.camera_actions_service import ICameraActionsService
from src.utils_widgets.clickable_label import ClickableLabel
from src.camera_settings.controller import CameraSettingsController
from src.camera_settings.model import CameraSettingsModel
from src.camera_settings.repository import ICameraSettingsRepository
from src.camera_settings.view.camera_tab import camera_tab_factory
from src.camera_settings.view.camera_settings_view import CameraSettingsView


class CameraSettingsPlugin:
    """
    Wires the camera settings MVC stack.

    Parameters
    ----------
    repo:
        Persistence repository — loaded/saved by CameraSettingsController.
    actions_service:
        Optional camera actions handler (raw mode, capture, calibrate).
        If provided, the plugin connects view control signals to it automatically.
        Pass *None* (default) to leave signals unconnected (useful in tests /
        standalone runner).
    """

    def __init__(
        self,
        repo: ICameraSettingsRepository,
        actions_service: Optional[ICameraActionsService] = None,
    ):
        model = CameraSettingsModel(repo)
        view, settings_view = camera_tab_factory()
        self._controller = CameraSettingsController(model, settings_view)
        self._view: CameraSettingsView = view

        if actions_service is not None:
            self._connect_actions(actions_service)

    # ── Private ────────────────────────────────────────────────────────────────

    def _connect_actions(self, svc: ICameraActionsService) -> None:
        ctrl = self._view.controls
        ctrl.raw_mode_toggled.connect(svc.set_raw_mode)
        ctrl.capture_requested.connect(svc.capture_image)
        ctrl.calibrate_camera_requested.connect(svc.calibrate_camera)
        ctrl.calibrate_robot_requested.connect(svc.calibrate_robot)

    # ── Public API ─────────────────────────────────────────────────────────────

    @property
    def widget(self) -> QWidget:
        return self._view

    @property
    def preview_label(self) -> ClickableLabel | None:
        """The built-in ClickableLabel, or None after set_preview_widget()."""
        return self._view.preview_label

    def set_preview_widget(self, widget: QWidget) -> None:
        """Plug in a live camera feed widget (replaces the ClickableLabel)."""
        self._view.set_preview_widget(widget)

    def load(self) -> None:
        self._controller.load()
