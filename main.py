import sys
from PyQt5 import QtWidgets
from code.main_window import MainWindow
import logging


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger.debug("Setting up QApplication.")

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    logger.debug("Created application and MainWindow widget")
    main_window.show()
    logger.debug("MainWindow closed, exiting program.")
    sys.exit(app.exec_())
