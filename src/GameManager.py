import pygame
import sys
from Characters.Mage import Mage
from Characters.Wizard import Wizard
from Utils.HealthBar import HealthBar
from pygame.sprite import LayeredUpdates
import random
from TurnIndicator import TurnIndicator
from Effects.DamageIndicator import DamageIndicator
from Effects.DamageFlash import DamageFlash
from Effects.GameOver import GameOver
from Effects.CardPlayedDisplay import CardPlayedDisplay
from Effects.QuantumTunnelingIndicator import QuantumTunnelingIndicator
from Spells.ElementalWeather.Rain import Rain
from Spells.ElementalWeather.WindTornado import WindTornado
from Spells.ElementalWeather.Heatwave import HeatWave
from Spells.ElementalWeather.Earthquake import Earthquake
from Cards.ElementalWeather import ElementalWeather
from Cards.ElementalAfflication import ElementalAfflication
from Cards.PhaseBias import PhaseBias
from Spells.ElementalWeather.WeatherSpells import WeatherSpells
from WeatherManager import WeatherManager
from Utils.PhaseBiasManager import PhaseBiasManager

class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 700
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Initialize effects
        self.turn_indicator = TurnIndicator(self.screen)
        self.damage_indicator = DamageIndicator(self.screen)
        self.damage_flash = DamageFlash()
        self.game_over = GameOver(self.screen)
        self.card_display = CardPlayedDisplay(self.screen)
        self.phase_bias_manager = PhaseBiasManager(self.screen)
        self.quantum_tunneling_indicator = QuantumTunnelingIndicator(self.screen)
        
        # Initialize characters
        self.wizard = Wizard(self.screen, (180,320))
        self.mage = Mage(self.screen, (900,320))
        self.weather_manager = WeatherManager(self.turn_indicator)

        # Set damage indicators for health bars
        self.mage.health.set_damage_indicator(self.damage_indicator)
        self.wizard.health.set_damage_indicator(self.damage_indicator)
        
        # Set damage flash effect
        self.mage.set_damage_flash(self.damage_flash)
        self.wizard.set_damage_flash(self.damage_flash)
        
        # Set card display effect
        self.mage.set_card_display(self.card_display)
        self.wizard.set_card_display(self.card_display)
        
        # Set phase bias manager
        self.mage.set_phase_bias_manager(self.phase_bias_manager)
        self.wizard.set_phase_bias_manager(self.phase_bias_manager)
        
        # Set quantum tunneling indicator
        self.mage.set_quantum_tunneling_indicator(self.quantum_tunneling_indicator)
        self.wizard.set_quantum_tunneling_indicator(self.quantum_tunneling_indicator)
        
        # Turn counter
        self.turn_counter = 1
        
        # Clock for timing
        self.clock = pygame.time.Clock()
        self.dt = 0  # Time delta between frames

    def setup_display(self):
        background = pygame.image.load("./Assets/image.png")
        background = pygame.transform.scale(background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        return background
    
    def reset_game(self):
        """Reset the game state for a new game"""
        # Reset game over state
        self.game_over.reset()
        
        # Reinitialize characters 
        self.wizard = Wizard(self.screen, (180,320))
        self.mage = Mage(self.screen, (900,320))
        
        # Set damage indicators for health bars
        self.mage.health.set_damage_indicator(self.damage_indicator)
        self.wizard.health.set_damage_indicator(self.damage_indicator)
        
        # Set damage flash effect
        self.mage.set_damage_flash(self.damage_flash)
        self.wizard.set_damage_flash(self.damage_flash)
        
        # Set card display effect
        self.mage.set_card_display(self.card_display)
        self.wizard.set_card_display(self.card_display)
        
        # Set phase bias manager
        self.mage.set_phase_bias_manager(self.phase_bias_manager)
        self.wizard.set_phase_bias_manager(self.phase_bias_manager)
        
        # Set quantum tunneling indicator
        self.mage.set_quantum_tunneling_indicator(self.quantum_tunneling_indicator)
        self.wizard.set_quantum_tunneling_indicator(self.quantum_tunneling_indicator)
        
        # Reset turn counter
        self.turn_counter = 1
    
    def start_game(self):
        clock = pygame.time.Clock()
        game_assets = self.setup_display()
        running = True
        initiative = random.randint(0,1)
        mage_turn = False
        wizard_turn = True
        
        # Show initial turn indicator
        current_player = self.wizard if wizard_turn else self.mage
        self.turn_indicator.start_transition(current_player)
        while running:
            # Calculate time delta for animations
            self.dt = clock.get_time() / 1000.0  # Convert to seconds
            for event in pygame.event.get():
                # Handle Phase Bias Manager clicks first (highest priority)
                if self.phase_bias_manager.is_active and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.phase_bias_manager.handle_click(pygame.mouse.get_pos()):
                        continue  # Phase Bias Manager handled the click
                
                # Only process events if turn indicator is not active and game is not over and phase bias is not active
                if (not self.turn_indicator.is_active and 
                    not self.game_over.is_game_over and 
                    not self.card_display.is_active and 
                    not self.phase_bias_manager.is_active):
                    running = self.handle_events(event, mage_turn, wizard_turn)
                # Handle game over screen clicks
                elif self.game_over.is_game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.game_over.handle_click(pygame.mouse.get_pos())
                    if action == "restart":
                        self.reset_game()
                        mage_turn = False
                        wizard_turn = True
                        self.turn_indicator.start_transition(self.wizard)
                    elif action == "quit":
                        running = False
                # Handle event when game is in any state
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Cancel Phase Bias if active
                    if self.phase_bias_manager.is_active:
                        self.phase_bias_manager.cancel()
                    else:
                        running = False
            
            # Draw background
            self.screen.blit(game_assets, (0, 0))
            self.weather_manager.animate_weather()
            # wind.animate_spell()
            # Update effects
            self.damage_indicator.update()
            self.damage_flash.update()
            self.card_display.update(self.dt)
            self.quantum_tunneling_indicator.update()
            
            # Render card display (in background, before characters)
            self.card_display.render()
            
            # Draw turn counter
            font = pygame.font.SysFont('Arial', 24)
            turn_text = font.render(f"Turn {self.turn_counter}", True, (255, 255, 255))
            self.screen.blit(turn_text, (20, 20))
            
            # Draw current player indicator if game not over
            if not self.game_over.is_game_over:
                current_player = "Wizard's Turn" if wizard_turn else "Mage's Turn"
                player_text = font.render(current_player, True, (255, 255, 255))
                self.screen.blit(player_text, (20, 50))
            
            # Animate characters
            mage_card_x = self.SCREEN_WIDTH // 2 - 350
            mage_card_y = self.SCREEN_HEIGHT - 50
            mage_turn_result = self.mage.animate(deck_position=(mage_card_x,mage_card_y), target=self.wizard, turn=mage_turn and not self.game_over.is_game_over, weather_manager=self.weather_manager)  
            wizard_turn_result = self.wizard.animate(deck_position=(mage_card_x,mage_card_y), target=self.mage, turn=wizard_turn and not self.game_over.is_game_over, weather_manager=self.weather_manager)
            
            # Check for game over conditions
            if not self.game_over.is_game_over:
                if self.game_over.check_game_over(self.mage, self.wizard):
                    # Game is over, no need to check turn transitions
                    pass
                else:
                    # Check for turn transitions
                    turn_changed = False
                    
                    if mage_turn_result == False:
                        # if self.mage.damage_over_turn is not None:
                        #     self.mage.damage_over_turn.apply_damage(self.mage, self.weather_manager)
                        # if self.wizard.damage_over_turn is not None:
                        #     self.wizard.damage_over_turn.apply_damage(self.wizard, self.weather_manager)
                        mage_turn = False
                        wizard_turn = True
                        turn_changed = True
                        self.turn_indicator.start_transition(self.wizard)
                    elif wizard_turn_result == False:
                        # if self.mage.damage_over_turn is not None:
                        #     self.mage.damage_over_turn.apply_damage(self.mage, self.weather_manager)
                        # if self.wizard.damage_over_turn is not None:
                        #     self.wizard.damage_over_turn.apply_damage(self.wizard, self.weather_manager)
                        mage_turn = True
                        wizard_turn = False
                        turn_changed = True
                        self.turn_counter += 1  # Increment turn counter after full round
                        self.turn_indicator.start_transition(self.mage)
            
            # Render damage indicators (after characters but before turn indicator)
            self.damage_indicator.render()

            # Render quantum tunneling indicators
            self.quantum_tunneling_indicator.render()

            # Update and render turn indicator if game not over
            if not self.game_over.is_game_over:
                self.turn_indicator.update()
                self.turn_indicator.render()
            
            # Update and render game over screen
            self.game_over.update()
            self.game_over.render()
            
            # Render Phase Bias Manager (on top of everything)
            self.phase_bias_manager.render()

            pygame.display.flip()
            clock.tick(20)
        pygame.quit()
        sys.exit()

    def handle_events(self, event, mage_turn, wizard_turn):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_SPACE:
                self.mage.attack()
                self.wizard.attack()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            card = None
            # Handle card clicks
            mouse_pos = pygame.mouse.get_pos()
            if mage_turn == True:
                self.mage.handle_card_click(mouse_pos)
            elif wizard_turn == True:
                self.wizard.handle_card_click(mouse_pos)

        return True 