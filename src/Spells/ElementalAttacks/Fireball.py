import pygame
import math
import random
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
from Characters.DamageOverTurn import DamageOverTurn
class Fireball(SpellBase):
    """Fireball spell that launches a fiery projectile at the target"""
    
    # Define animation frames as class variable - these will be adjusted based on the actual sprite sheet
    animation_frames = [
        (4, 14, 62, 37),    # Frame 1
        (74, 14, 62, 37),   # Frame 2
        (134, 14, 62, 37),   # Frame 2
        (194, 14, 62, 37),   # Frame 2
        (264, 14, 62, 37)
    ]
    
    # Define explosion frames
    explosion_frames = [
        (334, 14, 62, 37),
        (404, 14, 62, 37),
        (464, 14, 62, 37),
        (534, 14, 62, 37),
        (580, 14, 62, 37)
    ]
    
    def __init__(self, screen):
        """Initialize the fireball spell"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/Elementals/ElementalAttacks/Fireball.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_frame = 0
        self.damage = 2  # Damage dealt by the fireball
        self.spell_active = False
        self.turns = 3
        # Fireball properties
        self.fireball = None
        self.fireball_speed = 16 # Speed of fireball
        self.fireball_size = (80, 80)  # Size of the fireball
        self.scale_factor = 6 # Scale factor for the explosion
        self.explosion_active = False
        self.explosion_frame = 0
        
        # Load the fireball sound effects
        self.sound_played = False
        self.launch_sound = pygame.mixer.Sound("./Assets/Sounds/Elementals/fire_launch.mp3")
        self.explosion_sound = pygame.mixer.Sound("./Assets/Sounds/Elementals/fire_explosion.mp3")
    
    def animate_spell(self, caster, target):
        """Animate the fireball spell
        
        Args:
            caster: The character casting the spell
            target: The intended target
            
        Returns:
            True if animation is still playing, False when complete
        """
        if not self.spell_active and not self.explosion_active:
            # Initialize fireball when spell starts
            self.spell_active = True
            self.explosion_active = False
            self.current_frame = 0
            self.explosion_frame = 0
            self.sound_played = False
            
            # Create fireball
            start_x = caster.position_to_draw[0]
            start_y = caster.position_to_draw[1]
            
            # Target position
            target_x = target.position_to_draw[0]
            target_y = target.position_to_draw[1]
            
            # Calculate direction vector for straight line movement
            dx = target_x - start_x
            dy = target_y - start_y
            distance = math.sqrt(dx * dx + dy * dy)
            
            # Normalize direction vector
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
            
            # Create the fireball
            self.fireball = {
                'x': start_x,
                'y': start_y,
                'start_x': start_x,
                'start_y': start_y,
                'target_x': target_x,
                'target_y': target_y,
                'dx': dx,
                'dy': dy,
                'distance': distance,
                'travelled': 0.0,
                'progress': 0.0,
                'speed': self.fireball_speed,
                'frame': 0
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
            explosion_image = self.sprite.get_sprite(frame_coords)
            
            # Scale explosion
            explosion_width = int(explosion_image.get_width() * self.scale_factor)
            explosion_height = int(explosion_image.get_height() * self.scale_factor)
            explosion_image = pygame.transform.scale(explosion_image, (explosion_width, explosion_height))
            
            # Draw at target position
            position = (self.fireball['target_x'] - explosion_width // 2, 
                        self.fireball['target_y'] - explosion_height // 2)
            
            self.screen.blit(explosion_image, position)
            
            # Advance explosion frame
            self.explosion_frame += 0.5  # Slower explosion animation
            
            return True
        
        # Handle fireball animation
        if self.spell_active:
            # Update distance travelled in straight line
            step_distance = self.fireball['speed']
            self.fireball['travelled'] += step_distance
            
            # Calculate progress as ratio of distance travelled to total distance
            self.fireball['progress'] = min(1.0, self.fireball['travelled'] / self.fireball['distance'])
            
            # Update position in straight line
            self.fireball['x'] = self.fireball['start_x'] + self.fireball['dx'] * self.fireball['travelled']
            self.fireball['y'] = self.fireball['start_y'] + self.fireball['dy'] * self.fireball['travelled']
            
            # Update animation frame
            self.fireball['frame'] = (self.fireball['frame'] + 0.3) % len(self.animation_frames)
            
            # Draw fireball
            frame_coords = self.animation_frames[int(self.fireball['frame'])]
            fireball_image = self.sprite.get_sprite(frame_coords)
            
            # Scale fireball
            fireball_image = pygame.transform.scale(fireball_image, self.fireball_size)
            
            # Draw fireball
            position = (self.fireball['x'] - fireball_image.get_width() // 2, 
                        self.fireball['y'] - fireball_image.get_height() // 2)
            
            if (target.character_id == "Wizard"):
                ##transform the fireball sprite to be 180 degrees rotated
                self.screen.blit(pygame.transform.rotate(fireball_image, 180), position)
            else:
                self.screen.blit(fireball_image, position)
            
            # Check if fireball has reached target using progress
            if self.fireball['progress'] >= 1.0:
                # Transition to explosion
                self.spell_active = False
                self.explosion_active = True
                self.explosion_frame = 0
                
                if self.explosion_sound:
                    self.explosion_sound.play()
                
                # Apply effect to target
                self.apply_affect(target)
            
            return True
        
        return False
    
    def apply_affect(self, target):
        """Apply damage to the target"""
        target.damage_over_turn = DamageOverTurn(self.damage, self.turns, "Fireball")
            
    def set_spell_state(self, spell_state):
        """Set the spell active state"""
        self.spell_active = spell_state 