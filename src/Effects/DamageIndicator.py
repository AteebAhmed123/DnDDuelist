import pygame
import random
import math

class DamageIndicator:
    """Visual indicator for damage taken by characters"""
    
    def __init__(self, screen):
        """Initialize the damage indicator
        
        Args:
            screen: The pygame screen to render on
        """
        self.screen = screen
        
        # Animation properties
        self.indicators = []  # List of active damage indicators
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Colors
        self.damage_color = (255, 50, 50)  # Red for damage
        self.heal_color = (50, 255, 50)    # Green for healing
        
    def add_damage_number(self, position, amount, is_heal=False):
        """Add a new damage number indicator
        
        Args:
            position: (x, y) position to show the indicator
            amount: Amount of damage/healing to display
            is_heal: True if this is healing, False if damage
        """
        # Create a new indicator
        indicator = {
            'position': position,
            'amount': amount,
            'color': self.heal_color if is_heal else self.damage_color,
            'lifetime': 0,
            'max_lifetime': 60,  # Frames the indicator will last
            'offset_x': random.randint(-20, 20),  # Random horizontal drift
            'offset_y': -5,  # Initial upward movement
            'font': self.font if amount >= 10 else self.small_font,  # Bigger font for bigger numbers
            'is_critical': random.random() < 0.2,  # 20% chance of critical hit effect
            'is_heal': is_heal  # Store whether this is healing or damage
        }
        
        self.indicators.append(indicator)
        
    def update(self):
        """Update all active damage indicators"""
        # Update each indicator
        for indicator in self.indicators[:]:  # Use a copy for safe removal
            # Update lifetime
            indicator['lifetime'] += 1
            
            # Update position (float upward and drift)
            indicator['offset_y'] -= 1  # Move upward
            
            # Remove if expired
            if indicator['lifetime'] >= indicator['max_lifetime']:
                self.indicators.remove(indicator)
                
    def render(self):
        """Render all active damage indicators"""
        for indicator in self.indicators:
            # Calculate position with offset
            x = indicator['position'][0] + indicator['offset_x']
            y = indicator['position'][1] + indicator['offset_y'] - indicator['lifetime']
            
            # Calculate alpha (fade out near end of lifetime)
            progress = indicator['lifetime'] / indicator['max_lifetime']
            alpha = 255 if progress < 0.7 else int(255 * (1 - (progress - 0.7) / 0.3))
            
            # Calculate scale (start big, then shrink slightly)
            scale = 1.5 - (0.5 * progress)
            if indicator['is_critical']:
                scale *= 1.3  # Make critical hits bigger
            
            # Create text with appropriate prefix
            prefix = "+" if indicator['is_heal'] else "-"
            text = f"{prefix}{indicator['amount']}"
            
            # Render text with current alpha
            color = indicator['color']
            
            # Create text surface
            text_surface = indicator['font'].render(text, True, color)
            
            # Scale the surface if needed
            if scale != 1.0:
                new_width = int(text_surface.get_width() * scale)
                new_height = int(text_surface.get_height() * scale)
                text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
            
            # Calculate final position (centered on the original point)
            final_x = x - text_surface.get_width() // 2
            final_y = y - text_surface.get_height() // 2
            
            # Add a subtle shadow for readability
            shadow_surface = indicator['font'].render(text, True, (0, 0, 0))
            if scale != 1.0:
                shadow_surface = pygame.transform.scale(shadow_surface, (new_width, new_height))
            
            # Draw shadow slightly offset
            self.screen.blit(shadow_surface, (final_x + 2, final_y + 2))
            
            # Draw the text
            self.screen.blit(text_surface, (final_x, final_y)) 