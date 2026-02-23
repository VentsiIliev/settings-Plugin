"""Tests for src/settings/core/touch_spinbox.py"""
import pytest
from src.settings.settings_view import TouchSpinBox


@pytest.fixture
def spin(qapp):
    return TouchSpinBox(min_val=0, max_val=10, initial=5, step=1, decimals=0)


class TestTouchSpinBoxInitialValue:
    def test_value_is_set(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=42, step=1, decimals=0)
        assert w.value() == 42.0

    def test_initial_clamped_to_min(self, qapp):
        w = TouchSpinBox(min_val=10, max_val=50, initial=0, step=1, decimals=0)
        assert w.value() == 10.0

    def test_initial_clamped_to_max(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=50, initial=999, step=1, decimals=0)
        assert w.value() == 50.0

    def test_label_shows_value(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=7, step=1, decimals=0)
        assert "7" in w.value_label.text()

    def test_label_shows_suffix(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=5, step=1, decimals=0, suffix=" mm")
        assert w.value_label.text().endswith(" mm")


class TestTouchSpinBoxIncrementDecrement:
    def test_increment(self, spin):
        spin.plus_btn.click()
        assert spin.value() == 6.0

    def test_decrement(self, spin):
        spin.minus_btn.click()
        assert spin.value() == 4.0

    def test_increment_clamps_at_max(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=3, initial=3, step=1, decimals=0)
        w.plus_btn.click()
        assert w.value() == 3.0

    def test_decrement_clamps_at_min(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=10, initial=0, step=1, decimals=0)
        w.minus_btn.click()
        assert w.value() == 0.0

    def test_minus_disabled_at_min(self, qapp):
        w = TouchSpinBox(min_val=5, max_val=10, initial=5, step=1, decimals=0)
        assert not w.minus_btn.isEnabled()

    def test_plus_disabled_at_max(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=5, initial=5, step=1, decimals=0)
        assert not w.plus_btn.isEnabled()

    def test_plus_enabled_below_max(self, spin):
        assert spin.plus_btn.isEnabled()

    def test_minus_enabled_above_min(self, spin):
        assert spin.minus_btn.isEnabled()

    def test_step_affects_increment(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=10, step=5, decimals=0)
        w.plus_btn.click()
        assert w.value() == 15.0

    def test_float_step(self, qapp):
        w = TouchSpinBox(min_val=0.0, max_val=5.0, initial=1.0, step=0.5, decimals=1)
        w.plus_btn.click()
        assert abs(w.value() - 1.5) < 1e-9


class TestTouchSpinBoxSignal:
    def test_increment_emits_value_changed(self, spin):
        received = []
        spin.valueChanged.connect(received.append)
        spin.plus_btn.click()
        assert len(received) == 1
        assert received[0] == 6.0

    def test_decrement_emits_value_changed(self, spin):
        received = []
        spin.valueChanged.connect(received.append)
        spin.minus_btn.click()
        assert received == [4.0]

    def test_no_signal_when_clamped_at_max(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=5, initial=5, step=1, decimals=0)
        received = []
        w.valueChanged.connect(received.append)
        w.plus_btn.click()
        assert received == []

    def test_set_value_does_not_emit(self, spin):
        received = []
        spin.valueChanged.connect(received.append)
        spin.setValue(3)
        assert received == []


class TestTouchSpinBoxSetValue:
    def test_set_value_updates_display(self, spin):
        spin.setValue(9)
        assert spin.value() == 9.0
        assert "9" in spin.value_label.text()

    def test_set_value_clamps_high(self, spin):
        spin.setValue(999)
        assert spin.value() == 10.0

    def test_set_value_clamps_low(self, spin):
        spin.setValue(-50)
        assert spin.value() == 0.0


class TestTouchSpinBoxClear:
    def test_clear_resets_to_min_when_min_zero(self, spin):
        spin.setValue(7)
        spin.clear()
        assert spin.value() == 0.0

    def test_clear_with_positive_min(self, qapp):
        w = TouchSpinBox(min_val=3, max_val=10, initial=7, step=1, decimals=0)
        w.clear()
        assert w.value() == 3.0


class TestTouchSpinBoxStepPills:
    def test_no_pills_when_single_option(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=0, step=1, decimals=0,
                         step_options=[1])
        assert len(w._step_btns) == 0
        assert w.height() == 72

    def test_no_pills_when_no_options(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=0, step=1, decimals=0)
        assert len(w._step_btns) == 0
        assert w.height() == 72

    def test_pills_shown_for_multiple_options(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=0, step=1, decimals=0,
                         step_options=[1, 5, 10])
        assert len(w._step_btns) == 3
        assert w.height() == 128

    def test_selecting_pill_changes_step(self, qapp):
        w = TouchSpinBox(min_val=0, max_val=100, initial=0, step=1, decimals=0,
                         step_options=[1, 5, 10])
        w._step_btns[5].click()
        w.plus_btn.click()
        assert w.value() == 5.0

    def test_decimals_shown_for_double(self, qapp):
        w = TouchSpinBox(min_val=0.0, max_val=1.0, initial=0.5, step=0.1, decimals=2)
        assert "0.50" in w.value_label.text()
