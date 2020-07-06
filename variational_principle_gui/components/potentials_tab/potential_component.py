import variational_principle_gui.components.abstract_component as ac
from PyQt5 import QtWidgets, Qt
from variational_principle_gui.components.embedded_graphs.potential_graph import PotentialGraph
import variational_principle.potential_handling.potential as pot


class PotentialComponent(ac.AbstractComponent):

    def __init__(self, main_window, computed_data):
        self.potential_selector, self.potential_text, self.potential_graph_widget = None, None, None
        self.potential_graph = None
        self.all_potentials = sorted(pot.list_potentials())
        super().__init__(main_window, computed_data)

    def setup_signals(self):

        combo_boxes = self.main_window.findChildren(QtWidgets.QComboBox)
        for combo_box in combo_boxes:
            if combo_box.objectName() == "potentialsComboBox":
                self.potential_selector = combo_box
                self.potential_selector.activated.connect(self.change_potential)
            elif combo_box.objectName() == "plotTypeBox_2":
                combo_box.activated.connect(self.plot_type_changed)

        plain_text_edits = self.main_window.findChildren(QtWidgets.QPlainTextEdit)
        for plain_text_edit in plain_text_edits:
            if plain_text_edit.objectName() == "potentialTextEdit":
                self.potential_text = plain_text_edit
                self.potential_text.textChanged.connect(self.write_to_potential_file)

        all_widgets = self.main_window.findChildren(QtWidgets.QWidget)
        for widget in all_widgets:
            if widget.objectName() == "potentialGraphWidget":
                self.potential_graph_widget = widget
                self.potential_graph = PotentialGraph(widget, self.computed_data)

        self.populate_potential_selector()

    def populate_potential_selector(self):
        self.potential_selector.clear()
        self.all_potentials.remove("square_well")
        for potential in self.all_potentials:
            self.potential_selector.addItem(potential)

        for i in range(self.potential_selector.count()):
            if self.potential_selector.itemText(i) == self.computed_data.potential_name:
                self.potential_selector.setCurrentIndex(i)
                self.change_potential(i)
                break

    def change_potential(self, index):
        potential = self.all_potentials[index]
        self.computed_data.potential_name = potential

        self.computed_data.label = pot.potential_display_name(potential)
        all_line_edits = self.main_window.input_component.input_widgets["label"]
        for line_edit in all_line_edits:
            line_edit.setText(self.computed_data.label)

        self.potential_graph.display(potential)
        self.display_potential_file(index)

    def plot_type_changed(self, i):
        self.potential_graph.plot_number = i
        self.potential_graph.display()

    def display_potential_file(self, index):
        potential_name = self.all_potentials[index]
        full_path = pot.full_potential_path(potential_name)

        with open(full_path, "r") as potential_file:
            self.potential_text.clear()
            for line in potential_file.readlines():
                self.potential_text.moveCursor(Qt.QTextCursor.End)
                self.potential_text.insertPlainText(line)

                if potential_name is "custom":
                    self.potential_text.setReadOnly(False)
                else:
                    self.potential_text.setReadOnly(True)

    def write_to_potential_file(self):
        # text = self.potential_text.toPlainText()
        # full_path = pot.full_potential_path(self.computed_data.potential_name)
        # TODO
        pass
