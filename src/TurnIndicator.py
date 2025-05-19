import pygame
import math

class TurnIndicator:
    """Visual indicator for turn transitions"""
    
    def __init__(self, screen):
        """Initialize the turn indicator
        
        Args:
            screen: The pygame screen to render on
        """
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Animation properties
        self.is_active = False
        self.animation_progress = 0.0
        self.animation_speed = 0.20  # Speed of transition animation
        self.max_alpha = 180  # Maximum transparency (0-255)
        
        # Text properties
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        # Create surfaces
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
    def start_transition(self, next_player_name):
        """Start the turn transition animation
        
        Args:
            next_player_name: Name of the player whose turn is starting
        """
        self.is_active = True
        self.animation_progress = 0.0
        self.next_player = next_player_name
        
    def update(self):
        """Update the animation state
        
        Returns:
            True if animation is still active, False when complete
        """
        if not self.is_active:
            return False
            
        # Update animation progress
        self.animation_progress += self.animation_speed
        
        # Check if animation is complete
        if self.animation_progress >= 2.0:
            self.is_active = False
            return False
            
        return True
        
    def render(self):
        """Render the turn transition effect"""
        if not self.is_active:
            return
            
        # Calculate alpha based on animation progress
        # Fade in from 0 to 1, then fade out from 1 to 2
        if self.animation_progress < 1.0:
            # Fade in
            alpha = int(self.max_alpha * self.animation_progress)
        else:
            # Fade out
            alpha = int(self.max_alpha * (2.0 - self.animation_progress))
        
        # Fill overlay with semi-transparent black
        self.overlay.fill((0, 0, 0, alpha))
        
        # Render turn text
        turn_text = f"{self.next_player}'s Turn"
        
        # Create text surfaces
        turn_surface = self.font_large.render(turn_text, True, (255, 255, 255))
        instruction_surface = self.font_small.render("Select a card to play", True, (200, 200, 200))
        
        # Calculate positions
        turn_pos = (self.width // 2 - turn_surface.get_width() // 2, 
                   self.height // 2 - turn_surface.get_height() // 2)
        instruction_pos = (self.width // 2 - instruction_surface.get_width() // 2,
                          turn_pos[1] + turn_surface.get_height() + 20)
        
        # Draw text on overlay
        self.overlay.blit(turn_surface, turn_pos)
        self.overlay.blit(instruction_surface, instruction_pos)
        
        # Draw overlay on screen
        self.screen.blit(self.overlay, (0, 0)) 