from abc import ABC, abstractmethod
from SpriteUtil.SpriteUtil import SpriteUtil
import pygame

class CardBlueprint(ABC):
    def __init__(self, screen):
        """Initialize the card with screen reference"""
        self.screen = screen
        self.sprite = None
        self.dimensions = (145, 200)  # Adjusted card size to match actual rendering
        self.rect = None  # For collision detection

    @abstractmethod
    def get_sprite_coords(self):
        """Return the coordinates for the card sprite"""
        pass

    def render(self, position_to_draw=None):
        """Render the card at the given position"""
        if position_to_draw is None:
            position_to_draw = (0, 0)

        sprite_coords = self.get_sprite_coords()
        sprite_image = self.sprite.get_sprite(sprite_coords)
        
        # Get the actual position where the sprite will be drawn
        actual_position = self.sprite.draw_sprite_image_at(sprite_image, position_to_draw)
        
        # Draw the sprite at the calculated position
        self.screen.blit(sprite_image, actual_position)
        
        # Update the card's rectangle for collision detection using the actual position
        self.rect = pygame.Rect(actual_position[0], actual_position[1], 
                               self.dimensions[0], self.dimensions[1])
                
        return True
        
    def is_clicked(self, mouse_pos):
        """Check if the card was clicked"""
        if self.rect:
            result = self.rect.collidepoint(mouse_pos)
            print(f"Mouse: {mouse_pos}, Card rect: {self.rect}, Result: {result}")
            return result
        return False 