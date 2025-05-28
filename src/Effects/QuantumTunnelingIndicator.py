import pygame
import math
import random

class QuantumTunnelingIndicator:
    """Visual indicator for quantum tunneling effects"""
    
    def __init__(self, screen):
        """Initialize the quantum tunneling indicator
        
        Args:
            screen: The pygame screen to render on
        """
        self.screen = screen
        
        # Animation properties
        self.indicators = []  # List of active indicators
        self.font = pygame.font.SysFont('Arial', 28, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 20, bold=True)
        
        # Colors for quantum effects
        self.tunneling_color = (100, 255, 255)  # Cyan for quantum tunneling
        self.success_color = (0, 255, 100)      # Green for successful tunneling
        self.failure_color = (255, 100, 100)    # Red for failed tunneling
        
        # Particle effects
        self.particles = []
        
    def add_tunneling_activated(self, position):
        """Add indicator when quantum tunneling is activated
        
        Args:
            position: (x, y) position to show the indicator
        """
        indicator = {
            'type': 'activated',
            'position': position,
            'text': 'QUANTUM TUNNELING ACTIVE',
            'color': self.tunneling_color,
            'lifetime': 0,
            'max_lifetime': 90,  # 1.5 seconds at 60 FPS
            'offset_x': 0,
            'offset_y': -10,
            'font': self.small_font,
            'alpha': 255,
            'scale': 1.0
        }
        
        self.indicators.append(indicator)
        self._create_activation_particles(position)
        
    def add_tunneling_success(self, position):
        """Add indicator when quantum tunneling successfully bypasses shield
        
        Args:
            position: (x, y) position to show the indicator
        """
        indicator = {
            'type': 'success',
            'position': position,
            'text': 'TUNNELED THROUGH!',
            'color': self.success_color,
            'lifetime': 0,
            'max_lifetime': 120,  # 2 seconds at 60 FPS
            'offset_x': 0,
            'offset_y': -20,
            'font': self.font,
            'alpha': 255,
            'scale': 1.5,
            'pulse': 0
        }
        
        self.indicators.append(indicator)
        self._create_success_particles(position)
        
    def add_tunneling_failure(self, position):
        """Add indicator when quantum tunneling fails
        
        Args:
            position: (x, y) position to show the indicator
        """
        indicator = {
            'type': 'failure',
            'position': position,
            'text': 'TUNNELING FAILED',
            'color': self.failure_color,
            'lifetime': 0,
            'max_lifetime': 90,  # 1.5 seconds at 60 FPS
            'offset_x': 0,
            'offset_y': -15,
            'font': self.small_font,
            'alpha': 255,
            'scale': 1.0
        }
        
        self.indicators.append(indicator)
        
    def _create_activation_particles(self, position):
        """Create particles for tunneling activation"""
        for _ in range(20):
            particle = {
                'x': position[0] + random.randint(-30, 30),
                'y': position[1] + random.randint(-30, 30),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'size': random.uniform(2, 5),
                'color': self.tunneling_color,
                'lifetime': 0,
                'max_lifetime': 60,
                'type': 'activation'
            }
            self.particles.append(particle)
            
    def _create_success_particles(self, position):
        """Create particles for successful tunneling"""
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            particle = {
                'x': position[0],
                'y': position[1],
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.uniform(3, 8),
                'color': self.success_color,
                'lifetime': 0,
                'max_lifetime': 90,
                'type': 'success'
            }
            self.particles.append(particle)
        
    def update(self):
        """Update all active indicators and particles"""
        # Update indicators
        for indicator in self.indicators[:]:
            indicator['lifetime'] += 1
            
            # Update position (float upward)
            indicator['offset_y'] -= 0.5
            
            # Update alpha (fade out near end)
            progress = indicator['lifetime'] / indicator['max_lifetime']
            if progress > 0.7:
                fade_progress = (progress - 0.7) / 0.3
                indicator['alpha'] = int(255 * (1 - fade_progress))
            
            # Update scale and pulse for success indicators
            if indicator['type'] == 'success':
                indicator['pulse'] += 0.2
                pulse_factor = 1 + 0.2 * math.sin(indicator['pulse'])
                indicator['scale'] = 1.5 * pulse_factor
            
            # Remove if expired
            if indicator['lifetime'] >= indicator['max_lifetime']:
                self.indicators.remove(indicator)
        
        # Update particles
        for particle in self.particles[:]:
            particle['lifetime'] += 1
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Apply gravity to particles
            particle['vy'] += 0.1
            
            # Fade out particles
            progress = particle['lifetime'] / particle['max_lifetime']
            if progress > 0.5:
                fade_progress = (progress - 0.5) / 0.5
                particle['size'] *= 0.98
            
            # Remove if expired
            if particle['lifetime'] >= particle['max_lifetime'] or particle['size'] < 0.5:
                self.particles.remove(particle)
                
    def render(self):
        """Render all active indicators and particles"""
        # Render particles first (behind text)
        for particle in self.particles:
            if particle['size'] > 0.5:
                # Calculate alpha based on lifetime
                progress = particle['lifetime'] / particle['max_lifetime']
                alpha = 255 if progress < 0.5 else int(255 * (1 - (progress - 0.5) / 0.5))
                
                # Create a surface for the particle with alpha
                particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
                color_with_alpha = (*particle['color'], alpha)
                pygame.draw.circle(
                    particle_surface, 
                    color_with_alpha, 
                    (int(particle['size']), int(particle['size'])), 
                    int(particle['size'])
                )
                
                self.screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        # Render text indicators
        for indicator in self.indicators:
            # Calculate position with offset
            x = indicator['position'][0] + indicator['offset_x']
            y = indicator['position'][1] + indicator['offset_y']
            
            # Create text surface
            text_surface = indicator['font'].render(indicator['text'], True, indicator['color'])
            
            # Scale the surface if needed
            if indicator['scale'] != 1.0:
                new_width = int(text_surface.get_width() * indicator['scale'])
                new_height = int(text_surface.get_height() * indicator['scale'])
                text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
            
            # Apply alpha
            text_surface.set_alpha(indicator['alpha'])
            
            # Calculate final position (centered)
            final_x = x - text_surface.get_width() // 2
            final_y = y - text_surface.get_height() // 2
            
            # Add a shadow for readability
            shadow_surface = indicator['font'].render(indicator['text'], True, (0, 0, 0))
            if indicator['scale'] != 1.0:
                shadow_surface = pygame.transform.scale(shadow_surface, (new_width, new_height))
            shadow_surface.set_alpha(indicator['alpha'] // 2)
            
            # Draw shadow slightly offset
            self.screen.blit(shadow_surface, (final_x + 2, final_y + 2))
            
            # Draw the text
            self.screen.blit(text_surface, (final_x, final_y))

    @staticmethod
    def render_static_tunneling_active(screen, character):
        """Render static quantum tunneling indicator for a character that has tunneling active"""
        if not hasattr(character, 'quantum_tunneling_active') or not character.quantum_tunneling_active:
            return
            
        # Character center position
        center = (character.position_to_draw[0], character.position_to_draw[1])
        
        # Draw cyan quantum aura with pulsing effect
        time_factor = pygame.time.get_ticks() * 0.003
        pulse = 0.8 + 0.2 * math.sin(time_factor)
        radius = int(85 * pulse)
        
        # Draw outer quantum field
        pygame.draw.circle(
            screen,
            (100, 255, 255, 100),  # Cyan with transparency
            center,
            radius,
            3
        )
        
        # Draw inner quantum field
        pygame.draw.circle(
            screen,
            (150, 255, 255, 150),  # Brighter cyan
            center,
            radius - 10,
            2
        )
        
        # Draw "Q" text indicator
        font = pygame.font.SysFont('Arial', 18, bold=True)
        text = font.render("Q", True, (100, 255, 255))
        text_rect = text.get_rect(center=(center[0], center[1] - radius - 15))
        
        # Add shadow for readability
        shadow = font.render("Q", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(center[0] + 1, center[1] - radius - 14))
        screen.blit(shadow, shadow_rect)
        screen.blit(text, text_rect)
        
        # Draw quantum particles around character
        for i in range(6):
            angle = time_factor + i * math.pi / 3
            particle_x = center[0] + (radius + 5) * math.cos(angle)
            particle_y = center[1] + (radius + 5) * math.sin(angle)
            
            # Small quantum particles
            particle_size = 3 + int(2 * math.sin(time_factor * 2 + i))
            pygame.draw.circle(
                screen,
                (100, 255, 255),
                (int(particle_x), int(particle_y)),
                particle_size
            ) 