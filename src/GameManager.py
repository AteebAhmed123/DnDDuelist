import pygame
import sys
from Characters.Mage import Mage
from Characters.Wizard import Wizard
from Utils.HealthBar import HealthBar
from pygame.sprite import LayeredUpdates

class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Initialize characters
        self.mage = Mage(self.screen, (650,280))
        self.wizard = Wizard(self.screen, (150,280))

    def setup_display(self):
        background = pygame.image.load("./Assets/image.png")
        background = pygame.transform.scale(background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        return background
    
    def start_game(self):
        clock = pygame.time.Clock()
        game_assets = self.setup_display()
        running = True

        while running:
            for event in pygame.event.get():
                running = self.handle_events(event)
            
            # Draw background
            self.screen.blit(game_assets, (0, 0))
            
            # Draw characters
            mage_card_x = self.SCREEN_WIDTH // 2 - 250
            mage_card_y = self.SCREEN_HEIGHT - 50
            self.mage.animate(deck_position=(mage_card_x,mage_card_y), target=self.wizard)             
            self.wizard.animate(deck_position=(mage_card_x,mage_card_y))
            
            # Draw mage's cards at bottom right of screen

            
            # Draw wizard's cards at bottom left of screen
            # wizard_card_x = self.SCREEN_WIDTH // 2 - 250
            # wizard_card_y = self.SCREEN_HEIGHT - 400
            # self.wizard.render_deck(wizard_card_x, wizard_card_y)
            
            pygame.display.flip()
            clock.tick(10)
        pygame.quit()
        sys.exit()

    def handle_events(self, event):
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
            self.mage.handle_card_click(mouse_pos)
        
        return True 