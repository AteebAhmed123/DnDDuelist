from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from QuantumMechanics.QuantumStates import QuantumState

class PhaseBias(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Phase Bias"
    description = "Apply phase bias to a superposition card to favor a specific collapse state."
    damage = 0
    
    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/PhaseBias.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.activated_card = False
        self.stateType = QuantumState.COLLAPSED  # Phase Bias is not a quantum card itself
        self.target_card = None  # The card this bias will be applied to
        self.favored_state = None  # The state to favor ('0' or '1' for 2-state, '00', '01', '10', '11' for 4-state)
        self.bias_strength = 0.7  # Probability of favored state (70% vs 30%)

    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def set_target_and_bias(self, target_card, favored_state):
        """Set the target card and the favored state for biasing"""
        self.target_card = target_card
        self.favored_state = favored_state
        
        # Apply the bias to the target card
        if hasattr(target_card, 'apply_phase_bias'):
            target_card.apply_phase_bias(favored_state, self.bias_strength)
    
    def activate_card(self, caster, target):
        """Phase Bias doesn't have a direct effect when played - it's applied to other cards"""
        # This card is played differently - through a targeting system
        return False, None
    
    def can_target_card(self, card):
        """Check if this card can be targeted by Phase Bias"""
        # Can only target cards in superposition state
        return (hasattr(card, 'stateType') and 
                card.stateType == QuantumState.SUPERPOSITION and
                hasattr(card, 'apply_phase_bias')) 