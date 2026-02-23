"""Tests for src/settings/core/settings_view.py"""
import pytest
from PyQt6.QtWidgets import QWidget

from src.settings.settings_view import SettingField, SettingGroup
from src.settings.settings_view import SettingsView


def _group(title, *fields):
    return SettingGroup(title=title, fields=list(fields))


def _spinbox(key, default=0):
    return SettingField(key, key.capitalize(), "spinbox",
                        default=default, min_val=0, max_val=1000, step=1)


def _text(key, default=""):
    return SettingField(key, key.capitalize(), "line_edit", default=default)


@pytest.fixture
def view(qapp):
    v = SettingsView(component_name="Test")
    v.add_tab("Tab1", [_group("G1", _spinbox("speed", 10), _spinbox("accel", 20))])
    v.add_tab("Tab2", [_group("G2", _text("name", "Robot"))])
    return v


class TestSettingsViewTabs:
    def test_tab_count(self, view):
        assert view._tabs.count() == 2

    def test_tab_titles(self, view):
        assert view._tabs.tabText(0) == "Tab1"
        assert view._tabs.tabText(1) == "Tab2"

    def test_add_raw_tab(self, qapp):
        v = SettingsView(component_name="X")
        raw = QWidget()
        v.add_raw_tab("Raw", raw)
        assert v._tabs.count() == 1
        assert v._tabs.tabText(0) == "Raw"

    def test_raw_tab_not_in_groups(self, qapp):
        v = SettingsView(component_name="X")
        v.add_raw_tab("Raw", QWidget())
        # Raw tab contributes no schema groups
        assert v._groups == []

    def test_multiple_groups_in_tab(self, qapp):
        g1 = _group("G1", _spinbox("a"))
        g2 = _group("G2", _spinbox("b"))
        v = SettingsView(component_name="X")
        v.add_tab("Combined", [g1, g2])
        assert len(v._groups) == 2


class TestSettingsViewSetValues:
    def test_set_values_pushes_to_groups(self, view):
        view.set_values({"speed": 99, "accel": 50})
        vals = view.get_values()
        assert vals["speed"] == 99.0
        assert vals["accel"] == 50.0

    def test_set_values_ignores_unknown_keys(self, view):
        view.set_values({"nonexistent": 42})
        vals = view.get_values()
        assert "nonexistent" not in vals

    def test_set_values_partial_update(self, view):
        view.set_values({"speed": 777})
        vals = view.get_values()
        assert vals["speed"] == 777.0
        assert vals["accel"] == 20.0  # default unchanged


class TestSettingsViewGetValues:
    def test_get_values_returns_all_keys(self, view):
        vals = view.get_values()
        assert "speed" in vals
        assert "accel" in vals
        assert "name" in vals

    def test_get_values_defaults(self, view):
        vals = view.get_values()
        assert vals["speed"] == 10.0
        assert vals["accel"] == 20.0
        assert vals["name"] == "Robot"

    def test_round_trip(self, view):
        view.set_values({"speed": 42, "accel": 7, "name": "HAL"})
        vals = view.get_values()
        assert vals["speed"] == 42.0
        assert vals["accel"] == 7.0
        assert vals["name"] == "HAL"


class TestSettingsViewLoad:
    def test_load_requires_mapper(self, qapp):
        v = SettingsView(component_name="X")
        v.add_tab("T", [_group("G", _spinbox("x"))])
        with pytest.raises(RuntimeError, match="No mapper"):
            v.load(object())

    def test_load_with_mapper(self, qapp):
        mapper = lambda model: {"x": model.x_val}

        class FakeModel:
            x_val = 77

        v = SettingsView(component_name="X", mapper=mapper)
        v.add_tab("T", [_group("G", _spinbox("x", default=0))])
        v.load(FakeModel())
        assert v.get_values()["x"] == 77.0


class TestSettingsViewSaveRequested:
    def test_save_button_emits_signal(self, view):
        received = []
        view.save_requested.connect(received.append)
        view._save_btn.click()
        assert len(received) == 1
        assert isinstance(received[0], dict)

    def test_save_emits_current_values(self, view):
        view.set_values({"speed": 55})
        received = []
        view.save_requested.connect(received.append)
        view._save_btn.click()
        assert received[0]["speed"] == 55.0


class TestSettingsViewValueChangedSignal:
    def test_spinbox_change_propagates_signal(self, view):
        received = []
        view.value_changed_signal.connect(lambda k, v, c: received.append((k, v, c)))
        # Directly increment the spinbox in the first group
        view._groups[0]._widgets["speed"].plus_btn.click()
        assert len(received) == 1
        key, val, component = received[0]
        assert key == "speed"
        assert val == 11.0
        assert component == "Test"

    def test_component_name_in_signal(self, qapp):
        v = SettingsView(component_name="MyComponent")
        v.add_tab("T", [_group("G", _spinbox("x", default=0))])
        received = []
        v.value_changed_signal.connect(lambda k, val, c: received.append(c))
        v._groups[0]._widgets["x"].plus_btn.click()
        assert received == ["MyComponent"]
