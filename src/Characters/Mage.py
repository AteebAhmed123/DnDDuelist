from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Utils.HealthBar import HealthBar
import pygame
import os

class Mage(CharacterBlueprint):

    standing_sprite_coords = [
            (51,4,78,95),
            (200,4,78,95),
            (352,4,78,95),
            (500,4,78,95),
            (652,4,78,95)
        ]
    
    attacking_sprite_coords = [
        (30,106,100,100),
        (180,106,100,100),
        (340,106,100,100),
        (500,106,100,100),
        (650,106,100,100),
        (47,207,100,100),
        (180,207,100,100),
        (340,207,100,100),
        (500,207,100,100),
        (650,207,100,100)
    ]

    sprite_states = {
        0: standing_sprite_coords,
        1: attacking_sprite_coords
    }

    health_bar_display_offset = 200    

    def __init__(self, screen):
        super().__init__()
        self.SPRITE_PATH = "./Assets/mage_sprite.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_state = 0
        self.animation_tracker = 0
        self.health = HealthBar(100, screen)
        self.screen = screen

    def get_sprites(self):
        return self.sprite_states[self.current_state]

    def motion_animation(self, position_to_draw = None):
        sprite_image = self.sprite_states[self.current_state]

        if self.animation_tracker > len(sprite_image)-1:
            self.animation_tracker = 0
            self.current_state = 0

        animation_to_render = sprite_image[self.animation_tracker]
        sprite_standing_image = self.sprite.get_sprite(animation_to_render)
        sprite_standing_image_position = self.sprite.draw_sprite_image_at(
            sprite_standing_image, 
            position_to_draw)  

        self.animation_tracker = self.animation_tracker + 1
        self.screen.blit(sprite_standing_image, sprite_standing_image_position)
    
    def animate(self, position_to_draw = None):
        self.motion_animation(position_to_draw)
        self.health.animate((position_to_draw[0], 
                             position_to_draw[1] - self.health_bar_display_offset))
    
    def attack(self):
        self.current_state = 1
        self.animation_tracker = 0