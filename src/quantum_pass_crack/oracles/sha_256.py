from qiskit.aqua.components.oracles.oracle import Oracle


class SHA256Oracle(Oracle):

    def __init__(self, *args, **kwargs):
        super(SHA256Oracle).__init__(*args, **kwargs)

    def construct_circuit(self):
        """Construct the oracle circuit.

        Returns:
            A quantum circuit for the oracle.
        """
        raise NotImplementedError()
