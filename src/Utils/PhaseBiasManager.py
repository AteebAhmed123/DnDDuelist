import pygame
from Cards.PhaseBias import PhaseBias
from QuantumMechanics.QuantumStates import QuantumState

class PhaseBiasManager:
    def __init__(self, screen):
        self.screen = screen
        self.is_active = False
        self.phase_bias_card = None
        self.target_cards = []  # Cards that can be targeted
        self.selected_target = None
        self.possible_states = {}
        self.selected_state = None
        self.font = pygame.font.SysFont('Arial', 18, bold=True)
        self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Message system for feedback
        self.show_message = False
        self.message_text = ""
        self.message_timer = 0
        self.message_duration = 120  # Show message for 6 seconds at 20 FPS
        
        # UI colors
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent black
        self.border_color = (255, 255, 255)
        self.highlight_color = (255, 255, 0)
        self.text_color = (255, 255, 255)
        self.error_color = (255, 100, 100)  # Light red for error messages
        
    def start_targeting(self, phase_bias_card, hand_cards):
        """Start the Phase Bias targeting process"""
        self.is_active = True
        self.phase_bias_card = phase_bias_card
        self.target_cards = []
        self.selected_target = None
        self.selected_state = None
        
        # Find cards that can be targeted (superposition cards)
        for card in hand_cards:
            if (hasattr(card, 'stateType') and 
                card.stateType == QuantumState.SUPERPOSITION and
                hasattr(card, 'apply_phase_bias')):
                self.target_cards.append(card)
        
        # If no valid targets found, cancel immediately
        if not self.target_cards:
            self.is_active = False
            self.show_error_message("No Superposition cards to target! Phase Bias discarded.")
            return False  # Indicate that targeting failed
        
        return True  # Indicate that targeting started successfully
    
    def handle_click(self, mouse_pos):
        """Handle clicks during Phase Bias targeting"""
        if not self.is_active:
            return False
            
        # Check if clicking on a target card
        if self.selected_target is None:
            for card in self.target_cards:
                if hasattr(card, 'is_clicked') and card.is_clicked(mouse_pos):
                    self.selected_target = card
                    if hasattr(card, 'get_possible_states'):
                        self.possible_states = card.get_possible_states()
                    return True
        
        # Check if clicking on a state option
        elif self.selected_target is not None and self.selected_state is None:
            # Calculate state option positions
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            dialog_width = 400
            dialog_height = 300
            dialog_x = (screen_width - dialog_width) // 2
            dialog_y = (screen_height - dialog_height) // 2
            
            # Check clicks on state buttons
            button_height = 40
            button_margin = 10
            start_y = dialog_y + 80
            
            for i, (state, description) in enumerate(self.possible_states.items()):
                button_y = start_y + i * (button_height + button_margin)
                button_rect = pygame.Rect(dialog_x + 20, button_y, dialog_width - 40, button_height)
                
                if button_rect.collidepoint(mouse_pos):
                    self.selected_state = state
                    self.apply_phase_bias()
                    return True
        
        return False
    
    def apply_phase_bias(self):
        """Apply the phase bias to the selected target"""
        if self.selected_target and self.selected_state:
            self.phase_bias_card.set_target_and_bias(self.selected_target, self.selected_state)
            self.is_active = False
    
    def cancel(self):
        """Cancel the Phase Bias targeting"""
        self.is_active = False
        self.selected_target = None
        self.selected_state = None
    
    def update(self):
        """Update the Phase Bias Manager state"""
        # Update message timer
        if self.show_message and self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.show_message = False
    
    def render(self):
        """Render the Phase Bias targeting UI"""
        # Always update first
        self.update()
        
        # Render error message if active
        if self.show_message:
            self.render_error_message()
        
        # Render targeting UI if active
        if not self.is_active:
            return
            
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        if self.selected_target is None:
            # Show instruction to select a target card
            instruction_text = "Click on a Superposition card to apply Phase Bias"
            text_surface = self.font.render(instruction_text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, 50))
            
            # # Draw background
            # bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, 
            #                     text_rect.width + 20, text_rect.height + 10)
            # bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            # bg_surface.fill(self.bg_color)
            # self.screen.blit(bg_surface, bg_rect)
            
            # Draw text
            self.screen.blit(text_surface, text_rect)
            
            # Highlight targetable cards
            for card in self.target_cards:
                if hasattr(card, 'rect') and card.rect:
                    pygame.draw.rect(self.screen, self.highlight_color, card.rect, 3)
                    
        elif self.selected_state is None:
            # Show state selection dialog
            self.render_state_selection_dialog()
    
    def render_state_selection_dialog(self):
        """Render the state selection dialog"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        dialog_width = 400
        dialog_height = 300
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = (screen_height - dialog_height) // 2
        
        # Draw dialog background
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        dialog_surface.fill(self.bg_color)
        self.screen.blit(dialog_surface, (dialog_x, dialog_y))
        
        # Draw border
        pygame.draw.rect(self.screen, self.border_color, 
                        (dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Draw title
        title_text = f"Choose favored state for {self.selected_target.name}"
        title_surface = self.title_font.render(title_text, True, self.text_color)
        title_rect = title_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 30))
        self.screen.blit(title_surface, title_rect)
        
        # Draw state options
        button_height = 40
        button_margin = 10
        start_y = dialog_y + 80
        
        for i, (state, description) in enumerate(self.possible_states.items()):
            button_y = start_y + i * (button_height + button_margin)
            button_rect = pygame.Rect(dialog_x + 20, button_y, dialog_width - 40, button_height)
            
            # Draw button background
            pygame.draw.rect(self.screen, (50, 50, 50), button_rect)
            pygame.draw.rect(self.screen, self.border_color, button_rect, 2)
            
            # Draw button text
            button_text = f"State {state}: {description}"
            text_surface = self.font.render(button_text, True, self.text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Draw instructions
        instruction_text = "Click on a state to favor it (70% chance)"
        instruction_surface = self.font.render(instruction_text, True, self.text_color)
        instruction_rect = instruction_surface.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + dialog_height - 30))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def render_error_message(self):
        """Render error message to the player"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Render error message
        error_surface = self.font.render(self.message_text, True, self.error_color)
        error_rect = error_surface.get_rect(center=(screen_width // 2, 100))
        
        # Draw background
        bg_rect = pygame.Rect(error_rect.x - 15, error_rect.y - 10, 
                            error_rect.width + 30, error_rect.height + 20)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((50, 0, 0, 200))  # Dark red background
        self.screen.blit(bg_surface, bg_rect)
        
        # Draw border
        pygame.draw.rect(self.screen, self.error_color, bg_rect, 2)
        
        # Draw text
        self.screen.blit(error_surface, error_rect)
    
    def show_error_message(self, message):
        """Show an error message to the player"""
        self.show_message = True
        self.message_text = message
        self.message_timer = self.message_duration 