import pygame
import random
from Spells.SpellBase import SpellBase
from SpriteUtil.SpriteUtil import SpriteUtil

class Rain(SpellBase):
    """Rain spell that creates a rain effect in the background"""
    
    def __init__(self, screen):
        """Initialize the rain effect"""
        super().__init__(screen)
        self.is_active = False
        self.raindrops = []
        self.rain_color = (120, 160, 255, 220)  # More visible blue-ish color
        self.rain_width = 3  # Thicker raindrops
        self.rain_height = 20  # Longer raindrops
        self.rain_count = 300  # More raindrops
        self.rain_speed = 25  # Faster rain
        self.thunder_timer = 0
        self.thunder_frequency = 5  # Seconds between thunder
        self.thunder_duration = 0.2  # How long the thunder flash lasts
        self.thunder_active = False
        self.thunder_alpha = 0
        
        # Screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Load the rain sound effect
        self.thunder_sound = pygame.mixer.Sound("./Assets/Sounds/Weathers/RainThunder.mp3")
        self.sound_playing = False
        
        # Create initial raindrops
        self._create_raindrops()
    
    def _create_raindrops(self):
        """Create the initial set of raindrops"""
        self.raindrops = []
        for _ in range(self.rain_count):
            x = random.randint(0, self.screen_width)
            y = random.randint(-100, self.screen_height)
            speed = random.randint(self.rain_speed - 5, self.rain_speed + 5)
            length = random.randint(self.rain_height - 5, self.rain_height + 6)
            self.raindrops.append({
                'x': x,
                'y': y,
                'speed': speed,
                'length': length
            })
    
    def start(self):
        """Start the rain animation"""
        self.is_active = True
        self._create_raindrops()  # Reset raindrops when starting
        self.thunder_sound.play(-1)  # Loop the rain sound
        self.sound_playing = True
    
    def stop(self):
        """Stop the rain animation"""
        self.is_active = False
        self.sound_playing = False  # Loop the rain sound
        # if self.rain_sound and self.sound_playing:
        #     self.rain_sound.stop()
        #     self.sound_playing = False
    
    def animate_spell(self, caster=None, target=None):
        """Render the rain effect"""
        print("rain")
        if not self.is_active:
            return False
        
        # Draw each raindrop
        for drop in self.raindrops:
            # Draw the raindrop as a line
            pygame.draw.line(
                self.screen,
                self.rain_color,
                (drop['x'], drop['y']),
                (drop['x'], drop['y'] + drop['length']),
                self.rain_width
            )
            
            # Update raindrop position
            drop['y'] += drop['speed']
            
            # If raindrop goes off screen, reset it to the top
            if drop['y'] > self.screen_height:
                drop['y'] = random.randint(-100, -10)
                drop['x'] = random.randint(0, self.screen_width)
        
        # Handle occasional thunder flashes
        current_time = pygame.time.get_ticks() / 1000  # Current time in seconds
                
        # If thunder is active, create a flash effect
        if self.thunder_active:
            elapsed = current_time - self.thunder_timer
            
            if elapsed < self.thunder_duration:
                # Flash intensity based on time
                flash_intensity = int(180 * (1 - elapsed / self.thunder_duration))
                flash_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                flash_surface.fill((255, 255, 255, flash_intensity))
                self.screen.blit(flash_surface, (0, 0))
            else:
                self.thunder_active = False
        
        return True
    
    def apply_effect(self):
        """Apply the spell's effect"""
        # Rain doesn't have a direct effect on gameplay
        pass 