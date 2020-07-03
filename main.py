import sys
from PyQt5 import QtWidgets
from code.main_window import MainWindow
import logging
import logging.config
import json
import datetime
from code.components.log_tab.standard_out_queue import StandardOutQueue


def setup_loggers():
    log_config_dict = json.load(open("data/logging.json", "r"))
    logging.config.dictConfig(log_config_dict)
    log_format = log_config_dict["formatters"]["default"]["format"]

    file_formatter = logging.Formatter(log_format)

    log_filename = "{:%Y-%m-%d}.log".format(datetime.datetime.now())
    log_file_handler = logging.FileHandler(log_filename)
    log_file_handler.setFormatter(file_formatter)

    out_queue = StandardOutQueue()
    log_widget_handler = logging.StreamHandler(out_queue)
    log_widget_handler.setFormatter(file_formatter)

    main_logger = logging.getLogger(__name__)
    main_logger.addHandler(log_file_handler)
    main_logger.addHandler(log_widget_handler)

    code_logger = logging.getLogger("code")
    code_logger.addHandler(log_file_handler)
    code_logger.addHandler(log_widget_handler)

    variational_principle_logger = logging.getLogger("variational_principle")
    variational_principle_logger.addHandler(log_file_handler)
    variational_principle_logger.addHandler(log_widget_handler)


if __name__ == "__main__":
    setup_loggers()

    logger = logging.getLogger(__name__)

    logger.debug("Setting up QApplication.")

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    logger.debug("Created application and MainWindow widget")
    main_window.show()

    sys.exit(app.exec_())
