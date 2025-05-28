from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.Lightning import Lightning
from Spells.Heal import Heal
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from qiskit import QuantumCircuit
from Spells.ElementalWeather.Heatwave import HeatWave

class HeatwaveWeather(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Burning Hands"
    description = "Burns the opponent with fire"
    damage = 0
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/Weathers/FireWeather.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.activated_card = False
        self.stateType = QuantumState.COLLAPSED
        self.spell = HeatWave(self.screen)
        self.collapsedState = None


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        self.activated_card = True
        return self.spell, None