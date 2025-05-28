import numpy as np
import random
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.primitives import BackendSamplerV2
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import Statevector

class QuantumTunneling:
    """
    Quantum Tunneling implementation for DnD Duelist.
    
    In quantum mechanics, tunneling allows particles to pass through barriers
    that they classically shouldn't be able to overcome. In our game, this
    translates to attacks having a probability of bypassing shields.
    """
    
    @staticmethod
    def calculate_tunneling_probability(caster, base_probability=0.7):
        """
        Calculate the probability of quantum tunneling occurring.
        
        Args:
            caster: The character attempting to tunnel
            base_probability: Base tunneling probability (default 70%)
            
        Returns:
            float: Probability of successful tunneling (0.0 to 1.0)
        """
        if not hasattr(caster, 'quantum_tunneling_active') or not caster.quantum_tunneling_active:
            return 0.0
        
        # Use the caster's tunneling probability if available
        if hasattr(caster, 'tunneling_probability'):
            return caster.tunneling_probability
        
        return base_probability
    
    @staticmethod
    def attempt_tunneling(caster, target):
        """
        Attempt quantum tunneling through a shield.
        
        Args:
            caster: The attacking character
            target: The defending character
            
        Returns:
            tuple: (tunneling_occurred, should_consume_effect)
                - tunneling_occurred: bool, whether tunneling happened
                - should_consume_effect: bool, whether to consume the tunneling effect
        """
        # Check if target has a shield
        if not hasattr(target, 'shield') or not target.shield:
            # No shield to tunnel through, effect is wasted
            return False, True
        
        # Check if caster has quantum tunneling active
        tunneling_prob = QuantumTunneling.calculate_tunneling_probability(caster)
        if tunneling_prob <= 0.0:
            return False, False
        
        # Use quantum circuit to simulate tunneling
        tunneling_occurred = QuantumTunneling._quantum_tunneling_simulation(tunneling_prob)
        
        # Always consume the effect after attempting tunneling
        return tunneling_occurred, True
    
    @staticmethod
    def _quantum_tunneling_simulation(probability):
        """
        Simulate quantum tunneling using a quantum circuit.
        
        Args:
            probability: The tunneling probability
            
        Returns:
            bool: Whether tunneling occurred
        """
        # Create a quantum circuit with 1 qubit
        qc = QuantumCircuit(1, 1)
        
        # Apply rotation to create the desired probability distribution
        # For probability p, we need angle θ such that sin²(θ/2) = p
        # Therefore θ = 2 * arcsin(√p)
        angle = 2 * np.arcsin(np.sqrt(probability))
        qc.ry(angle, 0)
        
        # Measure the qubit
        qc.measure(0, 0)
        
        # Execute the circuit
        sim = AerSimulator()
        job = sim.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        
        # Get the most frequent result (should be only one result with shots=1)
        measurement_result = max(counts, key=counts.get)
        
        # Return True if we measured |1⟩ (tunneling occurred)
        return measurement_result == '1'
    
    @staticmethod
    def apply_tunneling_damage(caster, target, damage):
        """
        Apply damage with quantum tunneling consideration.
        
        Args:
            caster: The attacking character
            target: The defending character  
            damage: The damage amount to apply
            
        Returns:
            bool: Whether damage was applied (for feedback)
        """
        tunneling_occurred, should_consume = QuantumTunneling.attempt_tunneling(caster, target)
        
        # Show visual indicators if quantum tunneling indicator is available
        if (hasattr(caster, 'quantum_tunneling_indicator') and 
            caster.quantum_tunneling_indicator and 
            hasattr(target, 'shield') and target.shield and
            hasattr(caster, 'quantum_tunneling_active') and 
            caster.quantum_tunneling_active):
            
            indicator_position = (target.position_to_draw[0], target.position_to_draw[1] - 80)
            
            if tunneling_occurred:
                caster.quantum_tunneling_indicator.add_tunneling_success(indicator_position)
            else:
                caster.quantum_tunneling_indicator.add_tunneling_failure(indicator_position)
        
        if tunneling_occurred:
            # Tunneling successful - damage bypasses shield
            target.health.reduce_health(damage * target.self_damage_multiplier)
            # Shield remains intact (tunneling doesn't destroy the barrier)
            damage_applied = True
        else:
            # Normal damage application (respects shield)
            if not target.shield:
                target.health.reduce_health(damage * target.self_damage_multiplier)
                damage_applied = True
            else:
                damage_applied = False
            
            # Remove shield after attack (normal behavior)
            target.shield = False
        
        # Reset vulnerability multiplier
        target.self_damage_multiplier = 1.0
        
        # Consume tunneling effect if needed
        if should_consume and hasattr(caster, 'quantum_tunneling_active'):
            caster.quantum_tunneling_active = False
            caster.tunneling_probability = 0.0
        
        return damage_applied 