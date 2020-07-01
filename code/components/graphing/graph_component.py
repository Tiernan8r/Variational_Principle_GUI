from code.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets
import code.components.graphing.embedded_graph as grapher
from code.components.graphing import list_view
import logging


class GraphComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialising GraphComponent object")
        super().__init__(main_window, computed_data, *args, **kwargs)

        self.logger.debug("Populating list view of available plots")
        self.list_view = list_view.ListView(self.main_window, self.computed_data)
        self.list_view.redisplay_list_view()
        self.logger.debug("Populating combo box of plot types.")
        self.populate_graph_combobox()

    def find_graph_widget(self):
        self.logger.debug("Finding the widget to embed plots to:")
        all_widgets = self.main_window.findChildren(QtWidgets.QWidget)
        for widget in all_widgets:
            if widget.objectName() == "graphsWidget":
                self.graph_widget = grapher.EmbeddedGraph(widget, self.computed_data)

    def setup_signals(self):

        self.logger = logging.getLogger(__name__)
        self.find_graph_widget()

        plot_type_selectors = self.main_window.findChildren(QtWidgets.QComboBox)
        for plot_type_selector in plot_type_selectors:
            if plot_type_selector.objectName() == "plotTypeBox" or len(plot_type_selectors) == 1:
                plot_type_selector.activated.connect(
                    self.combo_box_graph_type_changed(plot_type_selector))

        buttons = self.main_window.findChildren(QtWidgets.QAbstractButton)
        for button in buttons:
            if button.objectName() == "refreshButton":
                button.clicked.connect(self.refresh_button)

    def refresh_button(self):
        self.graph_widget.display()

    def populate_graph_combobox(self):
        combo_box = self.main_window.findChild(QtWidgets.QComboBox)
        if combo_box is None:
            self.logger.warning("Couldn't find QComboBox widget, returning.")
            return
        combo_box.clear()
        combo_box.hide()

        # TODO logs
        if self.computed_data.num_dimensions is None:
            return

        D = self.computed_data.num_dimensions
        if D == 1:
            combo_box.addItem("Line plot")
        elif D == 2:
            combo_box.addItem("Image plot")
            combo_box.addItem("Wireframe plot")
            combo_box.addItem("Surface plot")
        elif D == 3:
            combo_box.addItem("3D scatter plot")
        else:
            # TODO error log?
            pass

        self.graph_widget.current_plot_index = 0
        # can only show this as an option if there are choices?, need to remove the hide() above if removing
        if combo_box.count() > 1:
            combo_box.show()

    def combo_box_graph_type_changed(self, combo_box_widget: QtWidgets.QComboBox):

        def change(i):
            self.graph_widget.display(plot_number=i)
            # self.graph_widget.current_plot_index = i

        return change
