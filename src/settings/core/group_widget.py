from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QComboBox, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

from src.settings.core.schema import SettingGroup, SettingField
from src.settings.core.touch_spinbox import TouchSpinBox
from src.settings.core.int_list_widget import IntListWidget
from src.settings.core.styles import GROUP_STYLE, LABEL_STYLE, PRIMARY, PRIMARY_DARK, BORDER


_COMBO_STYLE = f"""
QComboBox {{
    background: white;
    color: #333333;
    border: 2px solid {BORDER};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12pt;
    min-height: 56px;
}}
QComboBox:hover {{ border-color: {PRIMARY}; }}
QComboBox::drop-down {{ border: none; width: 40px; }}
QComboBox QAbstractItemView {{
    background: white;
    color: #333333;
    selection-background-color: rgba(122, 90, 248, 0.12);
    selection-color: {PRIMARY_DARK};
    font-size: 11pt;
    padding: 8px;
}}
"""

_LINE_EDIT_STYLE = f"""
QLineEdit {{
    background: white;
    color: #333333;
    border: 2px solid {BORDER};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12pt;
    min-height: 56px;
}}
QLineEdit:focus {{ border-color: {PRIMARY}; }}
"""


class GenericSettingGroup(QGroupBox):
    """
    Schema-driven QGroupBox — touch-friendly, 2-column grid.

    Layout per field:
        ┌─────────────┐  ┌─────────────┐
        │ Label       │  │ Label       │
        │ [  widget ] │  │ [  widget ] │
        └─────────────┘  └─────────────┘

    Fields with widget_type="int_list" always span both columns.

    Signals:
        value_changed(key: str, value: object)
    """

    value_changed = pyqtSignal(str, object)

    def __init__(self, group: SettingGroup, parent=None):
        super().__init__(group.title, parent)
        self.setStyleSheet(GROUP_STYLE)
        self._group = group
        self._widgets: dict = {}
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout()
        outer.setContentsMargins(12, 16, 12, 12)
        outer.setSpacing(0)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        row = 0
        col = 0
        for f in self._group.fields:
            cell = QWidget()
            cell.setStyleSheet("background: transparent;")
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(6)

            label = QLabel(f.label)
            label.setStyleSheet(LABEL_STYLE)
            cell_layout.addWidget(label)

            widget = self._create_widget(f)
            cell_layout.addWidget(widget)
            self._widgets[f.key] = widget

            if f.widget_type == "int_list":
                # Flush to start of row if needed, then span both columns
                if col == 1:
                    row += 1
                grid.addWidget(cell, row, 0, 1, 2)
                row += 1
                col = 0
            else:
                grid.addWidget(cell, row, col)
                col += 1
                if col == 2:
                    col = 0
                    row += 1

        outer.addLayout(grid)
        self.setLayout(outer)

    def _create_widget(self, f: SettingField):
        if f.widget_type == "combo":
            w = QComboBox()
            w.setStyleSheet(_COMBO_STYLE)
            w.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            for choice in (f.choices or []):
                w.addItem(str(choice))
            if f.default is not None:
                idx = w.findText(str(f.default))
                if idx >= 0:
                    w.setCurrentIndex(idx)
            w.currentTextChanged.connect(lambda val, k=f.key: self.value_changed.emit(k, val))
            return w

        if f.widget_type == "line_edit":
            w = QLineEdit()
            w.setStyleSheet(_LINE_EDIT_STYLE)
            if f.default is not None:
                w.setText(str(f.default))
            w.textChanged.connect(lambda text, k=f.key: self.value_changed.emit(k, text))
            return w

        if f.widget_type == "int_list":
            w = IntListWidget(min_val=int(f.min_val), max_val=int(f.max_val))
            if f.default is not None:
                w.set_ids(str(f.default))
            w.valueChanged.connect(lambda val, k=f.key: self.value_changed.emit(k, val))
            return w

        # spinbox / double_spinbox → TouchSpinBox
        decimals = f.decimals if f.widget_type == "double_spinbox" else 0
        w = TouchSpinBox(
            min_val=f.min_val,
            max_val=f.max_val,
            initial=float(f.default) if f.default is not None else 0.0,
            step=f.step,
            decimals=decimals,
            step_options=f.step_options,
            suffix=f.suffix,
        )
        w.valueChanged.connect(lambda val, k=f.key: self.value_changed.emit(k, val))
        return w

    # ── public API ────────────────────────────────────────────────────────────

    def set_values(self, values: dict):
        for key, widget in self._widgets.items():
            if key not in values:
                continue
            val = values[key]
            if isinstance(widget, IntListWidget):
                widget.blockSignals(True)
                try:
                    widget.set_ids(val)
                finally:
                    widget.blockSignals(False)
            elif isinstance(widget, TouchSpinBox):
                widget.blockSignals(True)
                try:
                    widget.setValue(float(val))
                finally:
                    widget.blockSignals(False)
            elif isinstance(widget, QLineEdit):
                widget.blockSignals(True)
                try:
                    widget.setText(str(val))
                finally:
                    widget.blockSignals(False)
            elif isinstance(widget, QComboBox):
                widget.blockSignals(True)
                try:
                    idx = widget.findText(str(val))
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
                finally:
                    widget.blockSignals(False)

    def get_values(self) -> dict:
        result = {}
        for key, widget in self._widgets.items():
            if isinstance(widget, IntListWidget):
                result[key] = widget.get_ids()
            elif isinstance(widget, TouchSpinBox):
                result[key] = widget.value()
            elif isinstance(widget, QLineEdit):
                result[key] = widget.text()
            elif isinstance(widget, QComboBox):
                result[key] = widget.currentText()
        return result
