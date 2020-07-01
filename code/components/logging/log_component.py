from code.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets
import code.components.logging.logger as log
import logging


class LogComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger_object = None
        super().__init__(main_window, computed_data, *args, **kwargs)

    # TODO: fix stuttering from logging? probably from ui updates.
    def load_logging_widget(self):
        logger_text_box = self.main_window.ui_widget.findChild(QtWidgets.QPlainTextEdit)
        self.logger_object = log.Logger(logger_text_box)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)
        self.load_logging_widget()
