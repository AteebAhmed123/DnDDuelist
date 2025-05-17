from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Utils.HealthBar import HealthBar
import pygame
import os
from Cards.Deck import Deck

class Wizard(CharacterBlueprint):

    # Adjusted sprite coordinates to ensure full sprite is captured
    standing_sprite_coords = [
            (47,2,86,95),
            (209,2,86,95),
            (370,2,86,95),
            (530,2,86,95)]
    
    attacking_sprite_coords = [
        (27,421,130,100),
        (187,421,130,100),
        (347,421,130,100),
        (482,421,130,100),
        (650,421,130,100),
        (800,421,130,100),
        (0,530,130,100),
        (180,530,130,100)
    ]

    sprite_states = {
        0: standing_sprite_coords,
        1: attacking_sprite_coords
    }

    health_bar_display_offset = 220

    def __init__(self, screen, position_to_draw):
        super().__init__()
        self.SPRITE_PATH = "./Assets/wizard_sprite.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_state = 0
        self.animation_tracker = 0
        self.health = HealthBar(100, screen)
        self.screen = screen
        self.position_to_draw = position_to_draw
        
        # Initialize the wizard's deck
        # self.deck = Deck(screen)
        # self.hand = Hand(screen, self.deck)
        # self.deck.draw_hand()

    def get_sprites(self):
        return self.sprite_states[self.current_state]

    def motion_animation(self):
        sprite_image = self.sprite_states[self.current_state]

        if self.animation_tracker > len(sprite_image)-1:
            self.animation_tracker = 0
            self.current_state = 0

        animation_to_render = sprite_image[self.animation_tracker]
        sprite_standing_image = self.sprite.get_sprite(animation_to_render)
        sprite_standing_image_position = self.sprite.draw_sprite_image_at(
            sprite_standing_image, 
            self.position_to_draw)  

        self.animation_tracker = self.animation_tracker + 1
        self.screen.blit(pygame.transform.flip(sprite_standing_image, True, False), sprite_standing_image_position)

    def animate(self, deck_position):
        self.motion_animation()
        self.health.animate((self.position_to_draw[0], 
                             self.position_to_draw[1] - self.health_bar_display_offset))
        # self.render_deck(deck_position[0], deck_position[1])

    
    def attack(self):
        self.current_state = 1
        self.animation_tracker = 0
        
    def render_deck(self, center_x, y_position):
        """Render the wizard's deck at the specified position"""
        self.deck.render(center_x, y_position)
        
    # def draw_new_hand(self):
    #     """Draw a new hand from the deck"""
    #     self.deck.draw_hand()