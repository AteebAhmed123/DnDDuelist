import pygame
from abc import ABC, abstractmethod
from SpriteUtil.SpriteUtil import SpriteUtil

class SpellBase(ABC):
    """Base class for all spells and magical effects"""
    
    def __init__(self, screen):
        """Initialize the spell effect
        
        Args:
            screen: The pygame screen to render on
            caster_position: (x, y) position of the spell caster
            target_position: (x, y) position of the spell target
        """
        self.screen = screen
        self.sprite = None
        self.is_active = False
        self.current_frame = 0
        self.frame_counter = 0
        
    def start(self):
        """Start the spell animation"""
        self.current_frame = 0
        self.frame_counter = 0
        self.is_active = True

    @abstractmethod
    def animate_spell(self, caster, target):
        """Render the spell effect"""
        pass
        
    def apply_effect(self):
        """Apply the spell's effect to the target
        
        This method is called when the spell animation completes
        """
        pass 