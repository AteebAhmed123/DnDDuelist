from qiskit import QuantumCircuit, Aer, execute
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from WeatherManager import WeatherManager, WeatherType
from Spells.ElementalWeather.Rain import Rain
from Spells.ElementalWeather.WindTornado import WindTornado
from Spells.ElementalWeather.Heatwave import HeatWave
from Spells.ElementalWeather.Earthquake import Earthquake
from Cards.ElementalAfflication import ElementalAfflication

class QuantumEntanglement:
    """
    Manages quantum entanglement between ElementalAfflication and ElementalWeather
    using Bell states to ensure correlated outcomes.
    """
    
    def __init__(self, screen, weather_manager, game_manager=None):
        self.screen = screen
        self.weather_manager = weather_manager
        self.game_manager = game_manager
        self.entangled_circuit = None
        self.setup_entanglement()
        
        # Track the collapse state of both cards
        self.afflication_collapsed = False
        self.weather_collapsed = False
        
        # Store the collapsed states
        self.afflication_state = None
        self.weather_state = None
        
    def setup_entanglement(self):
        """Create the entangled quantum circuit using Bell state"""
        self.entangled_circuit = QuantumCircuit(4, 4)
        
        # Create entanglement between qubits 0-1 and 2-3
        # First pair for ElementalAfflication, Second pair for ElementalWeather
        self.entangled_circuit.h([0, 2])  # Apply Hadamard to first qubit of each pair
        self.entangled_circuit.cx(0, 1)   # Apply CNOT to entangle first pair
        self.entangled_circuit.cx(2, 3)   # Apply CNOT to entangle second pair
        
        # Entangle the two pairs
        self.entangled_circuit.cx(0, 2)   # Create entanglement between the pairs
        
        # Measure all qubits
        self.entangled_circuit.measure([0, 1, 2, 3], [0, 1, 2, 3])
    
    def collapse_states(self):
        """
        Collapse the entangled state and return the results
        """
        sim = Aer.get_backend('aer_simulator')
        job = execute(self.entangled_circuit, sim, shots=1)
        result = job.result()
        counts = result.get_counts()
        outcome = list(counts.keys())[0]  # Get the single outcome
        
        # Parse the 4-bit outcome
        afflication_state = outcome[:2]
        weather_state = outcome[2:]
        
        # Store the states
        self.afflication_state = afflication_state
        self.weather_state = weather_state
        
        return afflication_state, weather_state
    
    def handle_afflication_collapse(self, afflication_state, caster):
        """
        When ElementalAfflication collapses, determine and set the corresponding
        ElementalWeather state
        """
        self.afflication_collapsed = True
        self.afflication_state = afflication_state
        
        # If already have a predetermined weather state from previous entanglement
        if self.weather_collapsed:
            return self.weather_state
        
        # Map ElementalAfflication states to their corresponding ElementalWeather states
        if afflication_state == '00':  # EarthSpike
            weather_state = '00'  # Earthquake
        elif afflication_state == '01':  # WaterGeyser
            weather_state = '10'  # Rain
        elif afflication_state == '11':  # Fireball
            weather_state = '01'  # HeatWave
        elif afflication_state == '10':  # WindSlash
            weather_state = '11'  # WindTornado
        
        self.weather_state = weather_state
        self.weather_collapsed = True
        
        # Create and activate the corresponding weather spell
        self._activate_weather_spell(weather_state)
        
        return weather_state
    
    def handle_weather_collapse(self, weather_state):
        """
        When ElementalWeather collapses, determine and set the corresponding
        ElementalAfflication state
        """
        self.weather_collapsed = True
        self.weather_state = weather_state
        
        # If already have a predetermined afflication state from previous entanglement
        if self.afflication_collapsed:
            return self.afflication_state
        
        # Map ElementalWeather states to their corresponding ElementalAfflication states
        if weather_state == '00':  # Earthquake
            afflication_state = '00'  # EarthSpike
        elif weather_state == '10':  # Rain
            afflication_state = '01'  # WaterGeyser
        elif weather_state == '01':  # HeatWave
            afflication_state = '11'  # Fireball
        elif weather_state == '11':  # WindTornado
            afflication_state = '10'  # WindSlash
        
        self.afflication_state = afflication_state
        self.afflication_collapsed = True
        
        # Update the ElementalAfflication card state in both players' hands
        if self.game_manager:
            self._update_player_afflication_cards(afflication_state)
        
        return afflication_state
    
    def _activate_weather_spell(self, weather_state):
        """Create and activate the appropriate weather spell based on state"""
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
        
        if weather_spell:
            self.weather_manager.set_active_weather(weather_spell, weather_duration)
    
    def _update_player_afflication_cards(self, afflication_state):
        """Update the ElementalAfflication cards in players' hands"""
        # This method would be called when weather collapses first
        # It would update all ElementalAfflication cards to be in the corresponding state
        
        if self.game_manager:
            # Update Wizard's ElementalAfflication card
            for card in self.game_manager.wizard.cards:
                if isinstance(card, ElementalAfflication):
                    card.force_collapse_state(afflication_state)
                    
            # Update Mage's ElementalAfflication card
            for card in self.game_manager.mage.cards:
                if isinstance(card, ElementalAfflication):
                    card.force_collapse_state(afflication_state)
    
    def reset_entanglement(self):
        """Reset the entanglement state"""
        self.afflication_collapsed = False
        self.weather_collapsed = False
        self.afflication_state = None
        self.weather_state = None
        self.setup_entanglement()