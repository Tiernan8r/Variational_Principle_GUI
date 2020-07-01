from code.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets
import logging
from code.checkbox_parser import parse_check_value


class InputComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        # TODO move the dict back to main_window?
        self.widget_dict = {}
        self.logger = logging.getLogger(__name__)
        super().__init__(main_window, computed_data, *args, **kwargs)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)

        lineEdits = self.main_window.findChildren(QtWidgets.QLineEdit)
        for lineEdit in lineEdits:
            key = None
            if lineEdit.displayText() == "Linear Harmonic Oscillator":
                key = "label"

            if not key is None:
                lineEdit.editingFinished.connect(self.line_edit_config(lineEdit, key))

        spinBoxes = self.main_window.findChildren((QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox))
        for spinBox in spinBoxes:
            key = None

            val = spinBox.value()
            if val == -10:
                key = "start"
            elif val == 10:
                key = "stop"
            elif val == 2:
                key = "num_states"
            elif val == 1:
                key = "num_dimensions"
            elif val == 100:
                key = "num_samples"
            elif val == 5:
                key = "num_iterations"
            elif val == 30:
                key = "plot_scale"

            if key is not None:
                spinBox.valueChanged.connect(self.spin_box_update(spinBox, key))

        checkBox = self.main_window.findChild(QtWidgets.QCheckBox)
        checkBox.stateChanged.connect(self.check_box_config(checkBox, "plot_with_potential"))

    # TODO abstract these methods somehow?
    def spin_box_update(self, spinBox, key):
        spinBox.setValue(self.computed_data.__getattribute__(key))
        all_spin_boxes = self.widget_dict.get(key, [])
        all_spin_boxes.append(spinBox)
        self.widget_dict[key] = all_spin_boxes

        def save_edit():
            self.computed_data.__setattr__(key, spinBox.value())
            widgets = self.widget_dict.get(key)
            for w in widgets:
                w.setValue(spinBox.value())
            self.logger.debug("Saved '%s' to config file under key '%s'." % (spinBox.value(), key))

        return save_edit

    def line_edit_config(self, lineEdit, key):

        lineEdit.setText(self.computed_data.__getattribute__(key))
        all_line_edits = self.widget_dict.get(key, [])
        all_line_edits.append(lineEdit)
        self.widget_dict[key] = all_line_edits

        def save_edit():
            self.computed_data.__setattr__(key, lineEdit.displayText())
            widgets = self.widget_dict.get(key)
            for w in widgets:
                w.setText(lineEdit.displayText())
            self.logger.debug("Saved '%s' to config file under key '%s'." % (lineEdit.displayText(), key))

        return save_edit

    def check_box_config(self, checkBox, key):

        check_value = parse_check_value(self.computed_data.__getattribute__(key))
        checkBox.setCheckState(check_value)

        all_check_boxes = self.widget_dict.get(key, [])
        all_check_boxes.append(checkBox)
        self.widget_dict[key] = all_check_boxes

        def save_edit():
            checked = checkBox.checkState()
            self.computed_data.__setattr__(key, parse_check_value(checked))
            widgets = self.widget_dict.get(key)
            for w in widgets:
                w.setCheckState(checked)
            self.logger.debug("Saved '%s' to config file under key '%s'." % (bool(checked), key))

        return save_edit
