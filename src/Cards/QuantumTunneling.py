from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.QuantumTunnelingEffect import QuantumTunnelingEffect
import numpy as np

class QuantumTunneling(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)
    name = "Quantum Tunneling"
    description = "Next offensive attack has a 70% chance to bypass shields."
    damage = 0
    
    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/tunnel.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.tunneling_effect = QuantumTunnelingEffect(self.screen)
        self.activated_card = False
        
        # Quantum tunneling probability (70% chance to bypass shields)
        self.tunneling_probability = 0.7

    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        """Apply quantum tunneling effect to the caster"""
        # Apply the quantum tunneling effect to the caster
        caster.quantum_tunneling_active = True
        caster.tunneling_probability = self.tunneling_probability
        
        # Show activation indicator if available
        if hasattr(caster, 'quantum_tunneling_indicator') and caster.quantum_tunneling_indicator:
            indicator_position = (caster.position_to_draw[0], caster.position_to_draw[1] - 50)
            caster.quantum_tunneling_indicator.add_tunneling_activated(indicator_position)
        
        # Play the visual effect
        return self.tunneling_effect.animate_spell(caster, target), None
    
    def get_card_type(self):
        """Return the type of this card for deck building"""
        return "utility" 