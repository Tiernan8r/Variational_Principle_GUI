import matplotlib
import variational_principle.json_data
import code.data_handler as data_handler

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class EmbeddedGraph(QtWidgets.QWidget):

    def __init__(self, graph_widget, json_data, computed_data=None):
        super().__init__(parent=graph_widget)

        self.graph_widget = graph_widget
        self.json_data = json_data
        self.computed_data = computed_data

        self.current_item = "potential"

        self._setup_canvas()
        self._setup_layouts()

    def _setup_canvas(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot()

        self.figure_canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.figure_canvas, self)

    def _setup_layouts(self):
        graph_layout = QtWidgets.QVBoxLayout()
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.figure_canvas)

        self.graph_widget.setLayout(graph_layout)

    def display(self, name=None):

        if name is None:
            name = self.current_item

        if self.computed_data is None:
            return

        psi = self.computed_data.get_array(name)

        if psi is None:
            #TODO error
            return
        self.current_item = name

        V = self.computed_data.get_array("potential")
        r = self.computed_data.get_array("position")
        if V is None or r is None:
            # TODO error
            return

        self.axes.clear()
        #TODO change from reading config file to deriving from given data
        if self.json_data.num_dimensions == 1:

            legend = [name]
            psi_scale = 1
            if self.json_data.plot_with_potential and name != "potential":
                self.axes.plot(r[0], V)
                psi_scale = self.json_data.plot_scale
                legend.insert(0, "potential")

            # self.axes.plot(r[0], all_psi[0] * psi_scale)
            title = "Plot of {} of the {}:".format(name, self.json_data.label)
            self._plot_line(r[0], psi * psi_scale, title, "x", "y", legend)

        elif self.json_data.num_dimensions == 2:
            #TODO implement
            pass
        elif self.json_data.num_dimensions == 3:
            #TODO implement
            pass
        else:
            #TODO implement
            pass

        self.figure_canvas.draw()

    def _plot_line(self, x, y, title, xlabel, ylabel, legend=None):
        self.axes.plot(x, y)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        self.axes.legend(legend)

    def list_widget_item_change(self, to_item, from_item):
        if to_item is None:
            #TODO error log
            return

        if self.computed_data is None:
            #TODO error
            return

        self.display(to_item.text())


