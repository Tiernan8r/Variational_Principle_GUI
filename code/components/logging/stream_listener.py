from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread


class StreamListener(QtCore.QObject):
    log_received = pyqtSignal(str)

    def __init__(self, q, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = q

    @pyqtSlot()
    def receive(self):
        while True:
            while len(self.queue) > 0:
                text = self.queue.popleft()
                self.log_received.emit(text)
            QThread.sleep(1)