import variational_principle.variation_method as vm

from variational_principle_gui.components.abstract_component import AbstractComponent
from PyQt5 import QtWidgets, QtCore
import numpy as np
import multiprocessing
import logging


class ThreadCompute(AbstractComponent):

    stop_calculation = QtCore.pyqtSignal()
    new_calculation = QtCore.pyqtSignal()

    energy_received = QtCore.pyqtSignal(float)
    array_received = QtCore.pyqtSignal(str, np.ndarray)

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.listener_timer, self.computation_listener = None, None
        self.computation_thread = None

        self.progress_bars = None
        self.progress_timer = None
        self._start_code, self._stop_code = "START PROGRESS BAR", "STOP PROGRESS BAR"

        self.read_pipe, self.write_pipe = multiprocessing.Pipe(False)

        super().__init__(main_window, computed_data, *args, **kwargs)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)
        buttons = self.main_window.findChildren(QtWidgets.QAbstractButton)
        for button in buttons:
            if button.objectName() == "calculateButton":
                button.clicked.connect(self.setup_calculation)

        self.progress_bars = self.main_window.findChildren(QtWidgets.QProgressBar)
        for progress_bar in self.progress_bars:
            progress_bar.hide()
            progress_bar.reset()

        self.stop_calculation.connect(self.cancel_calculation)
        self.new_calculation.connect(self.setup_listener)

    def setup_listener(self):

        if self.listener_timer is not None:
            self.listener_timer.stop()

        self.computation_listener = ComputationListener(self.read_pipe, self.computed_data)

        self.listener_timer = QtCore.QTimer(self)
        self.listener_timer.setInterval(100)
        self.listener_timer.timeout.connect(self.computation_listener.listen)

        self.computation_listener.array_received.connect(self.new_array)
        self.computation_listener.energy_received.connect(self.new_energy)
        self.computation_listener.progress_received.connect(self.calculation_progress)

        self.listener_timer.start()

        self.logger.debug("Setup listener thread for computed data.")

    def setup_calculation(self):

        self.logger.debug("Beginning threaded calculation.")
        self.computed_data.clear()
        self.logger.debug("Cleared old data")

        if self.computation_thread is not None:
            self.stop_calculation.emit()
            # self.logger.debug("Previous calculation thread running, terminating it.")
            # self.computation_thread.terminate()
            #
            # self.listener_timer.stop()
            #
            # # pipes can be broken by termination, so reset them
            # self.write_pipe.close()
            # self.read_pipe.close()
            # self.read_pipe, self.write_pipe = multiprocessing.Pipe(False)
            # if self.computation_listener is not None:
            #     self.computation_listener.new_pipe(self.read_pipe)

        self.new_calculation.emit()
        # self.listener_timer.start()
        self.computation_thread = multiprocessing.Process(target=self.calculate)
        self.computation_thread.start()
        self.logger.debug("Started computation thread.")

        self.main_window.graph_component.list_view.clear()
        self.main_window.graph_component.graph_widget.reset()
        self.main_window.graph_component.toggle_widgets_enabled()

    def cancel_calculation(self):
        self.logger.debug("Previous calculation thread running, terminating it.")
        self.computation_thread.terminate()

        self.listener_timer.stop()

        # pipes can be broken by termination, so reset them
        self.write_pipe.close()
        self.read_pipe.close()
        self.read_pipe, self.write_pipe = multiprocessing.Pipe(False)
        if self.computation_listener is not None:
            self.computation_listener.new_pipe(self.read_pipe)

    # This is on separate process.
    def calculate(self):

        self.logger.debug("Beginning Variational Principle calculation on separate thread.")
        self.write_pipe.send(self._start_code)

        # TODO catch MemoryError.
        # TODO handle the allocation of memory by performing a check on the predicted array sizes?
        self.computed_data = vm.compute(self.computed_data, self.write_pipe)

        self.write_pipe.send(self._stop_code)
        self.logger.debug("DONE Variational Principle calculation on separate thread.")

    @QtCore.pyqtSlot(str)
    def calculation_progress(self, message):
        if message == self._start_code:
            self.logger.debug("Setting up progress bar timer.")
            self.progress_timer = QtCore.QTimer(self)
            self.progress_timer.setInterval(100)
            self.progress_timer.timeout.connect(self.increment_progress)
            self.progress_timer.start()
            for progress_bar in self.progress_bars:
                progress_bar.reset()
                progress_bar.show()
        elif message == self._stop_code:
            self.logger.debug("Stopping progress bar timer.")
            self.progress_timer.stop()
            for progress_bar in self.progress_bars:
                progress_bar.reset()
                progress_bar.hide()
        else:
            self.logger.debug("Received variational_principle_gui wasn't a progress variational_principle_gui: '%s'?" % message)

    def increment_progress(self):

        for progress_bar in self.progress_bars:
            max = progress_bar.maximum()
            val = progress_bar.value()
            val += 1
            if val >= max:
                progress_bar.reset()
            else:
                progress_bar.setValue(val)

    @QtCore.pyqtSlot(str, np.ndarray)
    def new_array(self, key, value):

        if key == self.computed_data.r_key:
            self.computed_data.r = value
            self.logger.debug("Received array with key '%s', saving the data under r in computed_data and returning." % key)
            return
        elif key == self.computed_data.v_key:
            self.logger.debug("Received array with key '%s', saving the data under V in computed_data." % key)
            self.computed_data.V = value

        # TODO change this implementation to a signal emit.
        self.logger.debug("New array calculated, under key '%s' updating graphs tab" % key)
        list_view = self.main_window.graph_component.list_view
        list_view.add_item(key, value)
        list_entry = list_view.get_item(key)
        if self.main_window.graph_component.graph_widget.current_list_entry is None:
            self.main_window.graph_component.graph_widget.current_list_entry = list_entry
            self.main_window.graph_component.refresh_button()
        # TODO some check to see if it's a new dimension type to improve performance (marginally)
        # self.main_window.graph_component.populate_graph_combobox()

    @QtCore.pyqtSlot(float)
    def new_energy(self, energy):
        self.energy_received.emit(energy)


class ComputationListener(QtCore.QObject):

    array_received = QtCore.pyqtSignal(str, np.ndarray)
    energy_received = QtCore.pyqtSignal(float)
    progress_received = QtCore.pyqtSignal(str)

    def __init__(self, read_pipe, computed_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self._read_pipe = read_pipe
        self.computed_data = computed_data
        self._is_running = True

    def new_pipe(self, read_pipe):
        self._read_pipe = read_pipe
        self.logger.debug("Got new pipe to read from.")

    @QtCore.pyqtSlot()
    def listen(self):

        is_closed = False
        try:
            self._read_pipe.poll()
        except EOFError as e:
            is_closed = True
        except OSError as e:
            is_closed = True

        if is_closed:
            self.logger.debug("Pipe is closed, can't use it.")
            return

        if not self._read_pipe.poll():
            # there is no new data in the pipe.
            return

        data = self._read_pipe.recv()

        key, value, energy = None, None, None

        if type(data) is tuple:
            key = data[0]
            value = data[1]
            self.logger.debug("Read tuple from pipe, under key '%s'" % key)

            self.array_received.emit(key, value)

        elif type(data) is np.float64 or type(data) is float:
            energy = data
            self.logger.debug("Read float from pipe of value '%s'" % energy)

            self.energy_received.emit(energy)
        elif type(data) is str:
            self.logger.debug("Received status variational_principle_gui from pipe.")
            self.progress_received.emit(data)
        else:
            self.logger.warning("Data read from pipe was neither a tuple or a float!")
            self.logger.warning("Value: %s" % data)
            self.logger.warning("Of type: %s" % type(data))
            return
