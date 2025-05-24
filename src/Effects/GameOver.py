import pygame

class GameOver:
    """Handles the game over state and winner determination"""
    
    def __init__(self, screen):
        """Initialize the game over screen"""
        self.screen = screen
        self.is_game_over = False
        self.winner = None
        self.reason = ""
        
        # Font for game over text
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 32)
        self.detail_font = pygame.font.SysFont('Arial', 24)
        
        # Transition animation
        self.fade_alpha = 0
        self.fade_speed = 5
        self.fade_max = 180  # Max alpha for semi-transparent overlay
        
        # Button for returning to menu
        self.restart_button_rect = pygame.Rect(0, 0, 200, 50)
        self.quit_button_rect = pygame.Rect(0, 0, 200, 50)
        
    def check_game_over(self, mage, wizard):
        """Check if the game is over and determine the winner
        
        Game is over if:
        1. Either character's health reaches 0
        2. A character has no cards in both hand and deck
        
        Returns:
            bool: True if game is over, False otherwise
        """
        # Check health condition
        if mage.health.health <= 0:
            self.winner = wizard
            self.reason = f"{mage.character_id} has been defeated!"
            self.is_game_over = True
            return True
            
        if wizard.health.health <= 0:
            self.winner = mage
            self.reason = f"{wizard.character_id} has been defeated!"
            self.is_game_over = True
            return True
            
        # Check empty deck and hand condition
        if len(mage.deck.cards_in_deck) == 0 and len(mage.hand.cards_in_hand) == 0:
            self.winner = wizard
            self.reason = f"{mage.character_id} has run out of cards!"
            self.is_game_over = True
            return True
            
        if len(wizard.deck.cards_in_deck) == 0 and len(wizard.hand.cards_in_hand) == 0:
            self.winner = mage
            self.reason = f"{wizard.character_id} has run out of cards!"
            self.is_game_over = True
            return True
            
        return False
        
    def update(self):
        """Update the game over screen transition"""
        if self.is_game_over and self.fade_alpha < self.fade_max:
            self.fade_alpha += self.fade_speed
            if self.fade_alpha > self.fade_max:
                self.fade_alpha = self.fade_max
                
    def render(self):
        """Render the game over screen"""
        if not self.is_game_over:
            return
            
        # Create overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.fade_alpha))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 80))
        self.screen.blit(game_over_text, text_rect)
        
        # Draw winner text
        if self.winner:
            winner_text = self.subtitle_font.render(f"{self.winner.character_id} Wins!", True, (255, 255, 255))
            winner_rect = winner_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
            self.screen.blit(winner_text, winner_rect)
            
            # Draw reason
            reason_text = self.detail_font.render(self.reason, True, (200, 200, 200))
            reason_rect = reason_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
            self.screen.blit(reason_text, reason_rect)
        
        # Draw buttons if fully faded in
        if self.fade_alpha >= self.fade_max:
            # Restart button
            button_width = 200
            button_height = 50
            button_margin = 20
            
            # Position buttons
            self.restart_button_rect = pygame.Rect(
                self.screen.get_width() // 2 - button_width - button_margin,
                self.screen.get_height() // 2 + 80,
                button_width,
                button_height
            )
            
            self.quit_button_rect = pygame.Rect(
                self.screen.get_width() // 2 + button_margin,
                self.screen.get_height() // 2 + 80,
                button_width,
                button_height
            )
            
            # Draw restart button
            pygame.draw.rect(self.screen, (50, 150, 50), self.restart_button_rect, border_radius=10)
            restart_text = self.detail_font.render("Play Again", True, (255, 255, 255))
            restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
            self.screen.blit(restart_text, restart_text_rect)
            
            # Draw quit button
            pygame.draw.rect(self.screen, (150, 50, 50), self.quit_button_rect, border_radius=10)
            quit_text = self.detail_font.render("Quit Game", True, (255, 255, 255))
            quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
            self.screen.blit(quit_text, quit_text_rect)
    
    def handle_click(self, mouse_pos):
        """Handle clicks on the game over screen buttons
        
        Returns:
            str: Action to take ('restart', 'quit', or None)
        """
        if not self.is_game_over or self.fade_alpha < self.fade_max:
            return None
            
        if self.restart_button_rect.collidepoint(mouse_pos):
            return "restart"
            
        if self.quit_button_rect.collidepoint(mouse_pos):
            return "quit"
            
        return None
        
    def reset(self):
        """Reset the game over state"""
        self.is_game_over = False
        self.winner = None
        self.reason = ""
        self.fade_alpha = 0 