import pygame
import math
import random
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
from Characters.DamageOverTurn import DamageOverTurn
import os
class WindSlash(SpellBase):
    """WindSlash spell that launches a cutting wind projectile at the target"""
    
    # Define animation frames as class variable - these will be adjusted based on the actual sprite sheet
    animation_frames = [
        (20, 20, 46, 23),    # Frame 1
        (80, 20, 46, 23),    # Frame 1
        (150, 20, 46, 23),    # Frame 1
        (210, 20, 46, 23),    # Frame 1
        (280, 20, 46, 23)    # Frame 1
    ]
    
    # Define explosion frames
    explosion_frames = [
        (335, 42, 38, 64),    # Frame 1
        (533, 10, 92, 90),    # Frame 1
        (19, 138, 92, 90),    # Frame 1
        (148, 144, 87, 53)    # Frame 1
    ]
    
    def __init__(self, screen):
        """Initialize the wind slash spell"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/ElementalAttacks/WindSlash.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.SPRITE_PATH_SLASH = "./Assets/Cards/Elementals/ElementalAttacks/wind_slash_explosion.png"
        self.sprite_slash = SpriteUtil(self.SPRITE_PATH_SLASH)
        self.current_frame = 0
        self.damage = 2 # Damage dealt by the wind slash
        self.spell_active = False
        self.turns = 3
        # WindSlash properties
        self.wind_slash = None
        self.wind_slash_speed = 30  # Speed of wind slash (faster than fireball)
        self.wind_slash_size = (100, 65)  # Size of the wind slash (wider, less tall)
        self.scale_factor = 3  # Scale factor for the explosion
        self.explosion_active = False
        self.explosion_frame = 0
                  
        # Load the wind slash sound effects
        self.sound_played = False


        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        parent3 = os.path.dirname(parent2)
        soundlaunch = os.path.join(parent3, "./Assets/Sounds/Elementals/wind_launch.wav")
        soundexplosion = os.path.join(parent3, "./Assets/Sounds/Elementals/wind_slash.mp3")

        self.launch_sound = pygame.mixer.Sound(soundlaunch)
        self.explosion_sound = pygame.mixer.Sound(soundexplosion)
        self.launch_sound.set_volume(0.5)
        self.explosion_sound.set_volume(0.5)
        
    def animate_spell(self, caster, target):
        """Animate the wind slash spell
        
        Args:
            caster: The character casting the spell
            target: The intended target
            
        Returns:
            True if animation is still playing, False when complete
        """
        if not self.spell_active and not self.explosion_active:
            # Initialize wind slash when spell starts
            self.spell_active = True
            self.explosion_active = False
            self.current_frame = 0
            self.explosion_frame = 0
            self.sound_played = False
            
            # Create wind slash at caster position
            start_x = caster.position_to_draw[0]
            start_y = caster.position_to_draw[1]
            
            # Get target position
            target_x = target.position_to_draw[0]
            target_y = target.position_to_draw[1]
            
            # Create the wind slash
            self.wind_slash = {
                'x': start_x,
                'y': start_y,
                'target_x': target_x,
                'target_y': target_y,
                'speed': self.wind_slash_speed,
                'frame': 0,
                'hit': False
            }
            
            # Play the launch sound
            if self.launch_sound:
                self.launch_sound.play()
                self.sound_played = True
            
            return True
        
        # Handle explosion animation
        if self.explosion_active:
            if self.explosion_frame >= len(self.explosion_frames):
                # Explosion animation complete
                self.explosion_active = False
                self.spell_active = False
                return False
            
            # Draw explosion
            frame_coords = self.explosion_frames[int(self.explosion_frame)]
            explosion_image = self.sprite_slash.get_sprite(frame_coords)
            
            # Scale explosion
            explosion_width = int(explosion_image.get_width() * self.scale_factor)
            explosion_height = int(explosion_image.get_height() * self.scale_factor)
            explosion_image = pygame.transform.scale(explosion_image, (explosion_width, explosion_height))
            
            # Draw at target position
            position = (self.wind_slash['target_x'] - explosion_width // 2, 
                        self.wind_slash['target_y'] - explosion_height // 2)
            
            self.screen.blit(explosion_image, position)
            
            # Advance explosion frame
            self.explosion_frame += 0.7  # Faster explosion animation than fireball
            
            return True
        
        # Handle wind slash animation
        if self.spell_active:
            # If already hit, return false
            if self.wind_slash['hit']:
                return False
            
            # Calculate direction to target
            dir_x = self.wind_slash['target_x'] - self.wind_slash['x']
            dir_y = self.wind_slash['target_y'] - self.wind_slash['y']
            
            # Normalize direction
            distance = math.sqrt(dir_x * dir_x + dir_y * dir_y)
            if distance > 0:
                dir_x /= distance
                dir_y /= distance

            # Move wind slash towards target
            if distance < self.wind_slash['speed']:
                # If very close to target, snap to target position
                self.wind_slash['x'] = self.wind_slash['target_x']
                self.wind_slash['y'] = self.wind_slash['target_y']
            else:
                # Otherwise move by speed in the target direction
                self.wind_slash['x'] += dir_x * self.wind_slash['speed']
                self.wind_slash['y'] += dir_y * self.wind_slash['speed']
            
            # Update animation frame
            self.wind_slash['frame'] = (self.wind_slash['frame'] + 0.3) % len(self.animation_frames)
            
            # Draw wind slash
            frame_coords = self.animation_frames[int(self.wind_slash['frame'])]
            wind_slash_image = self.sprite.get_sprite(frame_coords)
            
            # Scale wind slash
            wind_slash_image = pygame.transform.scale(wind_slash_image, self.wind_slash_size)
            
            # Draw wind slash
            position = (self.wind_slash['x'] - wind_slash_image.get_width() // 2, 
                       self.wind_slash['y'] - wind_slash_image.get_height() // 2)
            
                        
            if (target.character_id == "Wizard"):
                ##transform the fireball sprite to be 180 degrees rotated
                self.screen.blit(pygame.transform.rotate(wind_slash_image, 180), position)
                if self.wind_slash['x'] <= target.position_to_draw[0]:
                    self.wind_slash['hit'] = True
                    self.spell_active = False
                    self.explosion_active = True
                    self.explosion_frame = 0
                    
                    # Play sound and apply effect
                    self.explosion_sound.play()
                    self.apply_affect(target)
            else:
                self.screen.blit(wind_slash_image, position)
                if self.wind_slash['x'] >= target.position_to_draw[0]:
                    self.wind_slash['hit'] = True
                    self.spell_active = False
                    self.explosion_active = True
                    self.explosion_frame = 0
                    
                    # Play sound and apply effect
                    self.explosion_sound.play()
                    self.apply_affect(target)
            
            # Simple collision detection - check if we've reached or passed the target
            # For right-moving wind slash

                
            
            return True
        
        return False

    def apply_affect(self, target):
        """Apply damage to the target"""
        # The user will implement this part themselves
        target.damage_over_turn = DamageOverTurn(self.damage, self.turns, "WindSlash")
            
    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state
