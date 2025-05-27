from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Utils.HealthBar import HealthBar
import pygame
import os
from Cards.Deck import Deck
from Cards.Hands import Hand
from Spells.Barrier import StaticBarrierShield
from Spells.BacklashSurge import StaticVulnerabilityEffect
from Cards.ElementalDeck import ElementalDeck
from Cards.ElementalWeather import ElementalWeather
from Spells.ElementalWeather.WeatherSpells import WeatherSpells

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
        self.health = HealthBar(20, 20, screen)
        self.health.character = self  # Set reference to character
        self.screen = screen
        self.position_to_draw = position_to_draw
        
        # Initialize the wizard's deck
        self.deck = Deck(screen)
        self.elementDeck = ElementalDeck(screen)
        self.hand = Hand(screen, self.deck)
        self.card_played = []
        self.shield = False
        self.self_damage_multiplier = 1.0
        self.damage_over_turn = None
        self.damage_over_turn_applied = False
        self.turn_tracker = None

        # Damage flash effect
        self.damage_flash = None
        self.character_id = "Wizard"  # Unique ID for this character
        
        # Card display effect
        self.card_display = None

    def get_sprites(self):
        return self.sprite_states[self.current_state]

    def motion_animation(self):
        self.render_shield()
        self.render_vulnerable()
        sprite_image = self.sprite_states[self.current_state]

        if self.animation_tracker > len(sprite_image)-1:
            self.animation_tracker = 0
            self.current_state = 0

        animation_to_render = sprite_image[self.animation_tracker]
        sprite_standing_image = self.sprite.get_sprite(animation_to_render)
        
        # Apply damage flash effect if active
        if self.damage_flash:
            sprite_standing_image = self.damage_flash.apply_flash(
                self.character_id, sprite_standing_image)
                
        sprite_standing_image_position = self.sprite.draw_sprite_image_at(
            sprite_standing_image, 
            self.position_to_draw)  

        self.animation_tracker = self.animation_tracker + 1
        self.screen.blit(pygame.transform.flip(sprite_standing_image, True, False), sprite_standing_image_position)

    def animate(self, deck_position, target, turn, weather_manager):
        self.motion_animation()
        if self.turn_tracker != turn:
            print(self, self.turn_tracker, turn)
            if self.damage_over_turn is not None and not self.damage_over_turn_applied:
                self.damage_over_turn.apply_damage(self, weather_manager)
            self.turn_tracker = turn
        self.health.animate((self.position_to_draw[0], 
                             self.position_to_draw[1] - self.health_bar_display_offset))
        if turn:
            self.render_deck(deck_position[0], deck_position[1])
            self.elementDeck.render(deck_position[0], deck_position[1])
            self.hand.render(deck_position[0], deck_position[1])
            if (self.card_played != []):
                for eachCard in self.card_played:
                    playing_card = eachCard.activate_card(self, target)
                    if (isinstance(playing_card, WeatherSpells)):
                        weather_manager.set_active_weather(playing_card, 3)
                        self.card_played.remove(eachCard)
                        self.damage_over_turn_applied = False
                        return False

                    if (playing_card == False):
                        self.card_played.remove(eachCard)
                        self.damage_over_turn_applied = False
                        return False
        return True

    def set_damage_flash(self, damage_flash):
        """Set the damage flash effect for this character"""
        self.damage_flash = damage_flash
    
    def trigger_damage_flash(self):
        """Trigger the damage flash effect"""
        if self.damage_flash:
            self.damage_flash.start_flash(self.character_id)
    
    def attack(self):
        self.current_state = 1
        self.animation_tracker = 0

    def handle_card_click(self, mouse_pos):
        """Handle clicks on cards in the wizard's hand"""
        self.current_state = 1
        self.animation_tracker = 0
        card_index = self.hand.handle_click(mouse_pos)
        if card_index >= 0 and card_index < len(self.hand.cards_in_hand):
            selected_card = self.hand.cards_in_hand[card_index]
            
            # Display the card if we have a card display effect
            if self.card_display:
                self.card_display.start(selected_card)
            
            self.hand.remove_card(card_index)
            self.card_played.append(selected_card)
            if (len(self.deck.cards_in_deck) > 0):
                print("Activating card", type(selected_card))
                self.hand.add_card(self.deck.draw_card_from_deck(1)[0])

    def render_deck(self, center_x, y_position):
        """Render the mage's deck at the specified position"""
        self.deck.render(center_x, y_position)

    def render_shield(self):
        """Render the shield for this character"""
        if self.shield:
            StaticBarrierShield.render_static_shield(self.screen, self)

    def render_vulnerable(self):
        """Render the vulnerable for this character"""
        if self.self_damage_multiplier > 1.0:
            print("self.self_damage_multiplier Wizard", self.self_damage_multiplier)
            StaticVulnerabilityEffect.render_static_vulnerable(self.screen, self)

    def set_card_display(self, card_display):
        """Set the card display effect for this character"""
        self.card_display = card_display
    # def draw_new_hand(self):
    #     """Draw a new hand from the deck"""
    #     self.deck.draw_hand()