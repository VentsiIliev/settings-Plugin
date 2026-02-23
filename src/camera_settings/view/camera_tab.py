from src.settings.settings_view.settings_view import SettingsView
from src.camera_settings.view.camera_settings_schema import (
    CORE_GROUP,
    CONTOUR_GROUP,
    PREPROCESSING_GROUP,
    CALIBRATION_GROUP,
    BRIGHTNESS_GROUP,
    ARUCO_GROUP,
)
from src.camera_settings.mapper import CameraSettingsMapper


def camera_tab_factory(parent=None) -> SettingsView:
    view = SettingsView(
        component_name="CameraSettings",
        mapper=CameraSettingsMapper.to_flat_dict,
        parent=parent,
    )
    view.add_tab("Core",          [CORE_GROUP])
    view.add_tab("Detection",     [CONTOUR_GROUP, PREPROCESSING_GROUP])
    view.add_tab("Calibration",   [CALIBRATION_GROUP])
    view.add_tab("Brightness",    [BRIGHTNESS_GROUP])
    view.add_tab("ArUco",         [ARUCO_GROUP])
    return view
