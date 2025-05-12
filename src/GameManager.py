import pygame
import sys
from Characters.Mage import Mage
from Characters.Wizard import Wizard
from Utils.HealthBar import HealthBar
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
        self.wizard = Wizard()

    def setup_display(self):
        background = pygame.image.load("./Assets/image.png")
        background = pygame.transform.scale(background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        return background
    
    def start_game(self):
        clock = pygame.time.Clock()
        game_assets = self.setup_display()
        running = True

        # Draw background
        while running:
            for event in pygame.event.get():
                running = self.handle_events(event)
            
            self.screen.blit(game_assets, (0, 0))
            # Draw mage at center of screen
            magesAndPlacements = self.mage.animate(position_to_draw=(650,280))
             
            wizardAndPlacements = self.wizard.animate(position_to_draw=(150,280))
            # self.screen.blit(mage, placement)
            self.screen.blit(magesAndPlacements[0], magesAndPlacements[1])
            self.screen.blit(pygame.transform.flip(wizardAndPlacements[0], True, False) , wizardAndPlacements[1])
            healthBar = HealthBar(self.screen).animate((660,50))
            # healthBarTwo = list(HealthBar().animate_background((70,20)))
            # scale health bar
            # healthBar[0] = pygame.transform.scale(healthBar[0], (230,25))
            # healthBarTwo[0] = pygame.transform.scale(healthBarTwo[0], (230,25))
            # self.screen.blit(healthBar[0], healthBar[1])
            # self.screen.blit(healthBarTwo[0], healthBarTwo[1])
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(10)


        # Quit game
        pygame.quit()
        sys.exit() 

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_SPACE:
                print("Space key pressed")
                self.mage.attack()
                self.wizard.attack()
            
        return True 