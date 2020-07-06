import logging
from variational_principle_gui.components.graphs_tab.list_entry import ListEntry
from variational_principle_gui.components.embedded_graphs.embedded_graph import EmbeddedGraph


class EnergyGraph(EmbeddedGraph):

    def __init__(self, graph_widget, computed_data):
        super().__init__(graph_widget, computed_data)
        self.logger = logging.getLogger(__name__)
        self._all_energies = []

    def add_energy(self, energy):
        self._all_energies.append(energy)
        self.display()

    def reset(self):
        super().reset()
        self._all_energies = []

        self.figure.clear(keep_observers=True)
        self.figure_canvas.draw()

    def display(self):

        self.figure.clear(keep_observers=True)
        self.axes = self.figure.add_subplot()

        num_energies = len(self._all_energies)
        x = range(num_energies)
        y = self._all_energies

        title = "Energy Eigenvalues for the " + self.computed_data.label + ":"
        xlabel = "State number"
        ylabel = "Energy (eV)"

        self._plot_line(x, y, title, xlabel, ylabel, line_style="x-")
        self.figure_canvas.draw()