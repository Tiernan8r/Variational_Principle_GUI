import PyQt5.QtCore as QtCore
import logging


class AbstractComponent(QtCore.QObject):

    def __init__(self, main_window, computed_data, *args, **kwargs):

        self.logger = logging.getLogger(__name__)

        self.logger.debug("Initialising AbstractComponent object")
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.computed_data = computed_data
        self.logger.debug("Set main_window and computed_data objects.")
        self.setup_signals()
        self.logger.debug("setup signals.")

    def setup_signals(self):
        pass
