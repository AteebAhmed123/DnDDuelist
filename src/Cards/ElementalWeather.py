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
    name = "Elemental Afflication"
    description = "Afflict the opponent with a random elemental effect."
    damage = 0
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/Weathers/AllWeathers.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.spell = None
        self.activated_card = False
        self.stateType = QuantumState.ENTANGLED
        self.collapsedState = None


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        if self.stateType == QuantumState.ENTANGLED:
            self.afflicationState, self.collapsedState = QuantumEntanglement.simulate_entanglement()
            
            self.stateType = QuantumState.COLLAPSED
            if self.collapsedState == '00':
                self.spell = Earthquake(self.screen)
            elif self.collapsedState == '01':
                self.spell = Rain(self.screen)
            elif self.collapsedState == '11':
                self.spell = HeatWave(self.screen)
            elif self.collapsedState == '10':
                self.spell = WindTornado(self.screen)

        if (self.collapsedState != None):
            return self.spell, self.interpret_afflication_state(self.afflicationState)
        

    def interpret_afflication_state(self, state):
        if state == '00':
            return EarthSpikeCard(self.screen)
        elif state == '01':
            return WaterGeyserCard(self.screen)
        elif state == '11':
            return BurningHandCard(self.screen)
        elif state == '10':
            return WindTornadoCard(self.screen)