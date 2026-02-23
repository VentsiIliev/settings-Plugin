"""Tests for src/settings/core/group_widget.py"""
import pytest
from PyQt6.QtWidgets import QComboBox, QLineEdit

from src.settings.settings_view import SettingField, SettingGroup
from src.settings.settings_view import GenericSettingGroup
from src.settings.settings_view import TouchSpinBox
from src.settings.settings_view import IntListWidget


def make_group(*fields):
    return SettingGroup(title="Test Group", fields=list(fields))


@pytest.fixture
def spin_group(qapp):
    f = SettingField("speed", "Speed", "spinbox", default=10, min_val=0, max_val=100, step=1)
    return GenericSettingGroup(make_group(f))


class TestGenericSettingGroupWidgetCreation:
    def test_spinbox_widget_created(self, qapp):
        f = SettingField("v", "V", "spinbox", default=5, min_val=0, max_val=10, step=1)
        g = GenericSettingGroup(make_group(f))
        assert isinstance(g._widgets["v"], TouchSpinBox)

    def test_double_spinbox_widget_created(self, qapp):
        f = SettingField("d", "D", "double_spinbox", default=1.5,
                         min_val=0.0, max_val=5.0, decimals=2, step=0.1)
        g = GenericSettingGroup(make_group(f))
        assert isinstance(g._widgets["d"], TouchSpinBox)

    def test_line_edit_widget_created(self, qapp):
        f = SettingField("ip", "IP", "line_edit", default="127.0.0.1")
        g = GenericSettingGroup(make_group(f))
        assert isinstance(g._widgets["ip"], QLineEdit)

    def test_combo_widget_created(self, qapp):
        f = SettingField("mode", "Mode", "combo", default="Auto",
                         choices=["Manual", "Auto"])
        g = GenericSettingGroup(make_group(f))
        assert isinstance(g._widgets["mode"], QComboBox)

    def test_int_list_widget_created(self, qapp):
        f = SettingField("ids", "IDs", "int_list", default="1,2,3",
                         min_val=0, max_val=255)
        g = GenericSettingGroup(make_group(f))
        assert isinstance(g._widgets["ids"], IntListWidget)

    def test_title_set(self, qapp):
        g = GenericSettingGroup(SettingGroup("My Settings"))
        assert g.title() == "My Settings"

    def test_all_keys_registered(self, qapp):
        fields = [
            SettingField("a", "A", "spinbox", default=0, min_val=0, max_val=10, step=1),
            SettingField("b", "B", "line_edit", default="hello"),
            SettingField("c", "C", "combo", default="X", choices=["X", "Y"]),
        ]
        g = GenericSettingGroup(make_group(*fields))
        assert set(g._widgets.keys()) == {"a", "b", "c"}


class TestGenericSettingGroupDefaults:
    def test_spinbox_default_value(self, qapp):
        f = SettingField("x", "X", "spinbox", default=42, min_val=0, max_val=100, step=1)
        g = GenericSettingGroup(make_group(f))
        assert g._widgets["x"].value() == 42.0

    def test_line_edit_default_text(self, qapp):
        f = SettingField("name", "Name", "line_edit", default="Robot")
        g = GenericSettingGroup(make_group(f))
        assert g._widgets["name"].text() == "Robot"

    def test_combo_default_selection(self, qapp):
        f = SettingField("m", "M", "combo", default="Auto",
                         choices=["Manual", "Auto", "Semi-Auto"])
        g = GenericSettingGroup(make_group(f))
        assert g._widgets["m"].currentText() == "Auto"

    def test_int_list_default_ids(self, qapp):
        f = SettingField("ids", "IDs", "int_list", default="1,2,3",
                         min_val=0, max_val=255)
        g = GenericSettingGroup(make_group(f))
        assert g._widgets["ids"].get_ids() == [1, 2, 3]


class TestGenericSettingGroupSetValues:
    def test_set_spinbox_value(self, spin_group):
        spin_group.set_values({"speed": 75})
        assert spin_group._widgets["speed"].value() == 75.0

    def test_set_line_edit_value(self, qapp):
        f = SettingField("ip", "IP", "line_edit", default="")
        g = GenericSettingGroup(make_group(f))
        g.set_values({"ip": "192.168.1.1"})
        assert g._widgets["ip"].text() == "192.168.1.1"

    def test_set_combo_value(self, qapp):
        f = SettingField("m", "M", "combo", default="A", choices=["A", "B", "C"])
        g = GenericSettingGroup(make_group(f))
        g.set_values({"m": "C"})
        assert g._widgets["m"].currentText() == "C"

    def test_set_int_list_value_from_list(self, qapp):
        f = SettingField("ids", "IDs", "int_list", default="", min_val=0, max_val=255)
        g = GenericSettingGroup(make_group(f))
        g.set_values({"ids": [10, 20, 30]})
        assert g._widgets["ids"].get_ids() == [10, 20, 30]

    def test_set_values_ignores_unknown_keys(self, spin_group):
        spin_group.set_values({"speed": 5, "unknown_key": 999})
        assert spin_group._widgets["speed"].value() == 5.0

    def test_set_values_does_not_emit_signals(self, spin_group):
        received = []
        spin_group.value_changed.connect(lambda k, v: received.append((k, v)))
        spin_group.set_values({"speed": 20})
        assert received == []


class TestGenericSettingGroupGetValues:
    def test_get_spinbox_value(self, spin_group):
        spin_group.set_values({"speed": 55})
        result = spin_group.get_values()
        assert result["speed"] == 55.0

    def test_get_line_edit_value(self, qapp):
        f = SettingField("host", "Host", "line_edit", default="localhost")
        g = GenericSettingGroup(make_group(f))
        result = g.get_values()
        assert result["host"] == "localhost"

    def test_get_combo_value(self, qapp):
        f = SettingField("m", "M", "combo", default="B", choices=["A", "B", "C"])
        g = GenericSettingGroup(make_group(f))
        result = g.get_values()
        assert result["m"] == "B"

    def test_get_int_list_value(self, qapp):
        f = SettingField("ids", "IDs", "int_list", default="5,6",
                         min_val=0, max_val=255)
        g = GenericSettingGroup(make_group(f))
        result = g.get_values()
        assert result["ids"] == [5, 6]

    def test_round_trip_spinbox(self, spin_group):
        spin_group.set_values({"speed": 33})
        assert spin_group.get_values()["speed"] == 33.0

    def test_round_trip_all_types(self, qapp):
        fields = [
            SettingField("v", "V", "spinbox", default=10, min_val=0, max_val=100, step=1),
            SettingField("t", "T", "line_edit", default="hello"),
            SettingField("c", "C", "combo", default="Y", choices=["X", "Y"]),
            SettingField("ids", "IDs", "int_list", default="1,2",
                         min_val=0, max_val=99),
        ]
        g = GenericSettingGroup(make_group(*fields))
        data = {"v": 50, "t": "world", "c": "X", "ids": [3, 4]}
        g.set_values(data)
        result = g.get_values()
        assert result["v"] == 50.0
        assert result["t"] == "world"
        assert result["c"] == "X"
        assert result["ids"] == [3, 4]


class TestGenericSettingGroupSignals:
    def test_spinbox_change_emits_value_changed(self, spin_group):
        received = []
        spin_group.value_changed.connect(lambda k, v: received.append((k, v)))
        spin_group._widgets["speed"].plus_btn.click()
        assert len(received) == 1
        assert received[0][0] == "speed"
        assert received[0][1] == 11.0

    def test_line_edit_change_emits_value_changed(self, qapp):
        f = SettingField("n", "N", "line_edit", default="")
        g = GenericSettingGroup(make_group(f))
        received = []
        g.value_changed.connect(lambda k, v: received.append((k, v)))
        g._widgets["n"].setText("abc")
        assert any(k == "n" and v == "abc" for k, v in received)

    def test_combo_change_emits_value_changed(self, qapp):
        f = SettingField("m", "M", "combo", default="A", choices=["A", "B"])
        g = GenericSettingGroup(make_group(f))
        received = []
        g.value_changed.connect(lambda k, v: received.append((k, v)))
        g._widgets["m"].setCurrentIndex(1)
        assert any(k == "m" and v == "B" for k, v in received)


class TestGenericSettingGroupIntListLayout:
    def test_int_list_widget_registered(self, qapp):
        """int_list widget must appear in _widgets after build."""
        f = SettingField("ids", "IDs", "int_list", default="", min_val=0, max_val=100)
        g = GenericSettingGroup(make_group(f))
        assert "ids" in g._widgets
        assert isinstance(g._widgets["ids"], IntListWidget)

    def test_int_list_after_odd_field_forces_new_row(self, qapp):
        """int_list after a single field (col=1 would be next) flushes to row start."""
        fields = [
            SettingField("a", "A", "spinbox", default=0, min_val=0, max_val=10, step=1),
            SettingField("ids", "IDs", "int_list", default="", min_val=0, max_val=10),
        ]
        # Must not raise and all widgets must be registered
        g = GenericSettingGroup(make_group(*fields))
        assert "a" in g._widgets
        assert "ids" in g._widgets
