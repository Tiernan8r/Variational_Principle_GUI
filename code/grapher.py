import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import variational_principle.plot as plot
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class EmbeddedGraph(object):

    def __init__(self, graph_widget):
        self.graph_widget = graph_widget

    def display(self):
        pass