from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2
from qiskit.quantum_info import Statevector
import random

class Superposition:
    def __init__(self):
        self.backend = AerSimulator()
        # Circuit always has 1 qubit + 1 classical bit
        self.qc = QuantumCircuit(1, 1)

    def super_position_qubit(self, qubit):
        qubit.h(0)
        qubit.measure(0, 0)
        return qubit
    
    def collapse_qubit(self, qubit):
        sim = AerSimulator()
        job = sim.run(qubit, shots=1)        # run 1,024 shots
        result = job.result()
        counts = result.get_counts()
        collapsedState = {'0': 0, '1': 0}
        if '0' in counts:
            collapsedState['0'] = counts['0']
        if '1' in counts:
            collapsedState['1'] = counts['1']
        
        if collapsedState['0'] > collapsedState['1']:
            return 0
        else:
            return 1

 
    # def get_statevector(self):
    #     """Return the exact statevector of the current circuit."""
    #     # Strip out the measurement when peeking at amplitudes
    #     circ = self.qc.remove_final_measurements(inplace=False)
    #     return Statevector.from_instruction(circ)

    # def apply_hadamard(self):
    #     """Apply H to create |+> and return its statevector."""
    #     self.qc.h(0)
    #     return self.get_statevector()
    
    # def collapse(self):
    #     """
    #     Do a single-shot measurement:
    #       1. Copy the circuit, append a measurement.
    #       2. Run 1 shot on AerSimulator.
    #       3. Rebuild self.qc in the post-measurement basis.
    #     Returns 0 or 1.
    #     """
    #     circ = self.qc.copy()
    #     circ.measure_all()
    #     job = self.backend.run(circ, shots=1)
    #     counts = job.result().get_counts()
    #     # In a single shot there's only one key in counts
    #     measured = int(next(iter(counts)))

    #     # Reinitialize the circuit in the collapsed state
    #     self.qc = QuantumCircuit(1, 1)
    #     if measured == 1:
    #         self.qc.x(0)
    #     # (Optional) map qubit → classical for consistency
    #     self.qc.measure(0, 0)

    #     return measured
    
    # def measure_probs(self, shots: int = 1024):
    #     """
    #     Perform repeated measurements to estimate probabilities.
    #     Returns a dict {'0': p0, '1': p1}.
    #     """
    #     circ = self.qc.copy()
    #     circ.measure(0, 0)
    #     job = self.backend.run(circ, shots=shots)
    #     counts = job.result().get_counts()
    #     total = sum(counts.values())
    #     return {bit: count/total for bit, count in counts.items()}
    
