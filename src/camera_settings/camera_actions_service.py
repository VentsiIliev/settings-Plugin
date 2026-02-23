"""
ICameraActionsService — protocol (interface) for camera action handling.

Inject a concrete implementation into CameraSettingsPlugin via the
``actions_service`` parameter.  The plugin connects view signals to the
service methods automatically.
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class ICameraActionsService(Protocol):
    def set_raw_mode(self, enabled: bool) -> None: ...
    def capture_image(self) -> None: ...
    def calibrate_camera(self) -> None: ...
    def calibrate_robot(self) -> None: ...
