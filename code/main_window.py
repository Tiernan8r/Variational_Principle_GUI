import os

from PyQt5 import QtWidgets, uic
import variational_principle.json_data as json_data
import variational_principle.variation_method as vm
import code.grapher as grapher


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.json_config = json_data.JsonData()

        self.ui_widget = self.load_ui()

        self.widget_dict = {}
        self.setup_signals()

        self.graph_widget = None
        self.find_graph_widget()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "../ui/form.ui")
        ui = uic.loadUi(path, self)
        return ui

    # TODO: setup logging

    def setup_signals(self):
        lineEdits = self.ui_widget.findChildren(QtWidgets.QLineEdit)
        for lineEdit in lineEdits:
            key = None
            if lineEdit.displayText() == "Linear Harmonic Oscillator":
                key = "label"
            elif lineEdit.displayText() == "autumn":
                key = "colourmap"

            if not key is None:
                lineEdit.editingFinished.connect(self.line_edit_config(lineEdit, key))

        spinBoxes = self.ui_widget.findChildren((QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox))
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

            if not key is None:
                spinBox.valueChanged.connect(self.spin_box_update(spinBox, key))

        checkBox = self.ui_widget.findChild(QtWidgets.QCheckBox)
        checkBox.stateChanged.connect(self.check_box_config(checkBox, "plot_with_potential"))

        buttons = self.ui_widget.findChildren(QtWidgets.QAbstractButton)
        for button in buttons:
            if button.text() == "Calculate":
                button.clicked.connect(self.calculate_button)
            if button.text() == "Refresh":
                button.clicked.connect(self.refresh_button)

    def find_graph_widget(self):
        # Finding the matplotlib enmbed widget:
        all_widgets = self.ui_widget.findChildren(QtWidgets.QWidget)
        for widget in all_widgets:
            if widget.objectName() == "graphsWidget":
                self.graph_widget = grapher.EmbeddedGraph(widget)

    # TODO abstract these methods somehow?
    def spin_box_update(self, spinBox, key):
        spinBox.setValue(self.json_config.__getattribute__(key))
        all_spin_boxes = self.widget_dict.get(key, [])
        all_spin_boxes.append(spinBox)
        self.widget_dict[key] = all_spin_boxes

        def save_edit():
            self.json_config.__setattr__(key, spinBox.value())
            widgets = self.widget_dict.get(key)
            for w in widgets:
                w.setValue(spinBox.value())
            print("Saved '%s' to config file under key '%s'." % (spinBox.value(), key))

        return save_edit

    def line_edit_config(self, lineEdit, key):

        lineEdit.setText(self.json_config.__getattribute__(key))
        all_line_edits = self.widget_dict.get(key, [])
        all_line_edits.append(lineEdit)
        self.widget_dict[key] = all_line_edits

        def save_edit():
            self.json_config.__setattr__(key, lineEdit.displayText())
            widgets = self.widget_dict.get(key)
            for w in widgets:
                w.setText(lineEdit.displayText())
            print("Saved '%s' to config file under key '%s'." % (lineEdit.displayText(), key))

        return save_edit

    def check_box_config(self, checkBox, key):

        checked_bool = self.json_config.__getattribute__(key)
        # 0 is unchecked
        check_value = 0
        if checked_bool:
            # 2 is fully checked
            check_value = 2
        checkBox.setCheckState(check_value)

        all_check_boxes = self.widget_dict.get(key, [])
        all_check_boxes.append(checkBox)
        self.widget_dict[key] = all_check_boxes

        def save_edit():
            checked = checkBox.checkState()
            self.json_config.__setattr__(key, bool(checked))
            widgets = self.widget_dict.get(key)
            for w in widgets:
                w.setCheckState(checked)
            print("Saved '%s' to config file under key '%s'." % (bool(checked), key))

        return save_edit

    def calculate_button(self):
        #TODO threading
        print("CALCULATING")
        self.r, self.V, self.all_psi, self.all_E = vm.config_compute(self.json_config)
        print("DONE CALCULATING")

    def refresh_button(self):
        #TODO threading
        self.graph_widget.display()
