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
        
        # Phase bias attributes
        self.has_phase_bias = False
        self.phase_bias_state = None
        self.phase_bias_strength = 0.5


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        if self.stateType == QuantumState.SUPERPOSITION:
            # Check if phase bias has been applied
            if self.has_phase_bias and self.phase_bias_state:
                # Create a new biased quantum circuit
                biased_qubit = QuantumCircuit(1, 1)
                Superposition.apply_biased_superposition_to_qubit(
                    biased_qubit, 
                    total_states=2, 
                    bias_state=self.phase_bias_state, 
                    bias_strength=self.phase_bias_strength
                )
                self.collapsedState = Superposition.collapse_qubit(biased_qubit)
                print(f"CollapseBarrier collapsed with bias toward {self.phase_bias_state}: result = {self.collapsedState}")
            else:
                # Normal collapse without bias
                self.collapsedState = Superposition.collapse_qubit(self.qubit)
                print(f"CollapseBarrier collapsed normally: result = {self.collapsedState}")
            
            self.stateType = QuantumState.COLLAPSED
        
        if (self.collapsedState != None):
            if (self.collapsedState == '0'):
                return self.barrier.animate_spell(caster, target), None
            elif (self.collapsedState == '1'):
                return self.vulnerable.animate_spell(caster, target), None                
    