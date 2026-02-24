from typing import Tuple

from src.settings.settings_view.settings_view import SettingsView
from src.plugins.glue_settings.view.glue_settings_schema import (
    SPRAY_GROUP,
    PUMP_GROUP,
    GENERATOR_GROUP,
    TIMING_GROUP,
    RAMP_GROUP,
)
from src.plugins.glue_settings.mapper import GlueSettingsMapper
from src.plugins.glue_settings.view.glue_type_tab import GlueTypeTab


def glue_tab_factory(parent=None) -> Tuple[SettingsView, GlueTypeTab]:
    view = SettingsView(
        component_name="GlueSettings",
        mapper=GlueSettingsMapper.to_flat_dict,
        parent=parent,
    )
    view.add_tab("General", [SPRAY_GROUP, PUMP_GROUP, GENERATOR_GROUP])
    view.add_tab("Timing", [TIMING_GROUP, RAMP_GROUP])

    glue_type_tab = GlueTypeTab()
    view.add_raw_tab("Glue Types", glue_type_tab)

    return view, glue_type_tab
