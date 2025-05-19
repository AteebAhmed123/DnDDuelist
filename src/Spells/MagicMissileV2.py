import pygame
import math
import random
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase

class MagicMissileV2(SpellBase):
    """Magic missile spell that reverses direction and hits the caster"""
    
    # Define animation frames as class variable
    animation_frames = [
        (26, 33, 52, 36),    # Frame 1
        (126, 33, 52, 36),    # Frame 1
        (226, 33, 52, 36),    # Frame 1
        (326, 33, 52, 36),    # Frame 1
        (426, 33, 52, 36),    # Frame 1
        (526, 33, 52, 36),    # Frame 1
        (626, 33, 52, 36),    # Frame 1
        (726, 33, 52, 36),    # Frame 1
        (826, 33, 52, 36)    # Frame 1 # Frame 1
    ]
    
    def __init__(self, screen):
        """Initialize the magic missile spell"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/magicmissile2.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_frame = 0
        self.damage = 3  # Self-damage is less than regular damage
        self.spell_active = False
        
        # Missile properties
        self.missiles = []
        self.missile_speed = 5
        self.max_missiles = 5
        self.missile_size = (72, 72)
        self.reversal_point = 0.5  # Point at which missiles reverse (0.5 = halfway)
        self.scale_factor = 2  # Scale the lightning to be twice as large
        self.missile_sound = pygame.mixer.Sound("./Assets/Sounds/magicmissile.mp3")
        self.sound_played = False

    def animate_spell(self, caster, target):
        """Animate the magic missile spell
        
        Args:
            caster: The character casting the spell
            target: The intended target (though missiles will reverse)
            
        Returns:
            True if animation is still playing, False when complete
        """
        if not self.spell_active:
            # Initialize missiles when spell starts
            self.spell_active = True
            self.missiles = []
            self.current_frame = 0
            self.sound_played = False
            
            # Create missiles
            for _ in range(self.max_missiles):
                # Random starting position near caster
                start_x = caster.position_to_draw[0] + random.randint(-20, 20)
                start_y = caster.position_to_draw[1] + random.randint(-20, 20)
                
                # Calculate path to target
                target_x = target.position_to_draw[0] + random.randint(-30, 30)
                target_y = target.position_to_draw[1] + random.randint(-30, 30)
                
                # Calculate midpoint for reversal
                mid_x = start_x + (target_x - start_x) * self.reversal_point
                mid_y = start_y + (target_y - start_y) * self.reversal_point
                
                # Add random variation to midpoint
                mid_x += random.randint(-20, 20)
                mid_y += random.randint(-20, 20)
                
                # Create missile
                missile = {
                    'x': start_x,
                    'y': start_y,
                    'start_x': start_x,
                    'start_y': start_y,
                    'mid_x': mid_x,
                    'mid_y': mid_y,
                    'target_x': start_x,  # Return to caster
                    'target_y': start_y,
                    'progress': 0.0,
                    'speed': self.missile_speed * (1.4 + random.random() * 0.4),  # Vary speed slightly
                    'frame': random.randint(0, len(self.animation_frames) - 1),
                    'hit': False,
                    'reversed': False
                }
                self.missiles.append(missile)
            
            # Play the missile launch sound
            self.missile_sound.play()
            self.sound_played = True
            
            return True
            
        # Update and render each missile
        all_missiles_complete = True
        
        for missile in self.missiles:
            if missile['hit']:
                continue
                
            all_missiles_complete = False
            
            # Update missile position
            missile['progress'] += missile['speed'] / 100.0
            
            # Check if missile should reverse direction
            if not missile['reversed'] and missile['progress'] >= self.reversal_point:
                missile['reversed'] = True
                # Add some "confusion" to the missile path when it reverses
                missile['mid_x'] += random.randint(-30, 30)
                missile['mid_y'] += random.randint(-30, 30)
            
            # Calculate position based on quadratic Bezier curve
            if not missile['reversed']:
                # First half of journey (to midpoint)
                t = missile['progress'] / self.reversal_point
                missile['x'] = self._quadratic_bezier(
                    missile['start_x'], missile['mid_x'], missile['mid_x'], t)
                missile['y'] = self._quadratic_bezier(
                    missile['start_y'], missile['mid_y'], missile['mid_y'], t)
            else:
                # Second half of journey (back to caster)
                t = (missile['progress'] - self.reversal_point) / (1 - self.reversal_point)
                missile['x'] = self._quadratic_bezier(
                    missile['mid_x'], missile['mid_x'], missile['target_x'], t)
                missile['y'] = self._quadratic_bezier(
                    missile['mid_y'], missile['mid_y'], missile['target_y'], t)
            
            # Check if missile has reached target (caster)
            if missile['progress'] >= 1.0:
                missile['hit'] = True
                # Apply damage when the last missile hits
                if all(m['hit'] for m in self.missiles):
                    self.apply_affect(caster)
                continue
            
            # Update animation frame
            missile['frame'] = (missile['frame'] + 0.2) % len(self.animation_frames)
            
            # Draw missile
            frame_index = int(missile['frame'])
            missile_sprite = self.sprite.get_sprite(self.animation_frames[frame_index])
            missile_sprite = pygame.transform.scale(missile_sprite, self.missile_size)
            
            # Rotate sprite to face direction of travel
            if missile['reversed']:
                # Calculate angle for return journey
                dx = missile['target_x'] - missile['x']
                dy = missile['target_y'] - missile['y']
            else:
                # Calculate angle for outward journey
                dx = missile['mid_x'] - missile['x']
                dy = missile['mid_y'] - missile['y']
                
            angle = math.degrees(math.atan2(dy, dx))
            rotated_missile = pygame.transform.rotate(missile_sprite, -angle)
            
            # Draw missile
            self.screen.blit(rotated_missile, (missile['x'] - rotated_missile.get_width() // 2, 
                                              missile['y'] - rotated_missile.get_height() // 2))
        
        # Check if all missiles have hit
        if all_missiles_complete:
            self.spell_active = False
            return False
            
        return True
        
    def _quadratic_bezier(self, p0, p1, p2, t):
        """Calculate point on a quadratic Bezier curve
        
        Args:
            p0, p1, p2: Control points
            t: Parameter (0 to 1)
            
        Returns:
            Position on curve
        """
        return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
        
    def apply_affect(self, target):
        """Apply damage to the target (caster)"""
        target.health.reduce_health(self.damage)
        print(f"Magic Missile backfires and deals {self.damage} damage to caster!") 