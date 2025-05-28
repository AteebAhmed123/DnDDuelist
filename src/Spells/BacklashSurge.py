import pygame
import math
import random
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
import os
class BacklashSurge(SpellBase):
    """Backlash Surge spell that applies vulnerability to a target (3x damage)"""
    
    def __init__(self, screen):
        """Initialize the vulnerability effect"""
        super().__init__(screen)
        # We'll create the vulnerability effect purely through rendering
        self.animation_speed = 0.1  # Seconds between frames
        self.frame_count = 30  # Number of frames in animation
        self.particles = []  # For particle effect
        self.particle_colors = [(255, 50, 50), (255, 100, 50), (255, 150, 50)]  # Red-orange colors
        
        # Sound effect
        self.sound_played = False
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        sound_path = "./Assets/Sounds/alarm.mp3"
        total_path = os.path.join(parent2, sound_path)
        self.surge_sound = pygame.mixer.Sound(total_path)
        self.surge_sound.set_volume(0.5)
        
    def start(self):
        """Start the vulnerability effect"""
        super().start()
        self.current_frame = 0
        self.particles = []
        self.generate_particles(100)  # Create initial particles
        
    def generate_particles(self, count):
        """Generate particles for the vulnerability effect"""
        for _ in range(count):
            # Random position, velocity, size, color, and lifespan
            particle = {
                'pos': [0, 0],  # Will be set based on target position
                'vel': [random.uniform(-2, 2), random.uniform(-2, 2)],
                'size': random.uniform(2, 6),
                'color': random.choice(self.particle_colors),
                'life': random.uniform(0.5, 1.0)  # Percentage of total animation
            }
            self.particles.append(particle)
            
    def animate_spell(self, caster, target):
        """Animate the vulnerability effect"""
        if self.current_frame >= self.frame_count:
            self.apply_effect(caster)
            self.sound_played = False
            return False
        
        # Play sound on first frame
        if self.current_frame == 0 and not self.sound_played and self.surge_sound:
            self.surge_sound.play()
            self.sound_played = True
            
        # Update particle positions
        self.update_particles(caster)
            
        # Draw a pulsing red aura around the target
        pulse_intensity = abs(math.sin(self.current_frame * 0.2)) * 180 + 75  # 75-255 range
        
        # Draw vulnerability symbols (lightning bolts) around target
        self.draw_vulnerability_indicators(caster, pulse_intensity)
        
        # Draw particles
        self.draw_particles()
        
        self.current_frame += 1
        return True
    
    def update_particles(self, target):
        """Update particle positions and properties"""
        target_center = (target.position_to_draw[0] + 65, target.position_to_draw[1] + 65)
        
        for particle in self.particles:
            # Initialize position at target center if not set
            if particle['pos'] == [0, 0]:
                particle['pos'] = [target_center[0], target_center[1]]
                
            # Update position based on velocity
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            
            # Reduce size slightly each frame
            particle['size'] *= 0.95
            
            # Update velocity to create spiral effect
            angle = math.atan2(particle['pos'][1] - target_center[1], 
                             particle['pos'][0] - target_center[0])
            particle['vel'][0] += 0.1 * math.cos(angle + math.pi/2)
            particle['vel'][1] += 0.1 * math.sin(angle + math.pi/2)
    
    def draw_particles(self):
        """Draw all particles"""
        for particle in self.particles:
            if particle['size'] > 0.5:  # Only draw visible particles
                pygame.draw.circle(
                    self.screen, 
                    particle['color'], 
                    (int(particle['pos'][0]), int(particle['pos'][1])), 
                    int(particle['size'])
                )
    
    def draw_vulnerability_indicators(self, target, intensity):
        """Draw visual indicators that target is vulnerable"""
        target_center = (target.position_to_draw[0], target.position_to_draw[1])
        radius = 80
        
        # Draw pulsing aura
        pygame.draw.circle(
            self.screen,
            (intensity, 50, 50, 100),  # Red with some transparency
            target_center,
            radius,
            3  # Width of circle
        )
        
        # Draw vulnerability "3x" text
        font = pygame.font.SysFont('Arial', 24, bold=True)
        text = font.render("3x", True, (255, 50, 50))
        text_rect = text.get_rect(center=(target_center[0], target_center[1] - radius - 15))
        self.screen.blit(text, text_rect)
        
        # Draw lightning bolt symbols around character
        self.draw_lightning_symbol(target_center, radius, intensity, 0)
        self.draw_lightning_symbol(target_center, radius, intensity, 2*math.pi/3)
        self.draw_lightning_symbol(target_center, radius, intensity, 4*math.pi/3)
    
    def draw_lightning_symbol(self, center, radius, intensity, angle_offset):
        """Draw a simple lightning bolt symbol"""
        angle = self.current_frame * 0.05 + angle_offset
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        
        # Lightning bolt coordinates (simple zigzag)
        points = [
            (x, y - 15),
            (x - 5, y - 5),
            (x + 5, y + 5),
            (x - 5, y + 15)
        ]
        
        # Draw lightning bolt
        color = (min(255, intensity + 50), 50, 50)
        pygame.draw.lines(self.screen, color, False, points, 3)
    
    def apply_effect(self, target):
        """Apply vulnerability effect to target"""
        target.self_damage_multiplier = 3.0


class StaticVulnerabilityEffect:
    """Class to render a static vulnerability effect for characters with vulnerable status"""
    
    @staticmethod
    def render_static_vulnerable(screen, character):
        """Render vulnerability indicators for a character that has vulnerable status"""
            
        # Character center position
        center = (character.position_to_draw[0], character.position_to_draw[1])
        
        # Draw red aura
        pygame.draw.circle(
            screen,
            (180, 50, 50, 150),  # Red with some transparency
            center,
            75,  # Radius
            2    # Width
        )
        
        # Draw "3x" text
        font = pygame.font.SysFont('Arial', 20, bold=True)
        text = font.render("3x", True, (255, 50, 50))
        text_rect = text.get_rect(center=(center[0], center[1] - 90))
        screen.blit(text, text_rect)
        
        # Draw small lightning bolts
        angle = pygame.time.get_ticks() * 0.001  # Slowly rotating
        for i in range(3):
            bolt_angle = angle + i * 2*math.pi/3
            x = center[0] + 75 * math.cos(bolt_angle)
            y = center[1] + 75 * math.sin(bolt_angle)
            
            # Simple lightning bolt
            points = [
                (x, y - 10),
                (x - 4, y - 3),
                (x + 4, y + 3),
                (x - 4, y + 10)
            ]
            
            pygame.draw.lines(screen, (255, 100, 50), False, points, 2) 