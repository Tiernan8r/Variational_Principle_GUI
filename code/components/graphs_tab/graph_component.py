from code.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets
from code.components.embedded_graphs.array_graph import ArrayGraph
from code.components.graphs_tab import list_view
import logging
from matplotlib import cm
from code.checkbox_parser import parse_check_value


class GraphComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initialising GraphComponent object")
        self.graph_widget = None
        self.colourmap_selector, self.colourmap_reversor = None, None
        self.plot_with_potential_widget, self.plot_scale_widget = None, None
        super().__init__(main_window, computed_data, *args, **kwargs)

        self.logger.debug("Populating list view of available plots")
        self.list_view = list_view.ListView(self.main_window, self.computed_data)
        self.list_view.redisplay_list_view()
        self.logger.debug("Populating combo box of plot types.")
        self.prev_num_dimensions = -1
        self.toggle_widgets_enabled()

    def find_graph_widget(self):
        self.logger.debug("Finding the widget to embed plots to:")
        all_widgets = self.main_window.findChildren(QtWidgets.QWidget)
        for widget in all_widgets:
            if widget.objectName() == "graphsWidget":
                self.graph_widget = ArrayGraph(widget, self.computed_data)

    def setup_signals(self):

        self.logger = logging.getLogger(__name__)
        self.find_graph_widget()

        combo_boxes = self.main_window.findChildren(QtWidgets.QComboBox)
        for combo_box in combo_boxes:
            if combo_box.objectName() == "plotTypeBox" or len(combo_boxes) == 1:
                combo_box.activated.connect(
                    self.combo_box_graph_type_changed)

            elif combo_box.objectName() == "colourmapComboBox":
                self.colourmap_selector = combo_box
                combo_box.activated.connect(self.colourmap_select)

                for cmap in sorted(cm.cmap_d):
                    if "_r" in cmap:
                        continue
                    else:
                        combo_box.addItem(cmap)
                old_cmap = self.computed_data.colourmap
                if old_cmap is None:
                    old_cmap = "autumn"

                default_index = combo_box.findText(old_cmap)
                combo_box.setCurrentIndex(default_index)

        check_boxes = self.main_window.findChildren(QtWidgets.QCheckBox)
        for check_box in check_boxes:
            if check_box.objectName() == "colourmapCheckBox":
                self.colourmap_reversor = check_box
                self.colourmap_reversor.stateChanged.connect(self.colourmap_reversal_toggle)
            elif check_box.objectName() == "plotWithPotentialCheckBox":
                self.plot_with_potential_widget = check_box

        spin_boxes = self.main_window.findChildren(QtWidgets.QDoubleSpinBox)
        for spin_box in spin_boxes:
            if spin_box.objectName() == "potential_scale":
                self.plot_scale_widget = spin_box
        # buttons = self.main_window.findChildren(QtWidgets.QAbstractButton)
        # for button in buttons:
        #     if button.objectName() == "refreshButton":
        #         button.clicked.connect(self.refresh_button)

    def toggle_widgets_enabled(self):

        num_dimensions = self.computed_data.num_dimensions
        if self.prev_num_dimensions == num_dimensions:
            return

        self.populate_graph_combobox()

        is_one_d = num_dimensions == 1

        self.plot_with_potential_widget.setEnabled(is_one_d)
        self.plot_scale_widget.setEnabled(is_one_d)
        self.colourmap_selector.setEnabled(not is_one_d)
        self.colourmap_reversor.setEnabled(not is_one_d)

        self.prev_num_dimensions = num_dimensions

    def colourmap_reversal_toggle(self, state):
        cmap_index = self.colourmap_selector.currentIndex()
        self.colourmap_select(cmap_index)

    def colourmap_select(self, index):

        colourmap_name = self.colourmap_selector.itemText(index)

        reversed = parse_check_value(self.colourmap_reversor.checkState())
        if reversed:
            colourmap_name += "_r"

        # self.computed_data.__setattr__("colourmap", colourmap_name)
        setattr(self.computed_data, "colourmap", colourmap_name)
        self.refresh_button()

    def refresh_button(self):
        self.populate_graph_combobox()
        self.graph_widget.display()

    def populate_graph_combobox(self):

        if self.prev_num_dimensions == self.computed_data.num_dimensions:
            self.logger.debug(
                "Previous dimension for refresh is equal to the current dimension, refresh will have no effect.")
            return

        combo_box = self.main_window.findChild(QtWidgets.QComboBox)
        if combo_box is None:
            self.logger.warning("Couldn't find QComboBox widget, returning.")
            return
        combo_box.clear()
        combo_box.hide()

        if self.computed_data.num_dimensions is None:
            self.logger.warning("Number of Dimensions is not set in the computed_data object!")
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

    def combo_box_graph_type_changed(self, i):
        self.graph_widget.display(plot_number=i)
