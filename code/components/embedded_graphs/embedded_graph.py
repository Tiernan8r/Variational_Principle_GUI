import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
from matplotlib.pyplot import cm
import logging


class EmbeddedGraph(QtWidgets.QWidget):

    def __init__(self, graph_widget, computed_data):
        super().__init__(parent=graph_widget)
        self.logger = logging.getLogger(__name__)

        self.graph_widget = graph_widget
        self.computed_data = computed_data

        self.current_plot_index = 0
        self.current_list_entry = None
        self.current_item = None

        self.figure, self.toolbar, self.axes = None, None, None
        self.colourbar = None

        self._setup_canvas()
        self._setup_layouts()

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

    def reset(self):
        self.current_plot_index = 0
        self.current_list_entry = None

    def _plot_line(self, x, y, title, xlabel, ylabel, legend=None, line_style="-"):
        self.axes.plot(x, y, line_style)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        if legend is not None:
            self.axes.legend(legend)

    def _plot_image(self, x, y, z, title, xlabel, ylabel):

        # TODO overhaul colour bar selection either through a dropdown list or use some check
        colour_map = self.computed_data.colourmap
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

        colour_map = self.computed_data.colourmap
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

        colour_map = self.computed_data.colourmap

        fig = self.figure
        ax = fig.gca(projection='3d')

        p = ax.scatter3D(x, y, zs=z, c=vals, cmap=colour_map)
        self.colourbar = fig.colorbar(p, ax=ax)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        # plt.show()

