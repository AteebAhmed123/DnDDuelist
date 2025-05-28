from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.MagicMissile import MagicMissile
from Spells.MagicMissileV2 import MagicMissileV2
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from qiskit import QuantumCircuit
from Spells.ThanosSnap import ThanosSnap

class ThanosSnapCard(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Thanos Snap"
    description = "Half the number of cards in your deck or half the number of cards in your opponent's deck."
    damage = 10
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/ThanosSnap.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.qubit = QuantumCircuit(1, 1)
        Superposition.apply_superposition_to_qubit(self.qubit, total_states=2)
        self.stateType = QuantumState.SUPERPOSITION
        self.collapsedState = None
        self.thanosSnap = ThanosSnap(self.screen)
        self.activated_card = False
        
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
                return self.thanosSnap.animate_spell(caster, caster), None
            elif (self.collapsedState == '1'):
                return self.thanosSnap.animate_spell(caster, target), None

    def get_possible_states(self):
        """Return the possible states for this card for UI selection"""
        return {
            '0': "Snap Your Own Deck (halve your cards)",
            '1': "Snap Enemy Deck (halve enemy cards)"
        }

    def apply_affect(self, caster, target):
        return self.spell.animate_spell(caster, target)
        
    