import pygame
import math
import random
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
from Characters.DamageOverTurn import DamageOverTurn
import os
class EarthSpike(SpellBase):
    """WaterGeyser spell that erupts from below the target, lifting them up"""
    
    # Define animation frames as class variable - these will be adjusted based on the actual sprite sheet
    animation_frames = [
        (4, 27, 64, 37),    # Frame 1 - initial small splash
        (61, 27, 64, 37),    # Frame 1 - initial small splash
        (127, 27, 64, 37),    # Frame 1 - initial small splash
        (191, 27, 64, 37),    # Frame 1 - initial small splash
        (256, 27, 64, 37),    # Frame 1 - initial small splash
        (320, 27, 64, 37),    # Frame 1 - initial small splash
        (385, 27, 64, 37),    # Frame 1 - initial small splash
        (450, 27, 64, 37),    # Frame 1 - initial small splash
    ]
        
    def __init__(self, screen):
        """Initialize the water geyser spell"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/ElementalAttacks/EarthSpike.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_frame = 0
        self.damage = 2  # Damage dealt by the water geyser
        self.spell_active = False
        self.turns = 3
        # Geyser properties
        self.geyser = None
        self.geyser_size = (120, 200)  # Size of the geyser (wider and taller)
        self.scale_factor = 4  # Scale factor for the geyser
        
        # Target movement properties
        self.target_original_position = None  # Original position of the target
        self.target_vertical_offset = 0       # Current vertical offset
        self.max_vertical_offset = 100        # Maximum height to lift the target
        self.vertical_speed = 15               # Speed of vertical movement
        self.rising = True                    # Whether target is rising or falling
        
        # Animation stages
        self.pre_lift_frames = 2      # Frames before target starts rising
        self.lift_duration_frames = 3  # Frames during which target is lifted
        self.post_lift_frames = 2      # Frames after target starts falling
                  
        # Load the water geyser sound effects
        self.sound_played = False
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        parent3 = os.path.dirname(parent2)
        total_path = os.path.join(parent3, "./Assets/Sounds/Elementals/earthspike.mp3")
        self.geyser_sound = pygame.mixer.Sound(total_path)
        self.geyser_sound.set_volume(0.5)
    
    def animate_spell(self, caster, target):
        """Animate the water geyser spell
        
        Args:
            caster: The character casting the spell
            target: The intended target
            
        Returns:
            True if animation is still playing, False when complete
        """
        target_position_draw = list(target.position_to_draw)
        if not self.spell_active:
            # Initialize geyser when spell starts
            self.spell_active = True
            self.current_frame = 0
            self.sound_played = False
            self.target_vertical_offset = 0
            self.rising = True
            
            # Save target's original position
            self.target_original_position = target_position_draw
            
            # Position geyser at target's feet
            target_x = target_position_draw[0]
            target_y = target_position_draw[1] + 90  # Adjust to appear at feet level
            
            # Create the geyser
            self.geyser = {
                'x': target_x,
                'y': target_y,
                'frame': 0
            }
            
            # Play the geyser sound
            if self.geyser_sound:
                self.geyser_sound.play()
                self.sound_played = True
            
            return True
        
        # Handle geyser animation
        if self.spell_active:
            # Update animation frame
            current_frame = int(self.geyser['frame'])
            
            # Draw geyser
            frame_coords = self.animation_frames[current_frame]
            geyser_image = self.sprite.get_sprite(frame_coords)
            
            # Scale geyser (larger for more dramatic effect)
            geyser_width = int(geyser_image.get_width() * self.scale_factor)
            geyser_height = int(geyser_image.get_height() * self.scale_factor)
            geyser_image = pygame.transform.scale(geyser_image, (geyser_width, geyser_height))
            
            # Position at the target's feet but centered horizontally
            position = (self.geyser['x'] - geyser_width // 2, 
                        self.geyser['y'] - geyser_height)
            
            # Draw the geyser
            self.screen.blit(geyser_image, position)
                        
                        # Advance to next frame
            self.geyser['frame'] += 0.4  # Slower animation
            
            # Check if animation is complete
            if self.geyser['frame'] >= len(self.animation_frames):
                # Reset target position to ensure it's back to original
                self.apply_affect(target)
                self.spell_active = False
                return False
            
            return True
        
        return False
        
    def apply_affect(self, target):
        """Apply damage to the target"""
        target.damage_over_turn = DamageOverTurn(self.damage, self.turns, "EarthSpike")
            
    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state
