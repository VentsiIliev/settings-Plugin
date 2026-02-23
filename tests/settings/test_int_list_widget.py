"""Tests for src/settings/core/int_list_widget.py"""
import pytest
from src.settings.settings_view import IntListWidget


@pytest.fixture
def widget(qapp):
    return IntListWidget(min_val=0, max_val=255)


class TestIntListWidgetSetIds:
    def test_set_ids_from_list(self, widget):
        widget.set_ids([1, 2, 3])
        assert widget.get_ids() == [1, 2, 3]

    def test_set_ids_from_string(self, widget):
        widget.set_ids("10,20,30")
        assert widget.get_ids() == [10, 20, 30]

    def test_set_ids_string_with_spaces(self, widget):
        widget.set_ids("5, 15, 25")
        assert widget.get_ids() == [5, 15, 25]

    def test_set_ids_clears_previous(self, widget):
        widget.set_ids([1, 2, 3])
        widget.set_ids([7, 8])
        assert widget.get_ids() == [7, 8]

    def test_set_ids_empty_list(self, widget):
        widget.set_ids([1, 2])
        widget.set_ids([])
        assert widget.get_ids() == []

    def test_set_ids_empty_string(self, widget):
        widget.set_ids([1, 2])
        widget.set_ids("")
        assert widget.get_ids() == []

    def test_set_ids_string_ignores_non_numeric(self, widget):
        widget.set_ids("1,abc,3")
        assert widget.get_ids() == [1, 3]


class TestIntListWidgetValueAlias:
    def test_value_returns_list(self, widget):
        widget.set_ids([4, 5, 6])
        assert widget.value() == [4, 5, 6]

    def test_set_value_from_list(self, widget):
        widget.setValue([10, 20])
        assert widget.get_ids() == [10, 20]

    def test_set_value_from_string(self, widget):
        widget.setValue("100,200")
        assert widget.get_ids() == [100, 200]


class TestIntListWidgetRemove:
    def test_remove_selected_item(self, widget):
        widget.set_ids([1, 2, 3])
        widget._list.setCurrentRow(1)
        widget._on_remove()
        assert widget.get_ids() == [1, 3]

    def test_remove_emits_signal(self, widget):
        widget.set_ids([1, 2, 3])
        widget._list.setCurrentRow(0)
        received = []
        widget.valueChanged.connect(received.append)
        widget._on_remove()
        assert len(received) == 1
        assert received[0] == [2, 3]

    def test_remove_no_selection_does_nothing(self, widget):
        widget.set_ids([1, 2])
        widget._list.clearSelection()
        widget._list.setCurrentRow(-1)
        widget._on_remove()
        assert widget.get_ids() == [1, 2]


class TestIntListWidgetAppend:
    def test_append_adds_item(self, widget):
        widget.set_ids([1])
        widget._append(5)
        assert 5 in widget.get_ids()

    def test_append_emits_signal(self, widget):
        received = []
        widget.valueChanged.connect(received.append)
        widget._append(42)
        assert len(received) == 1
        assert 42 in received[0]


class TestIntListWidgetUpdate:
    def test_update_changes_item(self, widget):
        widget.set_ids([1, 2, 3])
        widget._update(1, 99)
        assert widget.get_ids() == [1, 99, 3]

    def test_update_emits_signal(self, widget):
        widget.set_ids([10, 20])
        received = []
        widget.valueChanged.connect(received.append)
        widget._update(0, 55)
        assert received == [[55, 20]]


class TestIntListWidgetMinMax:
    def test_custom_range_respected(self, qapp):
        w = IntListWidget(min_val=10, max_val=50)
        assert w._min == 10
        assert w._max == 50
