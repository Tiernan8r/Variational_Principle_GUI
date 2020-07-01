import sys
import collections

from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor

from code.components.logging import stream_listener, standard_out_stream


class Logger(QtCore.QObject):

    def __init__(self, log_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_widget = log_widget
        self.queue = collections.deque()

        self.log_listener_thread = None
        self.stream_listener = None

        self.init_logging()

    def init_logging(self):
        # everything written to stdout gets put into queue
        sys.stdout = standard_out_stream.StandardOutStream(self.queue)

        # create the thread that listens for data on stdout
        self.log_listener_thread = QtCore.QThread()
        # create a stream listener callback object that detects new input and
        # sends a signal to the gui thread to display it to the text object
        self.stream_listener = stream_listener.StreamListener(self.queue)
        self.stream_listener.log_received.connect(self.write_log)
        # start the listener on the thread
        self.stream_listener.moveToThread(self.log_listener_thread)
        # attach the receive() method to the thread so that it constantly listens
        self.log_listener_thread.started.connect(self.stream_listener.receive)
        self.log_listener_thread.start()

    @QtCore.pyqtSlot(str)
    def write_log(self, text):
        self.log_widget.moveCursor(QTextCursor.End)
        self.log_widget.insertPlainText(text)
