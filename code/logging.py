import sys
import collections
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor


class Logger(QtCore.QObject):

    def __init__(self, log_widget, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.log_widget = log_widget
        self.queue = collections.deque()

        self.log_listener_thread = None
        self.stream_logger = None

        self.init_logging()

    def init_logging(self):
        sys.stdout = _StandardOutStream(self.queue)

        # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
        self.log_listener_thread = QtCore.QThread()
        self.stream_logger = _StreamLogger(self.queue)

        self.stream_logger.log_received.connect(self.write_log)
        self.stream_logger.moveToThread(self.log_listener_thread)
        self.log_listener_thread.started.connect(self.stream_logger.receive)
        self.log_listener_thread.start()

    @pyqtSlot(str)
    def write_log(self, text):
        self.log_widget.moveCursor(QTextCursor.End)
        self.log_widget.insertPlainText(text)


class _StandardOutStream(object):

    def __init__(self, q):
        self.queue = q

    def write(self, t):
        self.queue.append(t)

    def flush(self):
        pass


class _StreamLogger(QtCore.QObject):

    log_received = pyqtSignal(str)

    def __init__(self, q, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = q

    @pyqtSlot()
    def receive(self):
        while True:
            if len(self.queue) > 0:
                text = self.queue.popleft()
                self.log_received.emit(text)
