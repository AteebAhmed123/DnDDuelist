import pygame
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
import time

class Heal(SpellBase):
    """Lightning spell that strikes a target"""
    
    # Define animation frames as class variable
    animation_frames = [
        (34, 144, 58, 76),    # Frame 1
        (34, 274, 54, 76),   # Frame 2
        (34, 404, 54, 76),   # Frame 2
        (164, 24, 58, 76),   # Frame 2
        (164, 144, 58, 76),   # Frame 2
        (164, 274, 58, 76),   # Frame 2
        (164, 404, 58, 76),   # Frame 2
        (295, 24, 58, 76),   # Frame 2
        (295, 154, 58, 76),   # Frame 2
        (295, 274, 58, 76),   # Frame 2
        (295, 414, 58, 76),   # Frame 2
        (415, 34, 58, 76),   # Frame 2
        (415, 164, 58, 76),   # Frame 2
        (415, 294, 58, 76)   # Frame 2
    ]
    
    def __init__(self, screen):
        """Initialize the lightning effect"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/HealEffect.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.animation_speed = 0.1  # Seconds between frames
        self.damage = 10  # Damage dealt by the lightning
        self.scale_factor = 4  # Scale the lightning to be twice as large
        self.spell_active = False
        
        # Load the lightning sound effect
        self.sound_played = False
        self.heal_sound = pygame.mixer.Sound("./Assets/Sounds/heal.mp3")
        
    def animate_spell(self, caster, target):
        """Animate the lightning spell with frame delays"""

        if (self.current_frame > len(self.animation_frames) - 1):
            self.apply_affect(caster)
            self.sound_played = False  # Reset sound flag when animation completes
            return False
        
        if self.current_frame == 0 and not self.sound_played and self.heal_sound:
            self.heal_sound.play()
            self.sound_played = True
        
        print(f"Current frame: {self.current_frame}")
        frame_coords = self.animation_frames[self.current_frame]
        heal_image = self.sprite.get_sprite(frame_coords)
        
        # Scale up the lightning image
        original_width = heal_image.get_width()
        original_height = heal_image.get_height()
        print(f"Healing image: {heal_image}", caster, original_width, original_height)
        new_width = int(original_width * self.scale_factor)
        new_height = int(original_height * self.scale_factor)
        heal_image = pygame.transform.scale(heal_image, (new_width, new_height))

        position = (caster.position_to_draw[0], 
                    caster.position_to_draw[1])
 
        sprite_standing_image_position = self.sprite.draw_sprite_image_at(
            heal_image, 
            position)  
         
        # Draw the lightning
        self.screen.blit(heal_image, sprite_standing_image_position)
        self.current_frame = self.current_frame + 1
        return True
        
        
    def apply_affect(self, target):
        print(target)
        """Apply damage to the target"""
        target.health.increase_health(3)
        print(f"Lightning deals {self.damage} damage to target!") 

    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state