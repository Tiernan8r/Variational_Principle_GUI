import os
import logging.config
import json
import variational_principle.data_handling.computation_data as ci
import multiprocessing

from PyQt5 import QtWidgets, uic

import code.threading.thread_compute as tc

from code.components import input_component
from code.components.log_tab import log_component
from code.components.graphs_tab import graph_component
from code.components.energy_tab import energy_component
from code.components.potentials_tab import potential_component


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui_widget = self.load_ui()

        self.computed_data = ci.ComputationData()
        self.log_component = log_component.LogComponent(self, self.computed_data)

        self.input_component = input_component.InputComponent(self, self.computed_data)
        self.thread_compute = tc.ThreadCompute(self, self.computed_data)

        self.potential_component = potential_component.PotentialComponent(self, self.computed_data)

        self.graph_component = graph_component.GraphComponent(self, self.computed_data)
        self.energy_component = energy_component.EnergyComponent(self, self.computed_data)

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "../ui/form.ui")
        ui = uic.loadUi(path, self)
        return ui
