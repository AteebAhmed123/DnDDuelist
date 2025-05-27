from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.MagicMissile import MagicMissile
from Spells.MagicMissileV2 import MagicMissileV2
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from qiskit import QuantumCircuit
from Spells.ThanosSnap import ThanosSnap

class MagicMissive(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Magic Missive"
    description = "Launches a magic missile at the opponent, dealing 6 damage to them or 3 to you."
    damage = 10
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/MagicMCard.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.qubit = QuantumCircuit(1, 1)
        Superposition.apply_superposition_to_qubit(self.qubit, total_states=2)
        self.stateType = QuantumState.SUPERPOSITION
        self.collapsedState = None
        self.magicMissile = MagicMissile(self.screen)
        self.self_harm_magic_missile = MagicMissileV2(self.screen)
        self.activated_card = False

    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        if self.stateType == QuantumState.SUPERPOSITION:
            self.collapsedState = Superposition.collapse_qubit(self.qubit)
            self.stateType = QuantumState.COLLAPSED
        
        if (self.collapsedState != None):
            if (self.collapsedState == '0'):
                return self.magicMissile.animate_spell(caster, target)
            elif (self.collapsedState == '1'):
                return self.self_harm_magic_missile.animate_spell(caster, target)   

    def apply_affect(self, caster, target):
        return self.spell.animate_spell(caster, target)
        
    