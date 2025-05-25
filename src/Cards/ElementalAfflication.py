from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.Lightning import Lightning
from Spells.Heal import Heal
from Spells.MagicMissile import MagicMissile
from Spells.ThanosSnap import ThanosSnap
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
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
        self.spell = Lightning(self.screen)
        self.heal = Heal(self.screen)
        self.spell3 = MagicMissile(self.screen)
        self.spell4 = ThanosSnap(self.screen)
        self.activated_card = False
        self.stateType = QuantumState.SUPERPOSITION
        self.superposition = Superposition()
        self.qubit = self.superposition.super_position_qubit(QuantumCircuit(1, 1))
        self.collapsedState = None


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        if self.stateType == QuantumState.SUPERPOSITION:
            self.collapsedState = self.superposition.collapse_qubit(self.qubit)
            self.stateType = QuantumState.COLLAPSED
        
        if (self.collapsedState != None):
            if (self.collapsedState == 0):
                return self.spell.animate_spell(caster, target)
            elif (self.collapsedState == 1):
                return self.heal.animate_spell(caster, target)                
    