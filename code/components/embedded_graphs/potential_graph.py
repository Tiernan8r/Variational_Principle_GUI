import code.components.embedded_graphs.embedded_graph as eg
import variational_principle.variation_method as vm
import variational_principle.potential_handling.potential as pot
import logging


class PotentialGraph(eg.EmbeddedGraph):

    def __init__(self, graph_widget, computed_data):
        super().__init__(graph_widget, computed_data)
        self.plot_number = 0
        self.current_potential_name = None
        self.logger = logging.getLogger(__name__)

    def display(self, potential_name=None):

        if potential_name is None:

            if self.current_potential_name is None:
                self.logger.warning("No potential name provided, aborting potential plotting.")
                return

            potential_name = self.current_potential_name
        self.current_potential_name = potential_name

        self.figure.clear(keep_observers=True)
        self.axes = self.figure.add_subplot()

        r = vm.calculate_r(self.computed_data)
        V = pot.potential(r, potential_name)

        D = self.computed_data.num_dimensions

        title = "Potential for the " + self.computed_data.label + ":"

        xlabel = "$x$"
        ylabel = "$y$"
        zlabel = "$z$"

        if D == 1:
            ylabel = "$V$"
            self._plot_line(*r, V, title, xlabel, ylabel)
        elif D == 2:
            zlabel = "$V$"
            if self.plot_number == 0:
                self._plot_image(*r, V, title, xlabel, ylabel)
            elif self.plot_number == 1:
                self._plot_wireframe(*r, V, title, xlabel, ylabel, zlabel)
            elif self.plot_number == 2:
                self._plot_surface(*r, V, title, xlabel, ylabel, zlabel)
            else:
                self.logger.warning("Attempted to plot 2D plot without a proper plot type given.")
                return
        elif D == 3:
            self._plot_3D_scatter(*r, V, title, xlabel, ylabel, zlabel)
        else:
            self.logger.warning("Attempted to plot potential for greater than 3 dimensions!")
            return

        self.figure_canvas.draw()
