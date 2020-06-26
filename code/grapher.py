import matplotlib
matplotlib.use('Qt5Agg')

import variational_principle.json_data
import code.data_handler as data_handler

from PyQt5 import QtWidgets
from matplotlib.pyplot import cm

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



class EmbeddedGraph(QtWidgets.QWidget):

    def __init__(self, graph_widget, json_data, computed_data=None):
        super().__init__(parent=graph_widget)

        self.graph_widget = graph_widget
        self.json_data = json_data
        self.computed_data = computed_data

        self.current_item = "potential"
        self.current_plot_index = 0

        self._setup_canvas()
        self._setup_layouts()

        self.colourbar = None

    def _setup_canvas(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot()

        self.figure_canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.figure_canvas, self)

    def _setup_layouts(self):
        graph_layout = QtWidgets.QVBoxLayout()
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.figure_canvas)

        graph_canvas_layout = QtWidgets.QGridLayout()
        self.figure_canvas.setLayout(graph_canvas_layout)

        self.graph_widget.setLayout(graph_layout)

    def display(self, name=None, plot_number=-1):

        #TODO logging?
        if name is None:
            name = self.current_item

        if self.computed_data is None:
            return

        # TODO remove hardcoding of total number of plot options?
        if plot_number < 0:
            plot_number = self.current_plot_index
        elif plot_number > 2:
            plot_number = 2

        self.figure.clear(keep_observers=True)
        self.axes = self.figure.add_subplot()

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

        title = "Plot of {} of the {}:".format(name, self.json_data.label)
        xlabel, ylabel, zlabel = "$x$", "$y$", "$z$"

        D = self.computed_data.num_dimensions
        if D == 1:

            legend = [name]

            psi_scale = 1
            ylabel = "$\psi$"

            if self.json_data.plot_with_potential and name != "potential":
                self.axes.plot(r[0], V)

                psi_scale = self.json_data.plot_scale
                ylabel = "$V$"

                legend.insert(0, "potential")

            # self.axes.plot(r[0], all_psi[0] * psi_scale)
            self._plot_line(r[0], psi * psi_scale, title, xlabel, ylabel, legend)

        elif D == 2:

            zlabel = "$\psi$"
            if name == "potential":
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
            #TODO implement
            pass

        self.figure_canvas.draw()

    def _plot_line(self, x, y, title, xlabel, ylabel, legend=None):
        self.axes.plot(x, y)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        self.axes.legend(legend)

    def _plot_image(self, x, y, z, title, xlabel, ylabel):

        # TODO overhaul colour bar selection either through a dropdown list or use some check
        colour_map = self.json_data.colourmap
        cmap = cm.get_cmap(colour_map)
        cf = self.axes.contourf(x, y, z, cmap=cmap)
        self.colourbar = self.figure.colorbar(cf)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        # self.axes.show()

    # A method to plot the 2D system as a wireframe.
    def _plot_wireframe(self, x, y, z, title, xlabel, ylabel, zlabel):
        fig = self.figure
        ax = fig.gca(projection="3d")
        ax.plot_wireframe(x, y, z)
        ax.set_zlabel(zlabel)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        # ax.show()

    # A method to plot the 2D system as a surface plot.
    def _plot_surface(self, x, y, z, title, xlabel, ylabel, zlabel):

        colour_map = self.json_data.colourmap
        cmap = cm.get_cmap(colour_map)

        fig = self.figure
        ax = fig.gca(projection="3d")
        surf = ax.plot_surface(x, y, z, cmap=cmap)
        self.colourbar = fig.colorbar(surf, ax=ax)
        ax.set_zlabel(zlabel)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        # ax.show()

    # A method to plot the 3d system as a 3D scatter plot.
    def _plot_3D_scatter(self, x, y, z, vals, title, xlabel, ylabel, zlabel):

        colour_map = self.json_data.colourmap

        fig = self.figure
        ax = fig.gca(projection='3d')

        p = ax.scatter3D(x, y, zs=z, c=vals, cmap=colour_map)
        self.colourbar = fig.colorbar(p, ax=ax)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        # plt.show()

    def list_widget_item_change(self, to_item, from_item):
        if to_item is None:
            #TODO error log
            return

        if self.computed_data is None:
            #TODO error
            return

        self.display(to_item.text())

    def combo_box_graph_type_changed(self, combo_box_widget : QtWidgets.QComboBox):

        def change(i):
            # text = combo_box_widget.currentText()
            # num_dimensions = self.computed_data.num_dimensions
            self.display(plot_number=i)
            self.current_plot_index = i

        return change


