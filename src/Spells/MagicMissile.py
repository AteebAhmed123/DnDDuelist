import pygame
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
import time

class MagicMissile(SpellBase):
    """Lightning spell that strikes a target"""
    
    # Define animation frames as class variable

        # (26, 33, 52, 36),    # Frame 1
        # (126, 33, 52, 36),    # Frame 1
        # (226, 33, 52, 36),    # Frame 1
        # (326, 33, 52, 36),    # Frame 1
        # (426, 33, 52, 36),    # Frame 1
        # (526, 33, 52, 36),    # Frame 1
        # (626, 33, 52, 36),    # Frame 1
        # (726, 33, 52, 36),    # Frame 1
        # (826, 33, 52, 36)    # Frame 1

    animation_frames = [
        (26, 33, 52, 36),    # Frame 1
        (126, 33, 52, 36),    # Frame 1
        (226, 33, 52, 36),    # Frame 1
        (326, 33, 52, 36),    # Frame 1
        (426, 33, 52, 36),    # Frame 1
        (526, 33, 52, 36),    # Frame 1
        (626, 33, 52, 36),    # Frame 1
        (726, 33, 52, 36),    # Frame 1
        (826, 33, 52, 36)    # Frame 1 # Frame 1
    ]


    # animation_frames = [
    #     (26, 33, 52, 36),    # Frame 1
    #     (36, 5, 25, 21),    # Frame 1
    #     (66, 5, 25, 21),    # Frame 1
    #     (98, 5, 25, 21),    # Frame 1
    #     (131, 5, 25, 21),    # Frame 1
    #     (166, 5, 25, 21),    # Frame 1
    #     (187, 5, 25, 21),    # Frame 1
    #     (229, 5, 25, 21),    # Frame 1
    #     (292, 5, 25, 21)    # Frame 1
    # ]
    
    def __init__(self, screen):
        """Initialize the lightning effect"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/magicmissile2.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.animation_speed = 0.1  # Seconds between frames
        self.damage = 10  # Damage dealt by the lightning
        self.scale_factor = 2  # Scale the lightning to be twice as large
        self.spell_active = False
        
        # Load the lightning sound effect
        self.sound_played = False
        self.missile_sound = pygame.mixer.Sound("./Assets/Sounds/magicmissile.mp3")
        
    def animate_spell(self, caster, target):
        """Animate multiple magic missiles traveling from caster to target in sequence"""
        
        # Check if animation is complete
        if self.current_frame >= len(self.animation_frames):
            self.apply_affect(target)
            self.sound_played = False  # Reset sound flag
            return False
        
        # Play sound effect at the start of the animation
        if self.current_frame == 0 and not self.sound_played:
            self.missile_sound.play()
            self.sound_played = True
        
        # Get the current animation frame
        frame_coords = self.animation_frames[self.current_frame]
        missile_image = self.sprite.get_sprite(frame_coords)
        
        # Scale the missile image
        original_width = missile_image.get_width()
        original_height = missile_image.get_height()
        new_width = int(original_width * self.scale_factor)
        new_height = int(original_height * self.scale_factor)

        missile_image = pygame.transform.scale(missile_image, (new_width, new_height))
        
        # Calculate the missile's position based on its progress from caster to target
        progress = min(1.0, self.current_frame / (len(self.animation_frames) - 1))
        
        # Determine if we need to flip the missile based on direction
        flip_missile = caster.position_to_draw[0] > target.position_to_draw[0]
        if flip_missile:
            missile_image = pygame.transform.flip(missile_image, True, False)
        
        # Render 3 missiles with spacing along the path
        missile_spacing = [
            -0.2,  # First missile (trailing behind)
            0.0,   # Second missile (at current position)
            0.2    # Third missile (ahead)
        ]
        
        for spacing in missile_spacing:
            # Adjust progress for each missile to create spacing
            missile_progress = max(0.0, min(1.0, progress + spacing))
            
            # Linear interpolation between caster and target positions
            current_x = caster.position_to_draw[0] + (target.position_to_draw[0] - caster.position_to_draw[0]) * missile_progress
            current_y = caster.position_to_draw[1] + (target.position_to_draw[1] - caster.position_to_draw[1]) * missile_progress
            
            # Only draw missiles that are within the path (not before start or after end)
            if 0.0 <= missile_progress <= 1.0:
                # Create a rect for the missile at the calculated position
                missile_rect = missile_image.get_rect(center=(current_x, current_y))
                
                # Draw the missile
                self.screen.blit(missile_image, missile_rect)
        
        # Advance to the next frame
        self.current_frame += 1
        
        return True

    def apply_affect(self, target):
        """Apply damage to the target"""
        target.health.reduce_health(10)
        print(f"Lightning deals {self.damage} damage to target!") 

    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state