from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.Lightning import Lightning
from Spells.Heal import Heal
from Spells.MagicMissile import MagicMissile
from Spells.ThanosSnap import ThanosSnap
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from Spells.ElementalAttacks.Fireball import Fireball
from Spells.ElementalAttacks.WindSlash import WindSlash
from Spells.ElementalAttacks.WaterGeyser import WaterGeyser
from Spells.ElementalAttacks.EarthSpike import EarthSpike
from Spells.ElementalWeather.Rain import Rain
from Spells.ElementalWeather.Earthquake import Earthquake
from Spells.ElementalWeather.Heatwave import HeatWave
from Spells.ElementalWeather.WindTornado import WindTornado
from qiskit import QuantumCircuit
from QuantumMechanics.Entanglement import QuantumEntanglement
from Cards.WeatherCards.Nature import Nature
from Cards.WeatherCards.RainWeather import RainWeather
from Cards.WeatherCards.HeatwaveWeather import HeatwaveWeather
from Cards.WeatherCards.WindyWeather import WindyWeather

class WaterGeyserCard(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Water Geyser"
    description = "Erupts from below the target, lifting them up"
    damage = 0
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/ElementalAttacks/Driphex.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.spell = WaterGeyser(self.screen)
        self.activated_card = False
        self.stateType = QuantumState.ENTANGLED
        
        self.collapsedState = None


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        return self.spell.animate_spell(caster, target), None
        