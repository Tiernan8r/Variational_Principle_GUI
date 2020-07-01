from code.components.abstract_component import AbstractComponent
import logging


class EnergyComponent(AbstractComponent):

    def __init__(self, main_window, computed_data, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        super().__init__(main_window, computed_data, *args, **kwargs)

    def setup_signals(self):
        self.logger = logging.getLogger(__name__)
        pass