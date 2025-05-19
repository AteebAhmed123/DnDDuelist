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

class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Initialize effects
        self.turn_indicator = TurnIndicator(self.screen)
        self.damage_indicator = DamageIndicator(self.screen)
        self.damage_flash = DamageFlash()
        
        # Initialize characters
        self.mage = Mage(self.screen, (650,280))
        self.wizard = Wizard(self.screen, (150,280))
        
        # Set damage indicators for health bars
        self.mage.health.set_damage_indicator(self.damage_indicator)
        self.wizard.health.set_damage_indicator(self.damage_indicator)
        
        # Set damage flash effect
        self.mage.set_damage_flash(self.damage_flash)
        self.wizard.set_damage_flash(self.damage_flash)
        
        # Turn counter
        self.turn_counter = 1

    def setup_display(self):
        background = pygame.image.load("./Assets/image.png")
        background = pygame.transform.scale(background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        return background
    
    def start_game(self):
        clock = pygame.time.Clock()
        game_assets = self.setup_display()
        running = True
        initiative = random.randint(0,1)
        mage_turn = False
        wizard_turn = True
        
        # Show initial turn indicator
        current_player = "Wizard" if wizard_turn else "Mage"
        self.turn_indicator.start_transition(current_player)
        
        while running:
            for event in pygame.event.get():
                # Only process events if turn indicator is not active
                if not self.turn_indicator.is_active:
                    running = self.handle_events(event, mage_turn, wizard_turn)
            
            # Draw background
            self.screen.blit(game_assets, (0, 0))
            
            # Update effects
            self.damage_indicator.update()
            self.damage_flash.update()
            
            # Draw turn counter
            font = pygame.font.SysFont('Arial', 24)
            turn_text = font.render(f"Turn {self.turn_counter}", True, (255, 255, 255))
            self.screen.blit(turn_text, (20, 20))
            
            # Draw current player indicator
            current_player = "Wizard's Turn" if wizard_turn else "Mage's Turn"
            player_text = font.render(current_player, True, (255, 255, 255))
            self.screen.blit(player_text, (20, 50))
            
            # Animate characters
            mage_card_x = self.SCREEN_WIDTH // 2 - 250
            mage_card_y = self.SCREEN_HEIGHT - 50
            mage_turn_result = self.mage.animate(deck_position=(mage_card_x,mage_card_y), target=self.wizard, turn=mage_turn)  
            wizard_turn_result = self.wizard.animate(deck_position=(mage_card_x,mage_card_y), target=self.mage, turn=wizard_turn)
            
            # Check for turn transitions
            turn_changed = False
            
            if mage_turn_result == False:
                mage_turn = False
                wizard_turn = True
                turn_changed = True
                self.turn_indicator.start_transition("Wizard")
            elif wizard_turn_result == False:
                mage_turn = True
                wizard_turn = False
                turn_changed = True
                self.turn_counter += 1  # Increment turn counter after full round
                self.turn_indicator.start_transition("Mage")
            
            # Render damage indicators (after characters but before turn indicator)
            self.damage_indicator.render()
            
            # Update and render turn indicator
            self.turn_indicator.update()
            self.turn_indicator.render()
            
            pygame.display.flip()
            clock.tick(10)
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
            # Handle card clicks
            mouse_pos = pygame.mouse.get_pos()
            if mage_turn == True:
                self.mage.handle_card_click(mouse_pos)
            elif wizard_turn == True:
                self.wizard.handle_card_click(mouse_pos)
        return True 