import pygame
import sys
from Characters.Mage import Mage

class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Initialize mage
        self.mage = Mage()

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
            
            # Draw mage at center of screen
            mage, placement = self.mage.image_at(position_to_draw=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

            self.screen.blit(mage, placement)
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(60)

        # Quit game
        pygame.quit()
        sys.exit() 

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
        return True