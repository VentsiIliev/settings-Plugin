from typing import Tuple

from src.settings.core.settings_view import SettingsView
from src.settings.ui.robot_settings_tab.robot_settings_schema import (
    ROBOT_INFO_GROUP,
    GLOBAL_MOTION_GROUP,
    SAFETY_LIMITS_GROUP,
    TCP_STEP_GROUP,
    OFFSET_DIRECTION_GROUP,
    CALIBRATION_ADAPTIVE_GROUP,
    CALIBRATION_MARKER_GROUP,
)
from src.settings.ui.robot_settings_tab.mapper import RobotSettingsMapper
from src.settings.ui.robot_settings_tab.movement_groups_tab import MovementGroupsTab


def robot_tab_factory(parent=None) -> Tuple[SettingsView, MovementGroupsTab]:
    """
    Build the robot settings UI.

    Returns (view, movement_tab) so the caller can:
      - call view.load(config)  to populate flat settings
      - call movement_tab.load(config.movement_groups) to populate movement groups
      - connect movement_tab.set_current_requested / execute_trajectory_requested
        to the robot controller
    """
    movement_tab = MovementGroupsTab()

    view = SettingsView(
        component_name="RobotSettings",
        mapper=RobotSettingsMapper.to_flat_dict,
        parent=parent,
    )
    view.add_tab("General", [ROBOT_INFO_GROUP, GLOBAL_MOTION_GROUP, TCP_STEP_GROUP, OFFSET_DIRECTION_GROUP])
    view.add_tab("Safety",  [SAFETY_LIMITS_GROUP])
    view.add_raw_tab("Movement Groups", movement_tab)
    view.add_tab("Calibration", [CALIBRATION_ADAPTIVE_GROUP, CALIBRATION_MARKER_GROUP])

    return view, movement_tab
