import matplotlib

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class EmbeddedGraph(QtWidgets.QWidget):

    def __init__(self, graph_widget):
        super().__init__(parent=graph_widget)
        self.graph_widget = graph_widget

        self._setup_canvas()
        self._setup_layouts()

    def _setup_canvas(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self.figure_canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.figure_canvas, self)

    def _setup_layouts(self):
        graph_layout = QtWidgets.QVBoxLayout()
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.figure_canvas)

        self.setLayout(graph_layout)

        parent_layout = QtWidgets.QVBoxLayout()
        parent_layout.addWidget(self)
        self.graph_widget.setLayout(parent_layout)

    def display(self):
        self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.figure_canvas.draw()
