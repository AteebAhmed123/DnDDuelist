from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2
from qiskit.quantum_info import Statevector
from QuantumMechanics.QuantumStates import QuantumState

class QuantumEntanglement:
    """
    Manages quantum entanglement between ElementalAfflication and ElementalWeather
    using Bell states to ensure correlated outcomes.
    """
    
    def __init__(self, screen, weather_manager, game_manager=None):
        self.screen = screen
        self.weather_manager = weather_manager
        self.game_manager = game_manager
        
        # Track the collapse state of both cards
        self.afflication_collapsed = False
        self.weather_collapsed = False
        
        # Store the collapsed states
        self.afflication_state = None
        self.weather_state = None
        
        # Create the entangled quantum circuit
        self.entangled_circuit = QuantumCircuit(4, 4)
        self.setup_entanglement()
        
    def setup_entanglement(self):
        """Create the entangled quantum circuit using Bell state"""
        # Reset the circuit
        self.entangled_circuit = QuantumCircuit(4, 4)
        
        # First pair (qubits 0,1) for ElementalAfflication
        # Second pair (qubits 2,3) for ElementalWeather
        
        # Create superposition on first qubit of each pair
        self.entangled_circuit.h([0, 2])
        
        # Create entanglement within each pair
        self.entangled_circuit.cx(0, 1)
        self.entangled_circuit.cx(2, 3)
        
        # Create entanglement between pairs
        self.entangled_circuit.cx(0, 2)
        
        # Add measurements
        self.entangled_circuit.measure([0, 1, 2, 3], [0, 1, 2, 3])
        
    @staticmethod
    def simulate_entanglement():
        entangled_circuit = QuantumCircuit(4, 4)
        
        # First pair (qubits 0,1) for ElementalAfflication
        # Second pair (qubits 2,3) for ElementalWeather
        
        # Create superposition on first qubit of each pair
        entangled_circuit.h([0, 2])
        
        # Create entanglement within each pair
        entangled_circuit.cx(0, 1)
        entangled_circuit.cx(2, 3)
        
        # Create entanglement between pairs
        entangled_circuit.cx(0, 2)
        
        # Add measurements
        entangled_circuit.measure([0, 1, 2, 3], [0, 1, 2, 3])
        sim = AerSimulator()
        job = sim.run(entangled_circuit, shots=1)        # run 1,024 shots
        result = job.result()
        counts = result.get_counts()
        outcome = max(counts, key=counts.get)
        afflication_state = outcome[0:2]  # First two bits
        weather_state = outcome[2:4]      # Last two bits
        return afflication_state, weather_state


    def collapse_states(self):
        """Collapse both states at once and return the results"""
        # Use qiskit to simulate the measurement
        sim = AerSimulator()
        job = sim.run(self.entangled_circuit, shots=1)        # run 1,024 shots
        result = job.result()
        counts = result.get_counts()
        return max(counts, key=counts.get)
        
        # Parse the 4-bit outcome into two 2-bit states
        afflication_state = outcome[0:2]  # First two bits
        weather_state = outcome[2:4]      # Last two bits
        
        # Update internal state
        self.afflication_state = afflication_state
        self.weather_state = weather_state
        self.afflication_collapsed = True
        self.weather_collapsed = True
        
        return afflication_state, weather_state
    
    def handle_afflication_collapse(self, state, caster):
        """Handle the case where ElementalAfflication is measured first"""
        self.afflication_collapsed = True
        self.afflication_state = state
        
        # Determine the corresponding weather state based on the mapping
        if state == '00':  # EarthSpike
            weather_state = '00'  # Earthquake
        elif state == '01':  # WaterGeyser
            weather_state = '10'  # Rain
        elif state == '11':  # Fireball
            weather_state = '01'  # HeatWave
        elif state == '10':  # WindSlash
            weather_state = '11'  # WindTornado
        
        self.weather_state = weather_state
        self.weather_collapsed = True
        
        # Activate the weather effect
        self._activate_weather(weather_state)
        
        return weather_state
    
    def handle_weather_collapse(self, state):
        """Handle the case where ElementalWeather is measured first"""
        self.weather_collapsed = True
        self.weather_state = state
        
        # Determine the corresponding afflication state based on the mapping
        if state == '00':  # Earthquake
            afflication_state = '00'  # EarthSpike
        elif state == '10':  # Rain
            afflication_state = '01'  # WaterGeyser
        elif state == '01':  # HeatWave
            afflication_state = '11'  # Fireball
        elif state == '11':  # WindTornado
            afflication_state = '10'  # WindSlash
        
        self.afflication_state = afflication_state
        self.afflication_collapsed = True
        
        return afflication_state
    
    def _activate_weather(self, weather_state):
        """Activate the appropriate weather effect"""
        from Spells.ElementalWeather.Rain import Rain
        from Spells.ElementalWeather.WindTornado import WindTornado
        from Spells.ElementalWeather.Heatwave import HeatWave
        from Spells.ElementalWeather.Earthquake import Earthquake
        
        weather_spell = None
        weather_duration = 3  # Duration in turns
        
        if weather_state == '00':  # Earthquake
            weather_spell = Earthquake(self.screen)
        elif weather_state == '10':  # Rain
            weather_spell = Rain(self.screen)
        elif weather_state == '01':  # HeatWave
            weather_spell = HeatWave(self.screen)
        elif weather_state == '11':  # WindTornado
            weather_spell = WindTornado(self.screen)
        
        if weather_spell and self.weather_manager:
            self.weather_manager.set_active_weather(weather_spell, weather_duration)
    
    def reset(self):
        """Reset the entanglement state for a new round"""
        self.afflication_collapsed = False
        self.weather_collapsed = False
        self.afflication_state = None
        self.weather_state = None
        self.setup_entanglement()