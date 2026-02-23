"""Tests for src/settings/core/schema.py — no QApplication needed."""
import pytest
from src.settings.settings_view import SettingField, SettingGroup


class TestSettingField:
    def test_required_fields(self):
        f = SettingField(key="foo", label="Foo", widget_type="spinbox")
        assert f.key == "foo"
        assert f.label == "Foo"
        assert f.widget_type == "spinbox"

    def test_defaults(self):
        f = SettingField(key="x", label="X", widget_type="spinbox")
        assert f.default is None
        assert f.min_val == 0
        assert f.max_val == 100
        assert f.step == 1.0
        assert f.decimals == 2
        assert f.suffix == ""
        assert f.choices is None
        assert f.step_options is None

    def test_explicit_values(self):
        f = SettingField(
            key="speed",
            label="Speed",
            widget_type="spinbox",
            default=50,
            min_val=0,
            max_val=200,
            step=5,
            decimals=0,
            suffix=" mm/s",
            step_options=[1, 5, 10],
        )
        assert f.default == 50
        assert f.max_val == 200
        assert f.suffix == " mm/s"
        assert f.step_options == [1, 5, 10]

    def test_combo_with_choices(self):
        f = SettingField(
            key="mode", label="Mode", widget_type="combo",
            default="Auto", choices=["Manual", "Auto", "Semi-Auto"],
        )
        assert f.choices == ["Manual", "Auto", "Semi-Auto"]
        assert f.default == "Auto"

    def test_double_spinbox(self):
        f = SettingField(
            key="offset", label="Offset", widget_type="double_spinbox",
            default=0.5, min_val=-10.0, max_val=10.0, decimals=3,
        )
        assert f.decimals == 3
        assert f.min_val == -10.0

    def test_int_list(self):
        f = SettingField(
            key="ids", label="IDs", widget_type="int_list",
            default="1,2,3", min_val=0, max_val=255,
        )
        assert f.widget_type == "int_list"
        assert f.default == "1,2,3"


class TestSettingGroup:
    def test_title_and_empty_fields(self):
        g = SettingGroup(title="My Group")
        assert g.title == "My Group"
        assert g.fields == []

    def test_fields_list(self):
        f1 = SettingField("a", "A", "spinbox")
        f2 = SettingField("b", "B", "line_edit")
        g = SettingGroup(title="G", fields=[f1, f2])
        assert len(g.fields) == 2
        assert g.fields[0].key == "a"
        assert g.fields[1].key == "b"

    def test_independent_field_lists(self):
        """Default factory means groups don't share the same list object."""
        g1 = SettingGroup(title="G1")
        g2 = SettingGroup(title="G2")
        g1.fields.append(SettingField("x", "X", "spinbox"))
        assert g2.fields == []
