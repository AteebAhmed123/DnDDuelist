import pygame
from pygame.sprite import Sprite
from SpriteUtil.SpriteUtil import SpriteUtil
from Effects.DamageIndicator import DamageIndicator

class HealthBar(SpriteUtil):

    HEALTH_BAR_BACKGROUND_DIMENSION = [
        106,
        62,
        508,
        487
    ]

    SPRITE_HEALTH_BACKGROUND_PATH = "./Assets/Health/health.png"

    def __init__(self, health, screen):
        self.sprite_health_background = SpriteUtil(self.SPRITE_HEALTH_BACKGROUND_PATH) 
        self.screen = screen
        self.health = health
        self.animated_health_background = False
        self.last_health = health  # Track previous health value
        self.damage_indicator = None  # Will be set by GameManager
        self.position = (0, 0)  # Current position

    def set_damage_indicator(self, damage_indicator):
        """Set the damage indicator for this health bar"""
        self.damage_indicator = damage_indicator

    def reduce_health(self, amount):
        """Reduce health and show damage indicator"""
        old_health = self.health
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
        # Show damage indicator if available
        if self.damage_indicator and amount > 0:
            self.damage_indicator.add_damage_number(
                position=(self.position[0] + 20, self.position[1] - 30),
                amount=amount,
                is_heal=False
            )
            
            # Trigger damage flash if character has one
            if hasattr(self, 'character') and hasattr(self.character, 'trigger_damage_flash'):
                self.character.trigger_damage_flash()
            
        return old_health - self.health  # Return actual damage dealt

    def increase_health(self, amount):
        """Increase health and show healing indicator"""
        old_health = self.health
        self.health += amount
        if self.health > 100:
            self.health = 100
            
        # Show healing indicator if available
        if self.damage_indicator and amount > 0:
            self.damage_indicator.add_damage_number(
                position=(self.position[0] + 20, self.position[1] - 30),
                amount=amount,
                is_heal=True
            )
            
        return self.health - old_health  # Return actual healing done
    
    def animate_health_background(self, position_to_draw = None):
        if self.animated_health_background:
           return 
        sprite_health = self.sprite_health_background.get_sprite(self.HEALTH_BAR_BACKGROUND_DIMENSION)
        if position_to_draw is None:
            position_to_draw = (0,0)

        sprite_health = pygame.transform.scale(sprite_health, (40,40))
        coords_to_draw = self.sprite_health_background.draw_sprite_image_at(sprite_health, position_to_draw)
        self.screen.blit(sprite_health, coords_to_draw) 


    def animate_health_number(self, position_to_draw = None):
        if position_to_draw is None:
            position_to_draw = (0,0)
            
        health_font = pygame.font.SysFont('Arial', 24)
        health_text = health_font.render(f'{self.health}', True, (255, 0, 0))        
        text_position = (position_to_draw[0] + 30, position_to_draw[1] - 15)        
        self.screen.blit(health_text, text_position)

    def animate(self, position_to_draw = None):
        self.position = position_to_draw if position_to_draw else self.position
        self.animate_health_background(position_to_draw)
        self.animate_health_number(position_to_draw)
