import pygame
import math

class CardPlayedDisplay:
    """Displays a card in the center of the screen when played"""
    
    def __init__(self, screen):
        """Initialize the card display effect
        
        Args:
            screen: The pygame screen to render on
        """
        self.screen = screen
        self.is_active = False
        self.card = None
        self.display_time = 2.0  # seconds to display the card
        self.time_remaining = 0
        self.fade_in_time = 0.3  # seconds for fade in
        self.fade_out_time = 0.5  # seconds for fade out
        
        # Animation properties
        self.scale = 1.8  # Scale for the card when displayed in center (larger to be visible in background)
        self.alpha = 0  # Transparency (0-255)
        self.rotation = 0  # Initial rotation
        self.pulse_amount = 0.05  # Amount to pulse size
        self.pulse_speed = 3  # Speed of pulse
        self.max_alpha = 180  # Maximum alpha (transparency) to keep it in background
        
        # Position properties
        self.position = (0, 0)
        self.target_position = (0, 0)
        
    def start(self, card):
        """Start displaying the card
        
        Args:
            card: The card object to display
        """
        self.card = card
        self.is_active = True
        self.time_remaining = self.display_time
        self.alpha = 0
        self.rotation = -5  # Start with slight rotation
        
        # Calculate center position
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
        self.target_position = (screen_width // 2, screen_height // 2)
        
        # Start position (from the player's hand area)
        self.position = (screen_width // 2, screen_height - 100)
        
    def update(self, dt):
        """Update the card display animation
        
        Args:
            dt: Time delta in seconds
        """
        if not self.is_active or not self.card:
            return
        
        # Update remaining time
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.is_active = False
            return
        
        # Calculate animation phase
        total_time = self.display_time
        phase_time = self.time_remaining / total_time
        
        # Handle fade in
        if phase_time > (total_time - self.fade_in_time) / total_time:
            # Fade in phase
            fade_progress = 1 - (phase_time - (total_time - self.fade_in_time) / total_time) / (self.fade_in_time / total_time)
            self.alpha = int(self.max_alpha * fade_progress)
            
            # Move card from hand to center
            move_progress = fade_progress
            self.position = (
                self.position[0] + (self.target_position[0] - self.position[0]) * move_progress * 0.3,
                self.position[1] + (self.target_position[1] - self.position[1]) * move_progress * 0.3
            )
            
            # Rotate card slightly
            self.rotation = -5 + 5 * fade_progress
            
        # Handle fade out
        elif phase_time < self.fade_out_time / total_time:
            # Fade out phase
            fade_progress = phase_time / (self.fade_out_time / total_time)
            self.alpha = int(self.max_alpha * fade_progress)
            
            # Rotate card away
            self.rotation = 5 * (1 - fade_progress)
            
        else:
            # Steady display phase
            self.alpha = self.max_alpha
            self.position = self.target_position
            self.rotation = 0
            
            # Add subtle pulsing effect
            pulse = math.sin(pygame.time.get_ticks() * 0.005 * self.pulse_speed) * self.pulse_amount
            self.scale = 1.8 + pulse
        
    def render(self):
        """Render the card in the center of the screen"""
        if not self.is_active or not self.card or self.alpha <= 0:
            return
            
        # Get card image
        card_image = self.card.get_card_image()
        if not card_image:
            return
            
        # Create a copy of the image to modify
        card_copy = card_image.copy()
            
        # Scale the image
        original_width, original_height = card_copy.get_width(), card_copy.get_height()
        scaled_width = int(original_width * self.scale)
        scaled_height = int(original_height * self.scale)
        scaled_image = pygame.transform.scale(card_copy, (scaled_width, scaled_height))
        
        # Rotate the image
        if self.rotation != 0:
            scaled_image = pygame.transform.rotate(scaled_image, self.rotation)
            
        # Adjust alpha
        scaled_image.set_alpha(self.alpha)
            
        # Position the image in the center
        image_rect = scaled_image.get_rect(center=self.position)
        
        # Draw the image
        self.screen.blit(scaled_image, image_rect)
        
        # Draw card name with reduced visibility for background effect
        if hasattr(self.card, 'card_name') and self.alpha > 50:
            font = pygame.font.SysFont('Arial', 28, bold=True)
            text_alpha = min(200, int(self.alpha * 1.2))  # Slightly more visible than card
            
            # Create transparent surface for text
            name_text = font.render(self.card.card_name, True, (255, 255, 255))
            text_surface = pygame.Surface(name_text.get_size(), pygame.SRCALPHA)
            text_surface.fill((0, 0, 0, 0))  # Transparent background
            text_surface.blit(name_text, (0, 0))
            text_surface.set_alpha(text_alpha)
            
            # Position and render
            text_rect = name_text.get_rect(center=(self.position[0], self.position[1] + scaled_height//2 + 30))
            self.screen.blit(text_surface, text_rect) 