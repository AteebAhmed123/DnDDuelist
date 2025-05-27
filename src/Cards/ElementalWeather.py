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

class ElementalWeather(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Elemental Afflication"
    description = "Afflict the opponent with a random elemental effect."
    damage = 0
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/Weathers/AllWeathers.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.spell = None
        self.activated_card = False
        self.stateType = QuantumState.SUPERPOSITION
        self.superposition = Superposition()
        self.qubit = QuantumCircuit(2, 2)
        Superposition.apply_superposition_to_qubit(self.qubit, total_states=4)
        self.collapsedState = None


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        if self.stateType == QuantumState.SUPERPOSITION:
            self.collapsedState = Superposition.collapse_qubit(self.qubit)
            self.stateType = QuantumState.COLLAPSED
            print(self.collapsedState)
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