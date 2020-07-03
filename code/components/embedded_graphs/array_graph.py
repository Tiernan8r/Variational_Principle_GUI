from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import logging
from code.components.graphs_tab.list_entry import ListEntry
from code.components.embedded_graphs.embedded_graph import EmbeddedGraph


class ArrayGraph(EmbeddedGraph):

    def __init__(self, graph_widget, computed_data):
        super().__init__(graph_widget, computed_data)
        self.logger = logging.getLogger(__name__)

    def _setup_canvas(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot()

        self.figure_canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.figure_canvas, self)

    def _setup_layouts(self):

        parent_layout = QtWidgets.QGridLayout()
        parent_layout.addWidget(self.toolbar)
        parent_layout.addWidget(self)

        graph_layout = QtWidgets.QGridLayout()
        graph_layout.addWidget(self.figure_canvas)

        self.setLayout(graph_layout)
        self.graph_widget.setLayout(parent_layout)

    def display(self, list_entry: ListEntry = None, plot_number=-1):

        if list_entry is None:
            self.logger.warning("Attempted to plot with None data given, using previous value instead.")
            if self.current_list_entry is not None:
                list_entry = self.current_list_entry
            else:
                self.logger.warning("Couldn't find previous list entry, returning.")
                return
        self.current_list_entry = list_entry

        if self.computed_data is None:
            self.logger.warning("The ComputedData object is None!")
            return

        key = list_entry.key
        if key == self.computed_data.r_key:
            self.computed_data.r = list_entry.value
            self.logger.debug("Given position array, storing it.")
            return
        if key == self.computed_data.v_key:
            self.logger.debug("Given potential array, storing for future reference.")
            self.computed_data.V = list_entry.value

        # TODO remove hardcoding of total number of plot options?
        if plot_number < 0:
            plot_number = self.current_plot_index
        elif plot_number > 2:
            plot_number = 2
        self.current_plot_index = plot_number

        self.figure.clear(keep_observers=True)
        self.axes = self.figure.add_subplot()

        if self.computed_data.r is None:
            self.logger.warning("Attempted to plot graph when position vector not given, returning.")
            return

        psi = list_entry.value

        if psi is None:
            self.logger.warning("Cannot display, psi is None!")
            return
        self.current_item = key

        r, V = self.computed_data.r, self.computed_data.V
        if r is None or V is None:
            self.logger.warning("Cannot display, V or r is None!")
            return

        self.axes.clear()

        title = "Plot of {} of the {}:".format(key, self.computed_data.label)
        xlabel, ylabel, zlabel = "$x$", "$y$", "$z$"

        D = self.computed_data.num_dimensions
        if D == 1:

            legend = [key]

            psi_scale = 1
            ylabel = "$\psi$"

            if self.computed_data.plot_with_potential and key != "potential":
                self.axes.plot(r[0], V)

                psi_scale = self.computed_data.plot_scale
                ylabel = "$V$"

                legend.insert(0, "potential")

            self._plot_line(r[0], psi * psi_scale, title, xlabel, ylabel, legend)

        elif D == 2:

            zlabel = "$\psi$"
            if key == "potential":
                zlabel = "$V$"

            if plot_number == 0:
                self._plot_image(*r, psi, title, xlabel, ylabel)
            elif plot_number == 1:
                self._plot_wireframe(*r, psi, title, xlabel, ylabel, zlabel)
            else:
                self._plot_surface(*r, psi, title, xlabel, ylabel, zlabel)

        elif D == 3:
            self._plot_3D_scatter(*r, psi, title, xlabel, ylabel, zlabel)
        else:
            self.logger.warning("Attempt to call plotting for over 3 dimensions, not implemented.")
            pass

        self.figure_canvas.draw()