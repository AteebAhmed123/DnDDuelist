import pygame
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
import time

class Barrier(SpellBase):
    """Lightning spell that strikes a target"""
    
    # Define animation frames as class variable
    animation_frames = [
        (1586, 238, 181, 75),    # Frame 1
        (1955, 59, 402, 406),    # Frame 1
        (1955, 59, 402, 406),    # Frame 1
        (47, 530, 402, 406),    # Frame 1
        (517, 530, 402, 406),    # Frame 1
        (997, 530, 402, 406),    # Frame 1
        (1477, 530, 402, 406),    # Frame 1
        (996, 1010, 402, 406)    # Frame 1
    ]
    
    def __init__(self, screen):
        """Initialize the lightning effect"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Shield.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.animation_speed = 0.1  # Seconds between frames
        self.damage = 10  # Damage dealt by the lightning
        self.scale_factor = 4  # Scale the lightning to be twice as large
        self.spell_active = False
        
        # Load the lightning sound effect
        self.sound_played = False
        self.heal_sound = pygame.mixer.Sound("./Assets/Sounds/energyshieldsound.mp3")
        
    def animate_spell(self, caster, target):
        """Animate the lightning spell with frame delays"""

        if (self.current_frame > len(self.animation_frames) - 1):
            self.apply_affect(caster)
            self.sound_played = False  # Reset sound flag when animation completes
            return False
        
        if self.current_frame == 0 and not self.sound_played and self.heal_sound:
            self.heal_sound.play()
            self.sound_played = True
        
        frame_coords = self.animation_frames[self.current_frame]
        shield_image = self.sprite.get_sprite(frame_coords)
        shield_image = pygame.transform.scale(shield_image, (130, 130))

        position = (caster.position_to_draw[0], 
                    caster.position_to_draw[1])
 
        sprite_standing_image_position = self.sprite.draw_sprite_image_at(
            shield_image, 
            position)  
         
        # Draw the lightning
        self.screen.blit(shield_image, sprite_standing_image_position)
        self.current_frame = self.current_frame + 1
        return True
    

    def apply_affect(self, target):
        target.shield = True

    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state


class StaticBarrierShield:

    @staticmethod
    def render_static_shield(screen, caster):
        SPRITE_PATH = "./Assets/Cards/Shield.png"
        sprite = SpriteUtil(SPRITE_PATH)

        shield_image = sprite.get_sprite((996, 1010, 402, 406))
        
        original_width = shield_image.get_width()
        original_height = shield_image.get_height()
        shield_image = pygame.transform.scale(shield_image, (130, 130))

        position = (caster.position_to_draw[0], 
                    caster.position_to_draw[1])
 
        sprite_standing_image_position = sprite.draw_sprite_image_at(
            shield_image, 
            position)  
         
        # Draw the lightning
        screen.blit(shield_image, sprite_standing_image_position)