from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Utils.HealthBar import HealthBar
from Cards.Deck import Deck
from Cards.Hands import Hand
from Spells.Barrier import StaticBarrierShield
from Spells.BacklashSurge import StaticVulnerabilityEffect
from Cards.ElementalDeck import ElementalDeck

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
        self.health = HealthBar(20, 20, screen)
        self.elementDeck = ElementalDeck(screen)
        self.health.character = self  # Set reference to character
        self.screen = screen
        self.position_to_draw = position_to_draw
        
        # Initialize the mage's deck
        self.deck = Deck(screen)
        self.hand = Hand(screen, self.deck)
        self.card_played = []
        self.shield = False
        self.self_damage_multiplier = 1.0
        
        # Damage flash effect
        self.damage_flash = None
        self.character_id = "Mage"  # Unique ID for this character
        
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
        self.screen.blit(sprite_standing_image, sprite_standing_image_position)
    
    def animate(self, deck_position, target, turn):
        self.motion_animation()
        self.health.animate((self.position_to_draw[0], 
                             self.position_to_draw[1] - self.health_bar_display_offset))
        if turn:
            self.render_deck(deck_position[0], deck_position[1])
            self.elementDeck.render(deck_position[0], deck_position[1])
            self.hand.render(deck_position[0], deck_position[1])
            if (self.card_played != []):
                for eachCard in self.card_played:
                    playing_card = eachCard.activate_card(self, target)
                    if (playing_card == False):
                        self.card_played.remove(eachCard)
                        return False
        return True
    
    def attack(self):
        self.current_state = 1
        self.animation_tracker = 0

    def render_deck(self, center_x, y_position):
        """Render the mage's deck at the specified position"""
        self.deck.render(center_x, y_position)

    def handle_card_click(self, mouse_pos):
        """Handle clicks on cards in the mage's hand"""
        self.current_state = 1
        self.animation_tracker = 0
        card_index = self.hand.handle_click(mouse_pos)
        if card_index >= 0 and card_index < len(self.hand.cards_in_hand):
            selected_card = self.hand.cards_in_hand[card_index]
            
            # Display the card if we have a card display effect
            if self.card_display:
                self.card_display.start(selected_card)
            
            # Add to played cards
            self.card_played.append(selected_card)
            
            # Remove from hand and draw a new card if available
            self.hand.remove_card(card_index)
            if (len(self.deck.cards_in_deck) > 0):
                self.hand.add_card(self.deck.draw_card_from_deck(1)[0])

    def play_card(self, card):
        pass

    def set_damage_flash(self, damage_flash):
        """Set the damage flash effect for this character"""
        self.damage_flash = damage_flash
    
    def set_card_display(self, card_display):
        """Set the card display effect for this character"""
        self.card_display = card_display
    
    def trigger_damage_flash(self):
        """Trigger the damage flash effect"""
        if self.damage_flash:
            self.damage_flash.start_flash(self.character_id)

    def render_shield(self):
        """Render the shield for this character"""
        if self.shield:
            StaticBarrierShield.render_static_shield(self.screen, self)
    
    def render_vulnerable(self):
        """Render the vulnerable for this character"""
        if self.self_damage_multiplier > 1.0:
            print("self.self_damage_multiplier Mage", self.self_damage_multiplier)
            StaticVulnerabilityEffect.render_static_vulnerable(self.screen, self)

