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
        self.qubit = QuantumCircuit(1, 1)
        Superposition.apply_superposition_to_qubit(self.qubit, total_states=2)
        self.collapsedState = None
        
        # Phase bias properties
        self.has_phase_bias = False
        self.favored_state = None
        self.bias_strength = 0.5  # Default no bias

    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def apply_phase_bias(self, favored_state, bias_strength):
        """Apply phase bias to this card"""
        self.has_phase_bias = True
        self.favored_state = favored_state
        self.bias_strength = bias_strength
        
        # Recreate the quantum circuit with bias
        self.qubit = QuantumCircuit(1, 1)
        if self.has_phase_bias:
            Superposition.apply_superposition_with_bias(
                self.qubit, 
                total_states=2, 
                favored_state=self.favored_state, 
                bias_strength=self.bias_strength
            )
        else:
            Superposition.apply_superposition_to_qubit(self.qubit, total_states=2)
    
    def activate_card(self, caster, target):
        if self.stateType == QuantumState.SUPERPOSITION:
            if self.has_phase_bias:
                self.collapsedState = Superposition.collapse_qubit_with_bias(
                    self.qubit, 
                    self.favored_state, 
                    self.bias_strength
                )
            else:
                self.collapsedState = Superposition.collapse_qubit(self.qubit)
            self.stateType = QuantumState.COLLAPSED
        
        if (self.collapsedState != None):
            if (self.collapsedState == '0'):
                return self.barrier.animate_spell(caster, target), None
            elif (self.collapsedState == '1'):
                return self.vulnerable.animate_spell(caster, target), None
    
    def get_possible_states(self):
        """Return the possible states for this card for UI selection"""
        return {
            '0': "Barrier Shield (blocks next attack)",
            '1': "Vulnerability (3x damage on next attack)"
        }
    