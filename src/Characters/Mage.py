from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Utils.HealthBar import HealthBar
from Cards.Deck import Deck
from Cards.Hands import Hand
from Spells.Barrier import StaticBarrierShield
from Spells.BacklashSurge import StaticVulnerabilityEffect
from Cards.ElementalDeck import ElementalDeck
from Cards.ElementalWeather import ElementalWeather
from Cards.PhaseBias import PhaseBias
from Cards.QuantumTunneling import QuantumTunneling
from Spells.ElementalWeather.WeatherSpells import WeatherSpells
from Cards.ElementalAfflication import ElementalAfflication
from WeatherManager import WeatherType
from Cards.ElementalAttacksCards.WaterGeyserCard import WaterGeyserCard
from Cards.ElementalAttacksCards.WindTornadoCard import WindTornadoCard
from Cards.ElementalAttacksCards.BurningHandsCard import BurningHandCard
from Cards.ElementalAttacksCards.EarthSpikeCard import EarthSpikeCard
from Effects.QuantumTunnelingIndicator import QuantumTunnelingIndicator

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
        self.health = HealthBar(100, 100, screen)
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
        self.damage_over_turn = None
        self.damage_over_turn_applied = False
        self.turn_tracker = None
        # Damage flash effect
        self.damage_flash = None
        self.character_id = "Mage"  # Unique ID for this character
        
        # Card display effect
        self.card_display = None
        
        # Phase bias manager
        self.phase_bias_manager = None
        
        # Quantum tunneling properties
        self.quantum_tunneling_active = False
        self.tunneling_probability = 0.0

    def get_sprites(self):
        return self.sprite_states[self.current_state]

    def motion_animation(self):
        self.render_shield()
        self.render_vulnerable()
        self.render_quantum_tunneling()

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
    
    def animate(self, deck_position, target, turn, weather_manager):
        self.motion_animation()
        if self.turn_tracker != turn:
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
                    playing_card, accompany_card = eachCard.activate_card(self, target)

                    if (isinstance(playing_card, WeatherSpells)):
                        weather_manager.set_active_weather(playing_card, 3)
                        self.card_played.remove(eachCard)
                        self.damage_over_turn_applied = False
                        if (accompany_card != None):
                            for eachCard in range(0,len(self.hand.cards_in_hand)):
                                if (type(self.hand.cards_in_hand[eachCard]) == ElementalAfflication):
                                    if (weather_manager.weather_type == WeatherType.RAIN):
                                        self.hand.cards_in_hand[eachCard] = WaterGeyserCard(self.screen)
                                    elif (weather_manager.weather_type == WeatherType.WIND):
                                        self.hand.cards_in_hand[eachCard] = WindTornadoCard(self.screen)
                                    elif (weather_manager.weather_type == WeatherType.HEAT):
                                        self.hand.cards_in_hand[eachCard] = BurningHandCard(self.screen)
                                    elif (weather_manager.weather_type == WeatherType.EARTH):
                                        self.hand.cards_in_hand[eachCard] = EarthSpikeCard(self.screen)
                        return False

                    if (playing_card == False):
                        self.card_played.remove(eachCard)
                        if (accompany_card != None):
                            weather_manager.set_active_weather(accompany_card.spell, 3)
                            for eachCard in range(0,len(self.hand.cards_in_hand)):
                                print("found elemental afflication",eachCard, weather_manager.weather_type, type(self.hand.cards_in_hand[eachCard]))
                                if (weather_manager.weather_type == WeatherType.RAIN):
                                    self.hand.cards_in_hand[eachCard] = WaterGeyserCard(self.screen)
                                elif (weather_manager.weather_type == WeatherType.WIND):
                                    self.hand.cards_in_hand[eachCard] = WindTornadoCard(self.screen)
                                elif (weather_manager.weather_type == WeatherType.HEAT):
                                    self.hand.cards_in_hand[eachCard] = BurningHandCard(self.screen)
                                elif (weather_manager.weather_type == WeatherType.EARTH):
                                    self.hand.cards_in_hand[eachCard] = EarthSpikeCard(self.screen)

                        self.damage_over_turn_applied = False
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
        deck_click = self.elementDeck.handle_click(mouse_pos)
        
        # Check if ElementalDeck was clicked
        if deck_click is not None:
            elemental_weather = ElementalWeather(self.screen)
            self.card_display.start(elemental_weather)
            self.card_played.append(elemental_weather)
            return deck_click  # Return the ElementalWeather card
        
        if card_index >= 0 and card_index < len(self.hand.cards_in_hand):
            selected_card = self.hand.cards_in_hand[card_index]
            
            # Check if it's a Phase Bias card
            if isinstance(selected_card, PhaseBias):
                # Start Phase Bias targeting
                if self.phase_bias_manager:
                    targeting_success = self.phase_bias_manager.start_targeting(selected_card, self.hand.cards_in_hand)
                    if targeting_success:
                        # Remove the Phase Bias card from hand only if targeting started successfully
                        self.hand.remove_card(card_index)
                        if (len(self.deck.cards_in_deck) > 0):
                            self.hand.add_card(self.deck.draw_card_from_deck(1)[0])
                    else:
                        # Targeting failed (no valid targets), show a message or just do nothing
                        # The card remains in hand
                        pass
                return None
            
            # Display the card if we have a card display effect
            if self.card_display:
                self.card_display.start(selected_card)
            
            self.hand.remove_card(card_index)
            self.card_played.append(selected_card)            
            if (len(self.deck.cards_in_deck) > 0):
                self.hand.add_card(self.deck.draw_card_from_deck(1)[0])
        
        return None

    def play_card(self, card):
        pass

    def set_damage_flash(self, damage_flash):
        """Set the damage flash effect for this character"""
        self.damage_flash = damage_flash
    
    def set_card_display(self, card_display):
        """Set the card display effect for this character"""
        self.card_display = card_display
    
    def set_phase_bias_manager(self, phase_bias_manager):
        """Set the phase bias manager for this character"""
        self.phase_bias_manager = phase_bias_manager

    def set_quantum_tunneling_indicator(self, quantum_tunneling_indicator):
        """Set the quantum tunneling indicator for this character"""
        self.quantum_tunneling_indicator = quantum_tunneling_indicator

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
            StaticVulnerabilityEffect.render_static_vulnerable(self.screen, self)

    def render_quantum_tunneling(self):
        """Render the quantum tunneling indicator for this character"""
        QuantumTunnelingIndicator.render_static_tunneling_active(self.screen, self)

