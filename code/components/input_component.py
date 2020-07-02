from code.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets
import logging
from code.checkbox_parser import parse_check_value


class InputComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.input_widgets = {}
        self.logger = logging.getLogger(__name__)
        super().__init__(main_window, computed_data, *args, **kwargs)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)

        lineEdits = self.main_window.findChildren(QtWidgets.QLineEdit)
        for lineEdit in lineEdits:
            key = None
            if lineEdit.displayText() == "Linear Harmonic Oscillator":
                key = "label"

            if key is not None:
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

        checkBoxes = self.main_window.findChildren(QtWidgets.QCheckBox)
        for checkBox in checkBoxes:
            if checkBox.objectName() == "plotWithPotentialCheckBox":
                checkBox.stateChanged.connect(self.check_box_update(checkBox, "plot_with_potential"))
                # checkBox.setTristate(False)

    def _generic_update(self, widget, key, setter: str, getter: str, parser=None, shared_value=False):

        # config_reader = self.computed_data.__getattribute__(key)
        file_value = getattr(self.computed_data, key)
        if parser is not None:
            print("FROM FILE BEFORE:", file_value)
            file_value = parser(file_value)
        print("FROM FILE: ", file_value)

        get_attribute = None
        unparsed_get_attribute = getattr(widget, getter)
        if parser is not None:
            print("UNPARSED PRESET VALUE:", unparsed_get_attribute())

            def parsed_get_attribute():
                return parser(unparsed_get_attribute())
            get_attribute = parsed_get_attribute
        else:
            get_attribute = unparsed_get_attribute
        print("PRESET VALUE:", get_attribute())

        getattr(widget, setter)(file_value)
        all_widgets = self.input_widgets.get(key, [])
        if widget not in all_widgets:
            all_widgets.append(widget)
        self.input_widgets[key] = all_widgets
        print("ALL WIDGETS FOR KEY:", key, "ARE:", all_widgets)
        print()

        def save_edit():
            val = get_attribute()
            setattr(self.computed_data, key, val)
            all_widgets = self.input_widgets.get(key)
            for w in all_widgets:
                if shared_value:
                    getattr(w, setter)(val)
            self.logger.debug("Saved '%s' to config file under key '%s'." % (val, key))

        return save_edit

    def check_box_update(self, check_box, key):
        return self._generic_update(check_box, key, "setCheckState", "checkState", parser=parse_check_value)

    def spin_box_update(self, spinBox, key):
        return self._generic_update(spinBox, key, "setValue", "value")

    def line_edit_config(self, lineEdit, key):
        return self._generic_update(lineEdit, key, "setText", "displayText", shared_value=True)


