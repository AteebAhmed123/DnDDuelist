from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Utils.HealthBar import HealthBar
import pygame
import os
from Cards.Deck import Deck
from Cards.Hands import Hand
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

    def __init__(self, screen, position_to_draw):
        super().__init__()
        self.SPRITE_PATH = "./Assets/mage_sprite.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_state = 0
        self.animation_tracker = 0
        self.health = HealthBar(100, screen)
        self.screen = screen
        self.position_to_draw = position_to_draw
        
        # Initialize the mage's deck
        self.deck = Deck(screen)
        self.hand = Hand(screen, self.deck)
        self.card_played = []

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
        self.screen.blit(sprite_standing_image, sprite_standing_image_position)
    
    def animate(self, deck_position, target):
        self.motion_animation()
        self.health.animate((self.position_to_draw[0], 
                             self.position_to_draw[1] - self.health_bar_display_offset))
        self.render_deck(deck_position[0], deck_position[1])
        self.hand.render(deck_position[0], deck_position[1])
        if (self.card_played != []):
            for eachCard in self.card_played:
                playing_card = eachCard.activate_card(self, target)
                if (playing_card == False):
                    self.card_played.remove(eachCard)
    
    def attack(self):
        self.current_state = 1
        self.animation_tracker = 0

    def render_deck(self, center_x, y_position):
        """Render the mage's deck at the specified position"""
        self.deck.render(center_x, y_position)

    def handle_card_click(self, mouse_pos):
        """Handle clicks on cards in the mage's hand"""
        card_index = self.hand.handle_click(mouse_pos)
        if card_index >= 0 and card_index < len(self.hand.cards_in_hand):
            self.card_played.append(self.hand.cards_in_hand[card_index])
            self.hand.remove_card(card_index)
            if (len(self.deck.cards_in_deck) > 0):
                self.hand.add_card(self.deck.draw_card_from_deck(1)[0])

    def play_card(self, card):
        pass

    # def handle_card_click(self, mouse_pos):
    #     """Handle clicks on cards in the mage's hand"""
    #     card_index = self.hand.handle_click(mouse_pos)
    #     if card_index >= 0:
    #         activated_card =self.hand.remove_card(card_index)
    #         if (len(self.deck.cards_in_deck) > 0):
    #             self.hand.add_card(self.deck.draw_card_from_deck(1)[0])
            
    #         activated_card.enable_card_played()
    

