from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from QuantumMechanics.QuantumStates import QuantumState
from QuantumMechanics.Superposition import Superposition
import pygame

class PhaseBias(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Phase Bias"
    description = "Apply phase bias to a superposition card to favor a specific outcome."
    damage = 0
    
    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/PhaseBias.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.activated_card = False
        self.stateType = QuantumState.COLLAPSED  # Phase Bias is not in superposition itself
        self.target_card = None
        self.bias_state = None
        self.bias_strength = 0.75  # 75% chance to favor the chosen state
        self.awaiting_target_selection = False
        self.awaiting_state_selection = False

    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        """
        Phase Bias card requires two-step activation:
        1. Select target superposition card
        2. Select which state to bias toward
        """
        if not self.awaiting_target_selection and not self.awaiting_state_selection:
            # Start the targeting process
            self.awaiting_target_selection = True
            print("Phase Bias activated! Click on a superposition card to target.")
            return None, None
        
        # If we've completed the bias application
        if self.target_card and self.bias_state:
            self.apply_bias_to_card()
            return False, None  # Card effect completed
        
        return None, None
    
    def select_target_card(self, target_card):
        """Select which card to apply the bias to"""
        if not self.awaiting_target_selection:
            return False
        
        # Check if the target card is in superposition
        if hasattr(target_card, 'stateType') and target_card.stateType == QuantumState.SUPERPOSITION:
            self.target_card = target_card
            self.awaiting_target_selection = False
            self.awaiting_state_selection = True
            print(f"Target selected: {target_card.name}. Now choose which state to bias toward.")
            return True
        else:
            print("Target must be a card in superposition!")
            return False
    
    def select_bias_state(self, state_choice):
        """Select which state to bias toward"""
        if not self.awaiting_state_selection or not self.target_card:
            return False
        
        # Determine valid states based on the target card
        valid_states = self.get_valid_states_for_card(self.target_card)
        
        if state_choice in valid_states:
            self.bias_state = state_choice
            self.awaiting_state_selection = False
            print(f"Bias state selected: {state_choice}")
            return True
        else:
            print(f"Invalid state choice. Valid options: {valid_states}")
            return False
    
    def get_valid_states_for_card(self, card):
        """Get the valid states that can be biased for a specific card"""
        # For DuelistParadox (2-state system)
        if hasattr(card, 'qubit') and card.qubit.num_qubits == 1:
            return ['0', '1']  # Lightning or Heal
        # For ElementalWeather (4-state system)
        elif hasattr(card, 'qubit') and card.qubit.num_qubits == 2:
            return ['00', '01', '10', '11']  # Earthquake, HeatWave, Rain, WindTornado
        else:
            return []
    
    def apply_bias_to_card(self):
        """Apply the phase bias to the target card"""
        if not self.target_card or not self.bias_state:
            return False
        
        # Modify the target card's quantum circuit to include bias
        if hasattr(self.target_card, 'qubit'):
            # Store the bias information in the target card
            self.target_card.phase_bias_state = self.bias_state
            self.target_card.phase_bias_strength = self.bias_strength
            self.target_card.has_phase_bias = True
            
            print(f"Phase bias applied! {self.target_card.name} now has {self.bias_strength*100}% chance to collapse to state {self.bias_state}")
            return True
        
        return False
    
    def get_state_description(self, card, state):
        """Get a human-readable description of what each state means for a card"""
        if card.name == "Duelist's Paradox":
            if state == '0':
                return "Lightning (Attack)"
            elif state == '1':
                return "Heal (Defense)"
        elif card.name == "Elemental Weather":
            if state == '00':
                return "Earthquake"
            elif state == '01':
                return "HeatWave"
            elif state == '10':
                return "Rain"
            elif state == '11':
                return "WindTornado"
        elif card.name == "Collapse Barrier":
            if state == '0':
                return "Barrier (Protection)"
            elif state == '1':
                return "Vulnerability (3x Damage)"
        
        return f"State {state}"
    
    def is_awaiting_input(self):
        """Check if the card is waiting for player input"""
        return self.awaiting_target_selection or self.awaiting_state_selection
    
    def get_current_prompt(self):
        """Get the current prompt for the player"""
        if self.awaiting_target_selection:
            return "Select a superposition card to target"
        elif self.awaiting_state_selection:
            return "Choose which state to bias toward"
        return "" 