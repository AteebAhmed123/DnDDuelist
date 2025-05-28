import pygame
import random
import math
from Spells.SpellBase import SpellBase
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.ElementalWeather.WeatherSpells import WeatherSpells
import os
class Earthquake(WeatherSpells):
    """Earthquake spell that creates a nature disruption effect with trees falling down"""
    
    # Define the sprite frame coordinates for the tree/nature animation
    # These will need to be adjusted based on the actual sprite sheet layout
    NATURE_FRAMES = [
        (2, 193, 46, 65),     # Frame 1 - standing tree
        (52, 193, 46, 65),    # Frame 2 - tree starting to fall
        (102, 193, 46, 65),   # Frame 3 - tree falling more
        (162, 193, 57, 65),   # Frame 4 - tree falling further
        (0, 272, 69, 46),     # Frame 5 - tree almost down
        (79, 284, 76, 39),    # Frame 6 - fallen tree
    ]
    
    def __init__(self, screen):
        """Initialize the tree falling effect"""
        super().__init__(screen)
        self.is_active = False
        self.sprite_path = "./Assets/Cards/Elementals/Weathers/nature.png"
        self.sprite = SpriteUtil(self.sprite_path)
        
        # Animation properties
        self.current_frame = 0
        self.animation_speed = 0.1  # Frames per tick
        self.frame_counter = 0
        self.animation_completed = False
        
        # Screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Position (center of screen)
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2 - 150
        
        # Size of the tree
        self.tree_width = 70
        self.tree_height = 105
        
        # Shake effect for initial tree fall
        self.shake_intensity = 0
        self.max_shake_intensity = 15
        self.shake_decay = 0.95
        
        # Visual effects for initial impact
        self.dirt_particles = []
        self.rock_particles = []
        self.create_particles()
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        parent3 = os.path.dirname(parent2)
        total_path = os.path.join(parent3, "./Assets/Sounds/Weathers/earthquake.mp3")

        self.crash_sound = pygame.mixer.Sound(total_path)
        self.sound_played = False
    
    def create_particles(self):
        """Create particles for the tree falling impact"""
        # Create dirt particles
        for _ in range(30):
            self.dirt_particles.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(self.screen_height - 50, self.screen_height),
                'size': random.randint(2, 6),
                'speed_x': random.uniform(-2, 2),
                'speed_y': random.uniform(-8, -2),
                'color': (
                    random.randint(100, 150),  # R
                    random.randint(70, 120),   # G
                    random.randint(40, 80),    # B
                    random.randint(150, 255)   # Alpha
                ),
                'lifetime': random.randint(30, 90),
                'active': False,
                'gravity': random.uniform(0.1, 0.4)
            })
        
        # Create rock particles (larger than dirt)
        for _ in range(15):
            self.rock_particles.append({
                'x': random.randint(0, self.screen_width),
                'y': self.screen_height,
                'size': random.randint(4, 10),
                'speed_x': random.uniform(-1, 1),
                'speed_y': random.uniform(-10, -5),
                'color': (
                    random.randint(80, 120),   # R
                    random.randint(80, 120),   # G
                    random.randint(80, 120),   # B
                    255                         # Alpha
                ),
                'rotation': random.random() * 360,
                'rotation_speed': random.uniform(-5, 5),
                'active': False,
                'lifetime': random.randint(60, 120),
                'current_life': 0,
                'gravity': random.uniform(0.2, 0.5)
            })
    
    def start(self):
        """Start the tree falling animation"""
        self.is_active = True
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_completed = False
        self.shake_intensity = self.max_shake_intensity

        if self.crash_sound:
            self.crash_sound.play()
            self.sound_played = True
    
    def stop(self):
        """Stop the animation"""
        self.is_active = False
    
    def animate_spell(self, caster=None, target=None):
        """Render the tree falling effect"""
        if not self.is_active:
            return False
        
        # Calculate shake offset (only during the falling animation)
        shake_offset_x = 0
        shake_offset_y = 0
        
        if not self.animation_completed:
            # Apply shake decay
            self.shake_intensity *= self.shake_decay
            
            # Calculate shake offset
            shake_offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            shake_offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
        
        # When the tree hits the ground (frame 5), activate particles
        if int(self.current_frame) == 4 and not self.animation_completed:
            self._activate_particles()
        
        # Draw particles if active
        self._draw_dirt_particles()
        self._draw_rock_particles()
        
        # Get the current frame from the sprite sheet
        frame_idx = min(int(self.current_frame), len(self.NATURE_FRAMES) - 1)
        frame_coords = self.NATURE_FRAMES[frame_idx]
        tree_image = self.sprite.get_sprite(frame_coords)
        
        # Adjust width/height based on the current frame (fallen tree is wider than standing)
        current_width = self.tree_width
        current_height = self.tree_height
        
        if frame_idx >= 4:  # Adjust dimensions for fallen tree frames
            current_width = int(self.tree_width * 1.4)
            current_height = int(self.tree_height * 0.7)
        
        # Scale the image to desired size
        tree_image = pygame.transform.scale(tree_image, (current_width, current_height))
        
        # Calculate position to center the tree, with shake offset
        pos_x = self.x - (current_width // 2) + shake_offset_x
        pos_y = self.y - (current_height // 2) + shake_offset_y
        
        # Draw trees across the screen
        tree_positions = [
            (pos_x, pos_y),
            (pos_x + 50, pos_y),
            (pos_x - 50, pos_y),
            (pos_x + 100, pos_y),
            (pos_x - 100, pos_y),
            (pos_x + 200, pos_y),
            (pos_x - 200, pos_y),
            (pos_x + 300, pos_y),
            (pos_x - 300, pos_y)
        ]
        
        for x, y in tree_positions:
            self.screen.blit(tree_image, (x, y))
        
        # Update animation frame only if animation isn't completed
        if not self.animation_completed:
            self.frame_counter += self.animation_speed
            self.current_frame = self.frame_counter
            
            # Check if animation has completed
            if self.current_frame >= len(self.NATURE_FRAMES) - 1:
                self.current_frame = len(self.NATURE_FRAMES) - 1  # Stay on last frame
                self.animation_completed = True
        
        return True
    
    def _activate_particles(self):
        """Activate particles when the tree hits the ground"""
        # Activate dirt particles
        for particle in self.dirt_particles:
            if random.random() < 0.8:  # 80% chance
                particle['active'] = True
                # Position particles near the bases of trees
                tree_index = random.randint(0, 8)  # 9 trees
                base_x = self.x + (tree_index - 4) * 50  # -200 to +200 in steps of 50
                if tree_index >= 5:  # Adjust for wider spacing on the sides
                    base_x += 50 if tree_index == 5 else 100
                elif tree_index <= 3:
                    base_x -= 50 if tree_index == 3 else 100
                    
                particle['x'] = random.randint(base_x - 20, base_x + 20)
                particle['y'] = self.y + 40  # Near the base of the tree
                particle['lifetime'] = random.randint(30, 90)
        
        # Activate rock particles
        for rock in self.rock_particles:
            if random.random() < 0.7:  # 70% chance
                rock['active'] = True
                # Similar positioning as dirt particles
                tree_index = random.randint(0, 8)
                base_x = self.x + (tree_index - 4) * 50
                if tree_index >= 5:
                    base_x += 50 if tree_index == 5 else 100
                elif tree_index <= 3:
                    base_x -= 50 if tree_index == 3 else 100
                    
                rock['x'] = random.randint(base_x - 15, base_x + 15)
                rock['y'] = self.y + 40
                rock['current_life'] = 0
    
    def _draw_dirt_particles(self):
        """Draw and update dirt particles"""
        for particle in self.dirt_particles:
            if not particle['active']:
                continue
                
            # Draw the particle
            pygame.draw.circle(
                self.screen,
                particle['color'],
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )
            
            # Move the particle
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Apply gravity
            particle['speed_y'] += particle['gravity']
            
            # Reduce lifetime
            particle['lifetime'] -= 1
            
            # Deactivate if lifetime expired or off screen
            if particle['lifetime'] <= 0 or particle['y'] > self.screen_height:
                particle['active'] = False
    
    def _draw_rock_particles(self):
        """Draw and update rock particles"""
        for rock in self.rock_particles:
            if not rock['active']:
                continue
                
            # Draw the rock (as a polygon to show rotation)
            # Create a simple polygon for the rock
            points = []
            for i in range(5):
                angle = math.radians(rock['rotation'] + (i * 72))
                x = rock['x'] + rock['size'] * math.cos(angle)
                y = rock['y'] + rock['size'] * math.sin(angle)
                points.append((x, y))
            
            pygame.draw.polygon(
                self.screen,
                rock['color'],
                points
            )
            
            # Move the rock
            rock['x'] += rock['speed_x']
            rock['y'] += rock['speed_y']
            
            # Apply gravity
            rock['speed_y'] += rock['gravity']
            
            # Apply rotation
            rock['rotation'] += rock['rotation_speed']
            
            # Update lifetime
            rock['current_life'] += 1
            
            # Deactivate if lifetime expired or off screen
            if rock['current_life'] >= rock['lifetime'] or rock['y'] > self.screen_height:
                rock['active'] = False
    
    def apply_effect(self):
        """Apply the spell's effect"""
        # Tree falling doesn't have a direct effect on gameplay
        pass
