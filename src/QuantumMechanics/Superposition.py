from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2
from qiskit.quantum_info import Statevector
import random
import math

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
    def apply_biased_superposition_to_qubit(qubit, total_states=2, bias_state='0', bias_strength=0.7):
        """
        Apply superposition with bias toward a specific state.
        
        Args:
            qubit: The quantum circuit
            total_states: Number of possible states (2 or 4)
            bias_state: The state to bias toward ('0', '1' for 2 states; '00', '01', '10', '11' for 4 states)
            bias_strength: Probability of collapsing to the biased state (0.5 = no bias, 1.0 = always bias)
        """
        if total_states == 2:
            # For 2-state system, use rotation gates to create bias
            if bias_state == '0':
                # Bias toward |0⟩ - rotate less than π/2
                angle = math.acos(math.sqrt(bias_strength))
                qubit.ry(2 * angle, 0)
            else:  # bias_state == '1'
                # Bias toward |1⟩ - rotate more than π/2
                angle = math.acos(math.sqrt(1 - bias_strength))
                qubit.ry(2 * angle, 0)
            qubit.measure(0, 0)
        elif total_states == 4:
            # For 4-state system, create biased superposition
            # This is more complex, so we'll use a simplified approach
            # Apply Hadamard gates first
            qubit.h([0, 1])
            
            # Apply phase rotations based on bias
            if bias_state == '00':
                # No additional rotation needed for |00⟩ bias
                pass
            elif bias_state == '01':
                qubit.rz(math.pi * (1 - bias_strength), 1)
            elif bias_state == '10':
                qubit.rz(math.pi * (1 - bias_strength), 0)
            elif bias_state == '11':
                qubit.rz(math.pi * (1 - bias_strength), 0)
                qubit.rz(math.pi * (1 - bias_strength), 1)
            
            qubit.measure([0, 1], [0, 1])
    
    @staticmethod
    def collapse_qubit(qubit):
        sim = AerSimulator()
        job = sim.run(qubit, shots=1)        # run 1,024 shots
        result = job.result()
        counts = result.get_counts()
        return max(counts, key=counts.get)

    @staticmethod
    def collapse_biased_qubit(qubit, bias_state='0', bias_strength=0.7):
        """
        Collapse a qubit with bias toward a specific state.
        This is a simplified version that uses weighted random selection.
        """
        sim = AerSimulator()
        job = sim.run(qubit, shots=100)  # Use more shots for better probability estimation
        result = job.result()
        counts = result.get_counts()
        
        # If we have the bias state in results, increase its weight
        if bias_state in counts:
            # Artificially increase the count for the biased state
            bias_multiplier = bias_strength / (1 - bias_strength) if bias_strength < 1.0 else 10
            counts[bias_state] = int(counts[bias_state] * bias_multiplier)
        
        # Select based on weighted counts
        total_counts = sum(counts.values())
        rand_val = random.randint(1, total_counts)
        
        cumulative = 0
        for state, count in counts.items():
            cumulative += count
            if rand_val <= cumulative:
                return state
        
        # Fallback to original behavior
        return max(counts, key=counts.get)

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
    
