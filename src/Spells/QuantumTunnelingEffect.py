import pygame
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
import math
import os
class QuantumTunnelingEffect(SpellBase):
    """Quantum tunneling effect that creates a shimmering aura around the caster"""
    
    # Define animation frames for the tunneling effect
    animation_frames = [
        (0, 0, 100, 100),    # Frame 1 - placeholder coordinates
        (100, 0, 100, 100),  # Frame 2
        (200, 0, 100, 100),  # Frame 3
        (300, 0, 100, 100),  # Frame 4
        (400, 0, 100, 100),  # Frame 5
        (500, 0, 100, 100),  # Frame 6
        (600, 0, 100, 100),  # Frame 7
        (700, 0, 100, 100),  # Frame 8
    ]
    
    def __init__(self, screen):
        """Initialize the quantum tunneling effect"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/tunnel.png"  # Using the card image for effect
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.animation_speed = 0.1
        self.damage = 0  # No damage, just visual effect
        self.scale_factor = 1.5
        self.spell_active = False
        
        # Load sound effect
        self.sound_played = False
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            parent1 = os.path.dirname(dir_path)
            parent2 = os.path.dirname(parent1)
            sound_path = "./Assets/Sounds/energyshieldsound.mp3"
            total_path = os.path.join(parent2, sound_path)
            self.tunneling_sound = pygame.mixer.Sound(total_path)
            self.tunneling_sound.set_volume(0.5)
        except:
            self.tunneling_sound = None
        
        # Phase effect properties
        self.phase_offset = 0
        
    def animate_spell(self, caster, target):
        """Animate the quantum tunneling effect with a shimmering aura"""
        
        if self.current_frame > len(self.animation_frames) - 1:
            self.apply_affect(caster)
            self.sound_played = False
            return False
        
        # Play sound effect at the start
        if self.current_frame == 0 and not self.sound_played and self.tunneling_sound:
            self.tunneling_sound.play()
            self.sound_played = True
        
        # Create a shimmering effect using the card image
        # We'll use a simple approach: draw the card image with varying transparency
        card_image = self.sprite.get_sprite((0, 0, 250, 350))  # Full card image
        
        # Scale down for effect
        effect_size = (80, 80)
        effect_image = pygame.transform.scale(card_image, effect_size)
        
        # Create a pulsing alpha effect
        alpha = int(128 + 127 * math.sin(self.current_frame * 0.5))
        effect_image.set_alpha(alpha)
        
        # Position around the caster with slight offset
        position = (caster.position_to_draw[0] - 20, 
                   caster.position_to_draw[1] - 40)
        
        sprite_position = self.sprite.draw_sprite_image_at(effect_image, position)
        
        # Draw the effect
        self.screen.blit(effect_image, sprite_position)
        
        self.current_frame += 1
        return True
    
    def apply_affect(self, target):
        """Apply the quantum tunneling effect to the target (caster)"""
        # The effect is already applied in the card's activate_card method
        # This is just for consistency with the spell interface
        pass
    
    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state 