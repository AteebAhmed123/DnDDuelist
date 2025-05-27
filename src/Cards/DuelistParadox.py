from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.Lightning import Lightning
from Spells.Heal import Heal
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
from qiskit import QuantumCircuit

class DuelistParadox(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Duelist's Paradox"
    description = "Strikes the opponent with lightning, dealing 10 damage."
    damage = 10
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/DuelistParadox.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.spell = Lightning(self.screen)
        self.heal = Heal(self.screen)
        self.activated_card = False
        self.stateType = QuantumState.SUPERPOSITION
        self.qubit = QuantumCircuit(1, 1)
        Superposition.apply_superposition_to_qubit(self.qubit, total_states=2)
        self.collapsedState = None


    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        if self.stateType == QuantumState.SUPERPOSITION:
            self.collapsedState = Superposition.collapse_qubit(self.qubit)
            self.stateType = QuantumState.COLLAPSED
        
        if (self.collapsedState != None):
            if (self.collapsedState == '0'):
                return self.spell.animate_spell(caster, target)
            elif (self.collapsedState == '1'):
                return self.heal.animate_spell(caster, target)                
    