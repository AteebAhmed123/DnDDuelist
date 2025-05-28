import pygame
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
from QuantumMechanics.QuantumTunneling import QuantumTunneling
import time

class Lightning(SpellBase):
    """Lightning spell that strikes a target"""
    
    # Define animation frames as class variable
    animation_frames = [
        (0, 0, 54, 125),    # Frame 1
        (66, 3, 54, 125),   # Frame 2
        (131, 0, 54, 125),  # Frame 3
        (195, 0, 54, 125),  # Frame 4
        (262, 0, 54, 125),  # Frame 5
        (322, 0, 54, 125),  # Frame 6
        (450, 0, 54, 125),  # Frame 7
        (514, 0, 54, 125),  # Frame 8
        (518, 0, 54, 125)   # Frame 9
    ]
    
    def __init__(self, screen):
        """Initialize the lightning effect"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/lightning.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.animation_speed = 0.1  # Seconds between frames
        self.damage = 5  # Damage dealt by the lightning
        self.scale_factor = 5  # Scale the lightning to be twice as large
        self.spell_active = False
        
        # Load the lightning sound effect
        self.sound_played = False
        self.lightning_sound = pygame.mixer.Sound("./Assets/Sounds/lightning.wav")
        
    def animate_spell(self, caster, target):
        """Animate the lightning spell with frame delays"""
        # Reset animation state

        # self.lightning_sound.play()
        # print(self.current_frame, len(self.animation_frames))
        if (self.current_frame > len(self.animation_frames) - 1):
            self.apply_affect(caster, target)
            self.sound_played = False  # Reset sound flag when animation completes
            return False
        
        # Play sound effect at the start of the animation
        if self.current_frame == 0 and not self.sound_played and self.lightning_sound:
            self.lightning_sound.play()
            self.sound_played = True
        
        frame_coords = self.animation_frames[self.current_frame]
        lightning_image = self.sprite.get_sprite(frame_coords)
        
        # Scale up the lightning image
        original_width = lightning_image.get_width()
        original_height = lightning_image.get_height()
        new_width = int(original_width * self.scale_factor)
        new_height = int(original_height * self.scale_factor)
        lightning_image = pygame.transform.scale(lightning_image, (new_width, new_height))

        position = (target.position_to_draw[0], 
                    target.position_to_draw[1] - 250)
 
        sprite_standing_image_position = self.sprite.draw_sprite_image_at(
            lightning_image, 
            position)  
        
        # Draw the lightning
        self.screen.blit(lightning_image, sprite_standing_image_position)
        self.current_frame = self.current_frame + 1
        return True
        
        
    def apply_affect(self, caster, target):
        """Apply damage to the target using quantum tunneling system"""
        QuantumTunneling.apply_tunneling_damage(caster, target, self.damage)

    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state