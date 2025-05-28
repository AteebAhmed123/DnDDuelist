import pygame
import random
from Spells.SpellBase import SpellBase
from SpriteUtil.SpriteUtil import SpriteUtil
import math
from Spells.ElementalWeather.WeatherSpells import WeatherSpells
import os
class HeatWave(WeatherSpells):
    """HeatWave spell that creates a heat/fire effect in the middle of the screen"""
    
    # Define the sprite frame coordinates for the fire animation
    # These will need to be adjusted based on the actual sprite sheet layout
    FIRE_FRAMES = [
        (23, 34, 48, 66),     # Frame 1 
        (123, 34, 48, 66),     # Frame 1 
        (217, 34, 48, 66),     # Frame 1 
        (313, 34, 48, 66),     # Frame 1 
    ]
    
    def __init__(self, screen):
        """Initialize the heat wave effect"""
        super().__init__(screen)
        self.is_active = False
        self.sprite_path = "./Assets/Cards/Elementals/Weathers/fire.png"
        self.sprite = SpriteUtil(self.sprite_path)
        
        # Animation properties
        self.current_frame = 0
        self.animation_speed = 0.15  # Frames per tick
        self.frame_counter = 0
        
        # Screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Position (center of screen)
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2 + 140
        
        # Size of the fire
        self.fire_width = 350
        self.fire_height = 490
        
        # Heat visual effects
        self.heat_particles = []
        self.embers = []
        self.smoke_particles = []
        self.create_heat_effects()
        
        # Heat distortion effect
        self.heat_timer = 0
        self.heat_intensity = 0
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        parent3 = os.path.dirname(parent2)
        total_path = os.path.join(parent3, "./Assets/Sounds/Weathers/Fire.mp3")

        self.fire_sound = pygame.mixer.Sound(total_path)
        self.fire_sound.set_volume(0.5)
        self.sound_playing = False
    
    def create_heat_effects(self):
        """Create initial heat visual effects"""
        # Create heat particles (rising)
        for _ in range(50):
            self.heat_particles.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'size': random.randint(4, 10),
                'speed': random.randint(5, 10),
                'color': (
                    random.randint(200, 255),  # Red
                    random.randint(100, 180),  # Green
                    random.randint(0, 80),     # Blue
                    random.randint(20, 120)    # Alpha
                ),
                'lifetime': random.randint(50, 150)
            })
        
        # Create embers (sparks)
        for _ in range(30):
            self.embers.append({
                'x': random.randint(self.x - 200, self.x + 200),
                'y': random.randint(self.y - 100, self.y + 100),
                'size': random.randint(1, 3),
                'speed_x': random.uniform(1, 3),
                'speed_y': random.uniform(-2, 1),
                'color': (
                    random.randint(220, 255),  # Red
                    random.randint(120, 220),  # Green
                    random.randint(0, 50),     # Blue
                    255                         # Alpha
                ),
                'lifetime': random.randint(20, 60),
                'current_life': 0
            })
            
        # Create smoke particles
        for _ in range(25):
            self.smoke_particles.append({
                'x': random.randint(self.x - 300, self.x + 300),
                'y': random.randint(self.y - 50, self.y + 200),
                'size': random.randint(15, 30),
                'speed': random.uniform(3, 6),
                'color': (
                    random.randint(50, 80),    # Red
                    random.randint(50, 80),    # Green
                    random.randint(50, 80),    # Blue
                    random.randint(20, 80)     # Alpha
                ),
                'lifetime': random.randint(60, 120),
                'current_life': 0
            })
    
    def start(self):
        """Start the heat wave animation"""
        self.is_active = True
        self.current_frame = 0
        self.frame_counter = 0
        self.create_heat_effects()  # Reset heat effects
        if self.fire_sound and not self.sound_playing:
            self.fire_sound.play(-1)  # Loop the fire sound
            self.sound_playing = True
    
    def stop(self):
        """Stop the heat wave animation"""
        self.is_active = False
        if self.fire_sound and self.sound_playing:
            self.fire_sound.stop()
            self.sound_playing = False
    
    def animate_spell(self, caster=None, target=None):
        """Render the heat wave effect"""
        if not self.is_active:
            return False
            
        # # Draw heat distortion
        # self._draw_heat_distortion()
        
        # Draw heat particles
        self._draw_heat_particles()
        
        # Get the current frame from the sprite sheet
        frame_coords = self.FIRE_FRAMES[int(self.current_frame)]
        fire_image = self.sprite.get_sprite(frame_coords)
        
        # Scale the image to desired size
        fire_image = pygame.transform.scale(fire_image, (self.fire_width, self.fire_height))
        
        # Calculate position to center the fire
        pos_x = self.x - (self.fire_width // 2)
        pos_y = self.y - (self.fire_height // 2)
        
        # Set alpha for the fire (semi-transparent)
        fire_image.set_alpha(200)
        
        # Draw glow beneath each fire (as a circle)
        self._draw_fire_glow(pos_x, pos_y)
        self._draw_fire_glow(pos_x + 250, pos_y)
        self._draw_fire_glow(pos_x - 250, pos_y)
        
        # Draw the fire
        self.screen.blit(fire_image, (pos_x, pos_y))
        self.screen.blit(fire_image, (pos_x + 250, pos_y))
        self.screen.blit(fire_image, (pos_x - 250, pos_y))
        
        # Draw embers (in front of the fire)
        self._draw_embers()

        # Update animation frame
        self.frame_counter += self.animation_speed
        self.current_frame = self.frame_counter % len(self.FIRE_FRAMES)
        
        # Update heat intensity for distortion effect
        self.heat_timer += 0.1
        self.heat_intensity = (math.sin(self.heat_timer) + 1) / 2  # Oscillate between 0 and 1
        
        return True
        
    def _draw_fire_glow(self, pos_x, pos_y):
        """Draw a glowing effect beneath the fire"""
        # Calculate the intensity based on the current frame for flickering
        flicker = random.uniform(0.8, 1.0)
        
        # Base position (bottom center of the fire)
        glow_x = pos_x + (self.fire_width // 2)
        glow_y = pos_y + (self.fire_height * 0.8)
        
        # Draw multiple circles with decreasing opacity for a soft glow
        for radius in range(100, 20, -20):
            alpha = int(50 * flicker * (radius / 100))
            glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surface,
                (255, 150, 50, alpha),  # Orange-yellow with variable alpha
                (radius, radius),
                radius
            )
            self.screen.blit(glow_surface, (glow_x - radius, glow_y - radius))
    
    def _draw_heat_particles(self):
        """Draw and update heat particles (rising hot air)"""
        for particle in self.heat_particles:
            # Draw the particle
            pygame.draw.circle(
                self.screen,
                particle['color'],
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )
            
            # Move the particle upward
            particle['y'] -= particle['speed']
            particle['x'] += random.uniform(-0.5, 0.5)  # Slight horizontal drift
            
            # Reduce lifetime
            particle['lifetime'] -= 1
            
            # Reset if off screen or lifetime expired
            if particle['y'] < 0 or particle['lifetime'] <= 0:
                particle['y'] = random.randint(self.screen_height - 50, self.screen_height)
                particle['x'] = random.randint(0, self.screen_width)
                particle['size'] = random.randint(2, 8)
                particle['speed'] = random.randint(3, 8)
                particle['color'] = (
                    random.randint(200, 255),  # Red
                    random.randint(100, 180),  # Green
                    random.randint(0, 80),     # Blue
                    random.randint(20, 120)    # Alpha
                )
                particle['lifetime'] = random.randint(50, 150)
    
    def _draw_embers(self):
        """Draw and update ember particles (sparks)"""
        for ember in self.embers:
            # Draw the ember (small bright dot)
            pygame.draw.circle(
                self.screen,
                ember['color'],
                (int(ember['x']), int(ember['y'])),
                ember['size']
            )
            
            # Move the ember
            ember['x'] += ember['speed_x']
            ember['y'] += ember['speed_y']
            
            # Add gravity effect
            ember['speed_y'] += 0.05
            
            # Reduce ember size as it ages
            if ember['size'] > 0.2:
                ember['size'] -= 0.02
            
            # Update lifetime
            ember['current_life'] += 1
            
            # Reset if lifetime expired
            if ember['current_life'] >= ember['lifetime']:
                # Spawn new embers from one of the fire locations
                fire_index = random.randint(0, 2)
                base_x = self.x + (fire_index - 1) * 250  # -250, 0, or 250 offset
                
                ember['x'] = random.randint(base_x - 50, base_x + 50)
                ember['y'] = random.randint(self.y - 50, self.y + 50)
                ember['size'] = random.randint(1, 3)
                ember['speed_x'] = random.uniform(-1, 1)
                ember['speed_y'] = random.uniform(-4, -1)
                ember['color'] = (
                    random.randint(220, 255),  # Red
                    random.randint(120, 220),  # Green
                    random.randint(0, 50),     # Blue
                    255                         # Alpha
                )
                ember['lifetime'] = random.randint(20, 60)
                ember['current_life'] = 0
                
    def _draw_smoke_particles(self):
        """Draw and update smoke particles"""
        for smoke in self.smoke_particles:
            # Draw the smoke particle (larger, transparent circle)
            pygame.draw.circle(
                self.screen,
                smoke['color'],
                (int(smoke['x']), int(smoke['y'])),
                smoke['size']
            )
            
            # Move the smoke upward and with slight drift
            smoke['y'] -= smoke['speed']
            smoke['x'] += random.uniform(-0.3, 0.3)
            
            # Increase size as it rises (smoke disperses)
            smoke['size'] += 0.05
            
            # Update lifetime
            smoke['current_life'] += 1
            
            # Fade out as it ages
            if smoke['current_life'] > smoke['lifetime'] // 2:
                # Gradually reduce alpha
                if smoke['color'][3] > 5:
                    r, g, b, a = smoke['color']
                    smoke['color'] = (r, g, b, max(5, a - 1))
            
            # Reset if lifetime expired
            if smoke['current_life'] >= smoke['lifetime']:
                # Spawn new smoke from one of the fire locations
                fire_index = random.randint(0, 2)
                base_x = self.x + (fire_index - 1) * 250  # -250, 0, or 250 offset
                
                smoke['x'] = random.randint(base_x - 30, base_x + 30)
                smoke['y'] = random.randint(self.y - 20, self.y + 100)
                smoke['size'] = random.randint(5, 15)
                smoke['speed'] = random.uniform(1, 3)
                smoke['color'] = (
                    random.randint(50, 80),    # Red
                    random.randint(50, 80),    # Green
                    random.randint(50, 80),    # Blue
                    random.randint(20, 80)     # Alpha
                )
                smoke['lifetime'] = random.randint(60, 120)
                smoke['current_life'] = 0
    
    def _draw_heat_distortion(self):
        """Draw heat distortion effect"""
        # Create a subtle heat haze effect 
        for y in range(self.y - 200, self.y + 300, 15):
            amplitude = 3 * self.heat_intensity
            for x in range(0, self.screen_width, 10):
                offset = int(amplitude * math.sin((x/30) + self.heat_timer))
                
                # Draw a small vertical line with distortion
                pygame.draw.line(
                    self.screen,
                    (255, 255, 255, 10),  # Very transparent white
                    (x, y + offset),
                    (x, y + offset + 3),
                    1
                )
    
    def apply_effect(self):
        """Apply the spell's effect"""
        # Heat wave doesn't have a direct effect on gameplay
        pass
