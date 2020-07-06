from variational_principle_gui.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets
from variational_principle_gui.components.embedded_graphs.energy_graph import EnergyGraph
import logging


class EnergyComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialising EnergyComponent object")
        self.energy_graph_widget = None
        self.energies_scroll_area = None
        self.num_energies = 0
        super().__init__(main_window, computed_data, *args, **kwargs)
        self.reset()

    def find_graph_widget(self):
        self.logger.debug("Finding the widget to embed plots to:")
        all_widgets = self.main_window.findChildren(QtWidgets.QWidget)
        for widget in all_widgets:
            if widget.objectName() == "energyGraphWidget":
                self.energy_graph_widget = EnergyGraph(widget, self.computed_data)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)
        self.find_graph_widget()

        scroll_areas = self.main_window.findChildren(QtWidgets.QWidget)
        for scroll_area in scroll_areas:
            if scroll_area.objectName() == "energiesScrollArea":
                self.energies_scroll_area = scroll_area

        self.main_window.thread_compute.energy_received.connect(self.new_energy)
        self.main_window.thread_compute.new_calculation.connect(self.reset)

    def reset(self):
        self.num_energies = 0
        for widget in self.energies_scroll_area.findChildren(QtWidgets.QWidget):
            widget.close()

        self.energy_graph_widget.reset()

    def new_energy(self, energy):
        container_widget = QtWidgets.QWidget(parent=self.energies_scroll_area)
        container_layout = QtWidgets.QHBoxLayout()

        key = "state_{}:".format(self.num_energies)
        label_widget = QtWidgets.QLabel(parent=container_widget, text=key)
        container_layout.addWidget(label_widget)

        energy_amount_widget = QtWidgets.QLabel(parent=container_widget, text=str(energy))
        energy_amount_widget.setFrameStyle(QtWidgets.QFrame.Box)
        container_layout.addWidget(energy_amount_widget)

        units_widget = QtWidgets.QLabel(parent=container_widget, text="eV")
        container_layout.addWidget(units_widget)

        container_widget.setLayout(container_layout)

        current_layout = self.energies_scroll_area.layout()
        if current_layout is None:
            current_layout = QtWidgets.QGridLayout()
        current_layout.addWidget(container_widget)
        self.energies_scroll_area.setLayout(current_layout)

        self.num_energies += 1

        self.energy_graph_widget.add_energy(energy)