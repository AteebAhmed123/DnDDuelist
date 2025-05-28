from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2
from qiskit.quantum_info import Statevector
import random
import numpy as np

class Superposition:
    def __init__(self):
        self.backend = AerSimulator()

    @staticmethod
    def apply_superposition_to_qubit(qubit, total_states = 2):
        if (total_states == 2):
            qubit.h(0)
            qubit.measure(0, 0)
        elif (total_states == 4):
            qubit.h([0, 1])
            qubit.measure([0, 1], [0, 1])
    
    @staticmethod
    def apply_superposition_with_bias(qubit, total_states=2, favored_state=None, bias_strength=0.7):
        """Apply superposition with phase bias towards a favored state"""
        if total_states == 2:
            if favored_state is not None and bias_strength != 0.5:
                # Apply rotation to bias towards favored state
                # Calculate the angle for the desired bias
                if favored_state == '0':
                    # Bias towards |0⟩ state
                    theta = 2 * np.arccos(np.sqrt(bias_strength))
                else:
                    # Bias towards |1⟩ state  
                    theta = 2 * np.arccos(np.sqrt(1 - bias_strength))
                qubit.ry(theta, 0)
            else:
                # Standard equal superposition
                qubit.h(0)
            qubit.measure(0, 0)
        elif total_states == 4:
            if favored_state is not None and bias_strength != 0.25:
                # For 4-state system, we need to bias the 2-qubit system
                # This is more complex, so we'll use a simplified approach
                qubit.h([0, 1])
                # Apply phase rotations based on favored state
                if favored_state == '00':
                    qubit.rz(-np.pi/4, 0)
                    qubit.rz(-np.pi/4, 1)
                elif favored_state == '01':
                    qubit.rz(-np.pi/4, 0)
                    qubit.rz(np.pi/4, 1)
                elif favored_state == '10':
                    qubit.rz(np.pi/4, 0)
                    qubit.rz(-np.pi/4, 1)
                elif favored_state == '11':
                    qubit.rz(np.pi/4, 0)
                    qubit.rz(np.pi/4, 1)
            else:
                # Standard equal superposition
                qubit.h([0, 1])
            qubit.measure([0, 1], [0, 1])
    
    @staticmethod
    def collapse_qubit(qubit):
        sim = AerSimulator()
        job = sim.run(qubit, shots=1)        # run 1,024 shots
        result = job.result()
        counts = result.get_counts()
        return max(counts, key=counts.get)
    
    @staticmethod
    def collapse_qubit_with_bias(qubit, favored_state=None, bias_strength=0.7):
        """Collapse a qubit with bias towards a favored state"""
        if favored_state is None:
            # No bias, use standard collapse
            return Superposition.collapse_qubit(qubit)
        
        # Use weighted random selection to simulate bias
        if len(favored_state) == 1:  # 2-state system
            if random.random() < bias_strength:
                return favored_state
            else:
                return '1' if favored_state == '0' else '0'
        else:  # 4-state system
            states = ['00', '01', '10', '11']
            if random.random() < bias_strength:
                return favored_state
            else:
                # Choose randomly from the other states
                other_states = [s for s in states if s != favored_state]
                return random.choice(other_states)

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
    
