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
from qiskit import QuantumCircuit

class ElementalAfflication(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Elemental Afflication"
    description = "Afflict the opponent with a random elemental effect."
    damage = 0
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/ElementalAttacks/ElementalAffliction.png"
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
            if (self.collapsedState == '00'):
                self.spell = EarthSpike(self.screen)
            elif self.collapsedState == '01':
                self.spell = WaterGeyser(self.screen)
            elif self.collapsedState == '11':
                self.spell = Fireball(self.screen)
            elif self.collapsedState == '10':
                self.spell = WindSlash(self.screen)
        
        if (self.collapsedState != None):
            return self.spell.animate_spell(caster, target)