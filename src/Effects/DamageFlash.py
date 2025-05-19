import pygame

class DamageFlash:
    """Creates a flashing effect on sprites when they take damage"""
    
    def __init__(self):
        """Initialize the damage flash effect"""
        self.active_flashes = {}  # Dictionary of active flashes by character ID
        
    def start_flash(self, character_id, duration=10):
        """Start a damage flash effect for a character
        
        Args:
            character_id: Unique identifier for the character
            duration: How long the flash should last in frames
        """
        self.active_flashes[character_id] = {
            'duration': duration,
            'remaining': duration,
            'intensity': 1.0  # Start at full intensity
        }
    
    def update(self):
        """Update all active flash effects"""
        # Update each flash
        for character_id in list(self.active_flashes.keys()):
            flash = self.active_flashes[character_id]
            flash['remaining'] -= 1
            
            # Calculate intensity (pulsing effect)
            progress = flash['remaining'] / flash['duration']
            flash['intensity'] = 0.5 + 0.5 * abs(progress * 2 - 1)  # Pulse between 0.5 and 1.0
            
            # Remove if expired
            if flash['remaining'] <= 0:
                del self.active_flashes[character_id]
    
    def apply_flash(self, character_id, sprite_surface):
        """Apply flash effect to a sprite if active
        
        Args:
            character_id: Unique identifier for the character
            sprite_surface: The pygame surface to apply the effect to
            
        Returns:
            Modified surface with flash effect, or original if no flash active
        """
        if character_id not in self.active_flashes:
            return sprite_surface
            
        # Get a copy of the sprite to modify
        flash_surface = sprite_surface.copy()
        
        # Get flash intensity
        intensity = self.active_flashes[character_id]['intensity']
        
        # Create a red overlay with the current intensity
        overlay = pygame.Surface(flash_surface.get_size(), pygame.SRCALPHA)
        red_value = int(255 * intensity)
        overlay.fill((red_value, 0, 0, 100))  # Semi-transparent red
        
        # Apply the overlay
        flash_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_ADD)
        
        return flash_surface 