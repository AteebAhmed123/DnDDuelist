from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.Lightning import Lightning
from Spells.Heal import Heal
from Spells.MagicMissile import MagicMissile
from Spells.ThanosSnap import ThanosSnap
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from Spells.ElementalWeather.Rain import Rain
from Spells.ElementalWeather.Earthquake import Earthquake
from Spells.ElementalWeather.Heatwave import HeatWave
from Spells.ElementalWeather.WindTornado import WindTornado
from Spells.ElementalWeather.WeatherSpells import WeatherSpells
from qiskit import QuantumCircuit
from QuantumMechanics.Entanglement import QuantumEntanglement
from Cards.ElementalAttacksCards.EarthSpikeCard import EarthSpikeCard
from Cards.ElementalAttacksCards.WaterGeyserCard import WaterGeyserCard
from Cards.ElementalAttacksCards.BurningHandsCard import BurningHandCard
from Cards.ElementalAttacksCards.WindTornadoCard import WindTornadoCard


class ElementalWeather(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Elemental Weather"
    description = "Afflict the opponent with a random elemental effect."
    damage = 0
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/Weathers/AllWeathers.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.spell = None
        self.activated_card = False
        self.stateType = None
        self.superposition = Superposition()
        self.qubit = QuantumCircuit(2, 2)
        self.collapsedState = None
        
        # Phase bias attributes
        self.has_phase_bias = False
        self.phase_bias_state = None
        self.phase_bias_strength = 0.5


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        if (self.stateType == None):
            Superposition.apply_superposition_to_qubit(self.qubit, total_states=4)
            self.stateType = QuantumState.SUPERPOSITION

        if self.stateType == QuantumState.SUPERPOSITION:
            # Check if phase bias has been applied
            if self.has_phase_bias and self.phase_bias_state:
                # Create a new biased quantum circuit
                biased_qubit = QuantumCircuit(2, 2)
                Superposition.apply_biased_superposition_to_qubit(
                    biased_qubit, 
                    total_states=4, 
                    bias_state=self.phase_bias_state, 
                    bias_strength=self.phase_bias_strength
                )
                self.collapsedState = Superposition.collapse_qubit(biased_qubit)
                print(f"ElementalWeather collapsed with bias toward {self.phase_bias_state}: result = {self.collapsedState}")
            else:
                # Normal collapse without bias
                self.collapsedState = Superposition.collapse_qubit(self.qubit)
                print(f"ElementalWeather collapsed normally: result = {self.collapsedState}")
            
            self.stateType = QuantumState.COLLAPSED
            
            if (self.collapsedState == '00'):
                self.spell = Earthquake(self.screen)
            elif self.collapsedState == '01':
                self.spell = HeatWave(self.screen)
            elif self.collapsedState == '11':
                self.spell = WindTornado(self.screen)
            elif self.collapsedState == '10':
                self.spell = Rain(self.screen)
        
        if (self.collapsedState != None):
            print("Returning spell", self.spell)
            return self.spell

    def interpret_afflication_state(self, state):
        if state == '00':
            return EarthSpikeCard(self.screen)
        elif state == '01':
            return WaterGeyserCard(self.screen)
        elif state == '11':
            return BurningHandCard(self.screen)
        elif state == '10':
            return WindTornadoCard(self.screen)