from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Utils.HealthBar import HealthBar
import pygame
import os
from Cards.Deck import Deck

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

    health_bar_display_offset = 220    

    def __init__(self, screen):
        super().__init__()
        self.SPRITE_PATH = "./Assets/mage_sprite.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_state = 0
        self.animation_tracker = 0
        self.health = HealthBar(100, screen)
        self.screen = screen
        
        # Initialize the mage's deck
        self.deck = Deck(screen)
        self.deck.draw_hand()

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
    
    def animate(self, position_to_draw = None, deck_position = None):
        self.motion_animation(position_to_draw)
        self.health.animate((position_to_draw[0], 
                             position_to_draw[1] - self.health_bar_display_offset))
        self.render_deck(deck_position[0], deck_position[1])
        
    
    def attack(self):
        self.current_state = 1
        self.animation_tracker = 0

    def render_deck(self, center_x, y_position):
        """Render the mage's deck at the specified position"""
        self.deck.render(center_x, y_position)
        
    def draw_new_hand(self):
        """Draw a new hand from the deck"""
        self.deck.draw_hand()

    def handle_card_click(self, mouse_pos):
        """Handle clicks on cards in the mage's hand"""
        card_index = self.deck.hand.handle_click(mouse_pos)
        if card_index >= 0:
            # Remove the clicked card
            self.deck.hand.remove_card(card_index)
            # Draw a new card if available
            # if len(self.deck.cards) > 0:
            #     self.deck.hand.add_card(self.deck.cards.pop(0))