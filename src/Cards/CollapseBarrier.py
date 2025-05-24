from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.Barrier import Barrier
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from qiskit import QuantumCircuit
from Spells.BacklashSurge import BacklashSurge

class CollapseBarrier(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Collapse Barrier"
    description = "Create a barrier that protects the caster from the next spell or take 3x Damage on the next spell."
    damage = 0
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/CollapseBarrier.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.barrier = Barrier(self.screen)
        self.vulnerable = BacklashSurge(self.screen)
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
                return self.barrier.animate_spell(caster, target)
            elif (self.collapsedState == 1):
                return self.vulnerable.animate_spell(caster, target)                
    