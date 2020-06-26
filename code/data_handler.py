class ComputedData(object):

    def __init__(self, r, V, all_psi, all_E, num_dimensions, num_samples):
        self._r = r
        self._V = V
        self._all_psi = all_psi
        self._all_E = all_E

        self._D = num_dimensions
        self._N = num_samples

        self._array_dict = {}
        self._energy_dict = {}

        self._array_dict["position"] = r
        self._array_dict["potential"] = V

        if len(all_psi) != len(all_E):
            # TODO pretty
            raise ValueError("There has to be the same amount of energies as eigenstates.")

        for i in range(len(all_psi)):
            key = "state_{}".format(i)

            self._array_dict[key] = all_psi[i]
            self._energy_dict[key] = all_E[i]

    def get_energy(self, key):
        return self._energy_dict.get(key, None)

    def get_array(self, key):
        return self._array_dict.get(key, None)

    @property
    def num_dimensions(self):
        return self._D

    @property
    def num_samples(self):
        return self._N
