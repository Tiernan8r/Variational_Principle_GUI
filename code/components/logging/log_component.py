from code.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets, QtCore, Qt
import logging
from code.components.logging.standard_out_queue import StandardOutQueue


class LogComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.text_widget = None
        self.log_timer = None
        self.standard_out_queue = None
        super().__init__(main_window, computed_data, *args, **kwargs)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Setting up logger objects.")

        self.standard_out_queue = StandardOutQueue()
        self.text_widget = self.main_window.ui_widget.findChild(QtWidgets.QPlainTextEdit)

        self.init_logging()

    def init_logging(self):
        self.logger.debug("Setting up timer for listening for log input.")
        self.log_timer = QtCore.QTimer()
        self.log_timer.setInterval(100)
        self.log_timer.timeout.connect(self.listen)
        self.log_timer.start()

    def listen(self):
        # if not self.standard_out_queue.empty():
        while not self.standard_out_queue.empty():
            text = self.standard_out_queue.read()
            self.text_widget.moveCursor(Qt.QTextCursor.End)
            self.text_widget.insertPlainText(text)
