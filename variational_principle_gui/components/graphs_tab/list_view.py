from PyQt5 import QtWidgets
import logging
from variational_principle_gui.components.abstract_component import AbstractComponent
from variational_principle_gui.components.graphs_tab.list_entry import ListEntry


class ListView(AbstractComponent):

    list_entry_dict = {}

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.list_entries = []
        self.list_widget = None
        self.has_potential = False
        super().__init__(main_window, computed_data, *args, **kwargs)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)

        self.list_widget = self.main_window.findChild(QtWidgets.QListWidget)
        self.list_widget.currentItemChanged.connect(self.list_widget_item_change)

        self.redisplay_list_view()

    def list_widget_item_change(self, to_item, from_item):
        if to_item is None:
            self.logger.warning("Attempt to change focus to item None!")
            return

        if self.computed_data is None:
            self.logger.warning("ComputedData object is not initialised!")
            return

        key = to_item.text()
        list_entry = self.list_entry_dict.get(key, None)
        self.main_window.graph_component.graph_widget.display(list_entry)

    def clear(self):
        self.logger.debug("Clearing previous data from list entries")

        self.list_entry_dict.clear()
        self.list_entries.clear()

        self.list_widget.clear()
        self.list_widget.hide()

        self.main_window.graph_component.graph_widget.reset()

    def add_item(self, key, value):

        current_index = self.list_widget.currentRow()
        if current_index < 0:
            current_index = 0
        self.logger.debug("Current selected item at index %d" % current_index)

        self.logger.debug("Adding new values to list entries under key '%s'" % key)
        list_entry = ListEntry(key, value)
        if key in self.list_entry_dict:
            for i in range(len(self.list_entries)):
                le = self.list_entries[i]
                if le.key == key:
                    self.list_entries[i] = list_entry
        else:
            self.list_entries.append(list_entry)
        self.list_entry_dict[key] = list_entry

        self.redisplay_list_view()
        self.list_widget.setCurrentItem(self.list_widget.item(current_index))

    def get_item(self, key):
        return self.list_entry_dict.get(key, None)

    def redisplay_list_view(self):
        if self.list_widget is None:
            self.logger.warning("Couldn't find any QListWidget widgets, returning.")
            return

        self.list_widget.clear()
        self.list_widget.hide()

        for list_entry in self.list_entries:
            key = list_entry.key

            if key == self.computed_data.r_key:
                self.main_window.graph_component.graph_widget.r = list_entry.value
                self.logger.debug("Position vector was found in list entry, passing value to graph widget.")
                continue
            if key == self.computed_data.v_key:
                self.main_window.graph_component.graph_widget.V = list_entry.value
                self.logger.debug("Potential vector was found in list entry, passing value to graph widget.")

            self.list_widget.addItem(key)

        if self.list_widget.count() > 0:
            self.list_widget.show()

