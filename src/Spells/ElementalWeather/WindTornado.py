import pygame
import random
from Spells.SpellBase import SpellBase
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.ElementalWeather.WeatherSpells import WeatherSpells
import os
class WindTornado(WeatherSpells):
    """WindTornado spell that creates a tornado effect in the middle of the screen"""
    
    # Define the sprite frame coordinates for the tornado animation
    # These will need to be adjusted based on the actual sprite sheet layout
    TORNADO_FRAMES = [
        (8, 7, 46, 56),    # Frame 1 
        (74, 7, 46, 56),    # Frame 1 
        (137, 7, 46, 56),    # Frame 1 
        (201, 7, 46, 56),    # Frame 1 
        (265, 7, 46, 56)
    ]
    
    def __init__(self, screen):
        """Initialize the tornado effect"""
        super().__init__(screen)
        self.is_active = False
        self.sprite_path = "./Assets/Cards/Elementals/Weathers/Tornado.png"
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
        self.y = self.screen_height // 2 - 400
        
        # Size of the tornado
        self.tornado_width = 400
        self.tornado_height = 600
        
        # Wind visual effects
        self.wind_streaks = []
        self.debris_particles = []
        self.create_wind_effects()
        
        # Wind sound effect (commented out for now)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        parent3 = os.path.dirname(parent2)
        total_path = os.path.join(parent3, "./Assets/Sounds/Weathers/tornado.mp3")

        self.wind_sound = pygame.mixer.Sound(total_path)
        self.wind_sound.set_volume(0.5)
        self.sound_playing = False
    
    def create_wind_effects(self):
        """Create initial wind visual effects"""
        # Create wind streaks (horizontal lines)
        for _ in range(30):
            self.wind_streaks.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'length': random.randint(20, 100),
                'speed': random.randint(25, 50),
                'color': (200, 200, 255, random.randint(30, 100)),
                'thickness': random.randint(1, 3)
            })
        
        # Create debris particles
        for _ in range(40):
            self.debris_particles.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'size': random.randint(2, 6),
                'speed_x': random.randint(15, 30),
                'speed_y': random.randint(0, 6),
                'color': (
                    random.randint(150, 200),
                    random.randint(150, 200),
                    random.randint(150, 200),
                    random.randint(100, 180)
                ),
                'rotation': random.random() * 360
            })
    
    def start(self):
        """Start the tornado animation"""
        self.is_active = True
        self.current_frame = 0
        self.frame_counter = 0
        self.create_wind_effects()  # Reset wind effects
        if self.wind_sound and not self.sound_playing:
            self.wind_sound.play(-1)  # Loop the wind sound
            self.sound_playing = True
    
    def stop(self):
        """Stop the tornado animation"""
        self.is_active = False
        if self.wind_sound and self.sound_playing:
            self.wind_sound.stop()
            self.sound_playing = False
    
    def animate_spell(self, caster=None, target=None):
        """Render the tornado effect"""
        if not self.is_active:
            return False
        
        # Draw wind streaks
        self._draw_wind_streaks()
        
        # Draw debris particles
        self._draw_debris_particles()
        
        # Get the current frame from the sprite sheet
        frame_coords = self.TORNADO_FRAMES[int(self.current_frame)]
        tornado_image = self.sprite.get_sprite(frame_coords)
        
        # Scale the image to desired size
        tornado_image = pygame.transform.scale(tornado_image, (self.tornado_width, self.tornado_height))
        
        # Calculate position to center the tornado
        pos_x = self.x - (self.tornado_width // 2)
        pos_y = self.y - (self.tornado_height // 2)
        
        tornado_image.set_alpha(200)
        # Draw the tornado
        self.screen.blit(tornado_image, (pos_x, pos_y))
        self.screen.blit(tornado_image, (pos_x + 300, pos_y))
        self.screen.blit(tornado_image, (pos_x - 300, pos_y))
        
        # Update animation frame
        self.frame_counter += self.animation_speed
        self.current_frame = self.frame_counter % len(self.TORNADO_FRAMES)
        
        return True
    
    def _draw_wind_streaks(self):
        """Draw and update wind streak effects"""
        for streak in self.wind_streaks:
            # Create a surface for the wind streak with alpha
            streak_surface = pygame.Surface((streak['length'], streak['thickness']), pygame.SRCALPHA)
            streak_surface.fill(streak['color'])
            
            # Draw the streak
            self.screen.blit(streak_surface, (streak['x'], streak['y']))
            
            # Move the streak
            streak['x'] += streak['speed']
            
            # Reset if off screen
            if streak['x'] > self.screen_width:
                streak['x'] = -streak['length']
                streak['y'] = random.randint(0, self.screen_height)
                streak['length'] = random.randint(20, 100)
                streak['color'] = (200, 200, 255, random.randint(30, 100))
    
    def _draw_debris_particles(self):
        """Draw and update debris particles"""
        for particle in self.debris_particles:
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
            
            # Add some randomness to movement to simulate wind turbulence
            particle['speed_y'] += random.uniform(-0.5, 0.5)
            if particle['speed_y'] > 3: particle['speed_y'] = 3
            if particle['speed_y'] < -3: particle['speed_y'] = -3
            
            # Reset if off screen
            if particle['x'] > self.screen_width:
                particle['x'] = 0
                particle['y'] = random.randint(0, self.screen_height)
                particle['size'] = random.randint(2, 6)
                particle['speed_x'] = random.randint(5, 15)
                particle['color'] = (
                    random.randint(150, 200),
                    random.randint(150, 200),
                    random.randint(150, 200),
                    random.randint(100, 180)
                )
    
    def apply_effect(self):
        """Apply the spell's effect"""
        # Tornado doesn't have a direct effect on gameplay
        pass
