import pygame
from Cards.PhaseBias import PhaseBias
from QuantumMechanics.QuantumStates import QuantumState

class PhaseBiasUI:
    def __init__(self, screen):
        self.screen = screen
        self.active_phase_bias = None
        self.is_active = False
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.button_font = pygame.font.SysFont('Arial', 20, bold=True)
        
        # UI colors
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent black
        self.text_color = (255, 255, 255)
        self.button_color = (70, 130, 180)  # Steel blue
        self.button_hover_color = (100, 149, 237)  # Cornflower blue
        self.button_text_color = (255, 255, 255)
        
        # UI positioning
        self.ui_width = 400
        self.ui_height = 300
        self.ui_x = (self.screen.get_width() - self.ui_width) // 2
        self.ui_y = (self.screen.get_height() - self.ui_height) // 2
        
        # Button tracking
        self.buttons = []
        self.hovered_button = None
    
    def start_phase_bias_targeting(self, phase_bias_card):
        """Start the Phase Bias targeting process"""
        self.active_phase_bias = phase_bias_card
        self.is_active = True
        self.buttons = []
        print("Phase Bias UI activated")
    
    def handle_card_click(self, clicked_card):
        """Handle when a card is clicked during targeting"""
        if not self.is_active or not self.active_phase_bias:
            return False
        
        if self.active_phase_bias.awaiting_target_selection:
            # Try to select the clicked card as target
            if self.active_phase_bias.select_target_card(clicked_card):
                self.setup_state_selection_buttons()
                return True
            return False
        
        return False
    
    def setup_state_selection_buttons(self):
        """Setup buttons for state selection"""
        if not self.active_phase_bias or not self.active_phase_bias.target_card:
            return
        
        valid_states = self.active_phase_bias.get_valid_states_for_card(self.active_phase_bias.target_card)
        self.buttons = []
        
        button_width = 80
        button_height = 40
        button_spacing = 10
        start_x = self.ui_x + (self.ui_width - (len(valid_states) * (button_width + button_spacing) - button_spacing)) // 2
        start_y = self.ui_y + 150
        
        for i, state in enumerate(valid_states):
            button_x = start_x + i * (button_width + button_spacing)
            button_rect = pygame.Rect(button_x, start_y, button_width, button_height)
            
            # Get description for the state
            description = self.active_phase_bias.get_state_description(self.active_phase_bias.target_card, state)
            
            self.buttons.append({
                'rect': button_rect,
                'state': state,
                'description': description,
                'hovered': False
            })
    
    def handle_click(self, mouse_pos):
        """Handle mouse clicks on the UI"""
        if not self.is_active:
            return False
        
        # Check button clicks
        for button in self.buttons:
            if button['rect'].collidepoint(mouse_pos):
                if self.active_phase_bias.select_bias_state(button['state']):
                    # Bias selection complete
                    self.active_phase_bias.apply_bias_to_card()
                    self.close()
                    return True
        
        return False
    
    def handle_mouse_motion(self, mouse_pos):
        """Handle mouse motion for button hover effects"""
        if not self.is_active:
            return
        
        self.hovered_button = None
        for button in self.buttons:
            button['hovered'] = button['rect'].collidepoint(mouse_pos)
            if button['hovered']:
                self.hovered_button = button
    
    def close(self):
        """Close the Phase Bias UI"""
        self.is_active = False
        self.active_phase_bias = None
        self.buttons = []
        self.hovered_button = None
    
    def render(self):
        """Render the Phase Bias UI"""
        if not self.is_active or not self.active_phase_bias:
            return
        
        # Draw background
        bg_surface = pygame.Surface((self.ui_width, self.ui_height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        self.screen.blit(bg_surface, (self.ui_x, self.ui_y))
        
        # Draw border
        pygame.draw.rect(self.screen, self.text_color, (self.ui_x, self.ui_y, self.ui_width, self.ui_height), 2)
        
        # Draw title
        title_text = self.font.render("Phase Bias", True, self.text_color)
        title_x = self.ui_x + (self.ui_width - title_text.get_width()) // 2
        self.screen.blit(title_text, (title_x, self.ui_y + 20))
        
        if self.active_phase_bias.awaiting_target_selection:
            # Show targeting instructions
            instruction_text = self.small_font.render("Click on a superposition card to target", True, self.text_color)
            instruction_x = self.ui_x + (self.ui_width - instruction_text.get_width()) // 2
            self.screen.blit(instruction_text, (instruction_x, self.ui_y + 60))
            
        elif self.active_phase_bias.awaiting_state_selection:
            # Show state selection
            if self.active_phase_bias.target_card:
                target_text = self.small_font.render(f"Target: {self.active_phase_bias.target_card.name}", True, self.text_color)
                target_x = self.ui_x + (self.ui_width - target_text.get_width()) // 2
                self.screen.blit(target_text, (target_x, self.ui_y + 60))
                
                instruction_text = self.small_font.render("Choose which state to bias toward:", True, self.text_color)
                instruction_x = self.ui_x + (self.ui_width - instruction_text.get_width()) // 2
                self.screen.blit(instruction_text, (instruction_x, self.ui_y + 90))
                
                # Draw buttons
                for button in self.buttons:
                    color = self.button_hover_color if button['hovered'] else self.button_color
                    pygame.draw.rect(self.screen, color, button['rect'])
                    pygame.draw.rect(self.screen, self.text_color, button['rect'], 2)
                    
                    # Draw button text
                    button_text = self.button_font.render(button['state'], True, self.button_text_color)
                    text_x = button['rect'].centerx - button_text.get_width() // 2
                    text_y = button['rect'].centery - button_text.get_height() // 2
                    self.screen.blit(button_text, (text_x, text_y))
                
                # Show description for hovered button
                if self.hovered_button:
                    desc_text = self.small_font.render(self.hovered_button['description'], True, self.text_color)
                    desc_x = self.ui_x + (self.ui_width - desc_text.get_width()) // 2
                    self.screen.blit(desc_text, (desc_x, self.ui_y + 220))
        
        # Show cancel instruction
        cancel_text = self.small_font.render("Press ESC to cancel", True, (200, 200, 200))
        cancel_x = self.ui_x + (self.ui_width - cancel_text.get_width()) // 2
        self.screen.blit(cancel_text, (cancel_x, self.ui_y + self.ui_height - 30))
    
    def handle_key(self, key):
        """Handle keyboard input"""
        if key == pygame.K_ESCAPE:
            self.close()
            return True
        return False 