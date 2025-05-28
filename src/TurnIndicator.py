import pygame
import math
from SpriteUtil.SpriteUtil import SpriteUtil

class TurnIndicator:
    """Visual indicator for turn transitions"""

    animation_frames = [
        (41, 64, 220, 196),
        (41, 364, 220, 196),
        (41, 664, 220, 196),
        (41, 964, 220, 196),
        (41, 1264, 220, 196),
        (41, 64, 220, 196)
    ]


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
        self.animation_speed = 0.07  # Speed of transition animation
        self.max_alpha = 180  # Maximum transparency (0-255)
        
        # Text properties
        self.font_large = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        # Create surfaces
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.SPRITE_PATH = "./Assets/turn_indicator.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_state = 0
        self.animation_tracker = 0
        self.total_turns = 0
        
        
    def start_transition(self, next_player):
        """Start the turn transition animation
        
        Args:
            next_player_name: Name of the player whose turn is starting
        """
        self.is_active = True
        self.animation_progress = 0.0
        self.next_player = next_player
        self.total_turns = self.total_turns + 1

    def get_current_turn(self):
        return self.total_turns

    def update(self):
        """Update the animation state
        
        Returns:
            True if animation is still active, False when complete
        """
        # print("turn_indicator_update", self.total_turns)
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
        if self.next_player.character_id == "Wizard":
            self.render_turn_indicator(self.next_player.position_to_draw)
        else:
            self.render_turn_indicator(self.next_player.position_to_draw)

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
        turn_text = f"{self.next_player.character_id}'s Turn"
        
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

    def render_turn_indicator(self, turn_indicator_position):
        """Render the turn indicator"""
        turn_indicator_position = (turn_indicator_position[0], turn_indicator_position[1] - 100)
        if self.animation_tracker > len(self.animation_frames)-1:
            self.animation_tracker = 0

        animation_to_render = self.animation_frames[self.animation_tracker]
        sprite_standing_image = self.sprite.get_sprite(animation_to_render)

        
        scaled_sprite_image = pygame.transform.scale(sprite_standing_image, (50, 50))
        sprite_standing_image_position = self.sprite.draw_sprite_image_at(
            scaled_sprite_image, 
            turn_indicator_position)  

        self.animation_tracker = self.animation_tracker + 1

        self.screen.blit(scaled_sprite_image, sprite_standing_image_position)