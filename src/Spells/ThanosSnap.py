import pygame
import random
import math
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.SpellBase import SpellBase
import os
class ThanosSnap(SpellBase):
    """Thanos Snap spell that makes the opponent discard half their cards"""
    
    # Define animation frames as class variable
    animation_frames = [
        # (6, 144, 72, 77),    # Frame 1
        # (256, 144, 72, 77),    # Frame 1
        # (346, 144, 72, 77),    # Frame 1
        # (426, 144, 72, 77),    # Frame 1
        # (1505, 144, 72, 77),    # Frame 1
        # (1581, 144, 72, 77),    # Frame 1
        (18, 148, 58, 72),    # Frame 1
        (599, 147, 58, 72),    # Frame 1
        (1595, 148, 58, 72),    # Frame 1
        (1920, 144, 58, 72),    # Frame 1
        (2329, 144, 58, 77),    # Frame 1
        (2912, 144, 58, 77),    # Frame 1
        (3576, 144, 58, 77)
    ]
    
    def __init__(self, screen):
        """Initialize the Thanos Snap effect"""
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/thanos_snap_sheet.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.current_frame = 0
        self.spell_active = False
        
        # Particle properties
        self.particles = []
        self.max_particles = 200
        self.particle_colors = [
            (255, 165, 0),    # Orange
            (255, 140, 0),    # Dark Orange
            (255, 69, 0),     # Red-Orange
            (255, 215, 0),    # Gold
            (218, 165, 32)    # Golden Rod
        ]
        
        # Sound effect
        self.sound_played = False
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        sound_path_snap = "./Assets/Sounds/thanossnap.wav"
        
        total_path_snap = os.path.join(parent2, sound_path_snap)
        self.snap_sound = pygame.mixer.Sound(total_path_snap)
        
    def animate_spell(self, caster, target):
        """Animate the Thanos Snap spell
        
        Args:
            caster: The character casting the spell
            target: The character whose cards will be discarded
            
        Returns:
            True if animation is still playing, False when complete
        """
        if not self.spell_active:
            # Initialize effect when spell starts
            self.spell_active = True
            self.particles = []
            self.current_frame = 0
            self.sound_played = False
            
            # Play sound effect
            self.snap_sound.play()
            self.sound_played = True
            
            # Create initial particles around target's cards
            self._create_card_particles(target)
            
            return True
            
        # Update animation frame
        self.current_frame += 0.2
        frame_index = int(self.current_frame) % len(self.animation_frames)
        
        # Draw the snap effect near caster's hand
        position_to_draw = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        snap_pos = (position_to_draw[0] - 120, position_to_draw[1] - 170)
        snap_sprite = self.sprite.get_sprite(self.animation_frames[frame_index])
        snap_sprite = pygame.transform.scale(snap_sprite, (200, 200))
        self.screen.blit(snap_sprite, snap_pos)
        
        # Update and draw particles
        self._update_particles()
        
        # End animation after 60 frames
        if self.current_frame >= len(self.animation_frames):
            self.apply_affect(target)
            self.spell_active = False
            return False
            
        return True
        
    def _create_card_particles(self, target):
        """Create particles around target's cards"""
        # Get positions of cards in hand
        card_positions = []
        
        # Add particles for each card in hand
        for i, card in enumerate(target.hand.cards_in_hand):
            if hasattr(card, 'rect') and card.rect:
                card_center = (
                    card.rect.centerx,
                    card.rect.centery
                )
                card_positions.append(card_center)
                
                # Create particles for this card
                self._create_particles_at_position(target.position_to_draw, 80)  # 30 particles per card
        
        # Add some particles around the deck
        deck_pos = (target.position_to_draw[0] - 100, target.position_to_draw[1] + 100)
        # self._create_particles_at_position(deck_pos, 50)  # 50 particles for the deck
    
    def _create_particles_at_position(self, position, count):
        """Create particles at the specified position"""
        for _ in range(count):
            # Random offset from center
            offset_x = random.randint(-60, 60)
            offset_y = random.randint(-320, 200)
            
            # Create particle
            particle = {
                'x': position[0] + offset_x,
                'y': position[1] + offset_y,
                'size': random.randint(15, 15),
                'color': random.choice(self.particle_colors),
                'speed_x': random.uniform(-1.5, 1.5),
                'speed_y': random.uniform(-1.5, 1.5),
                'fade_speed': random.uniform(0.01, 0.03),
                'alpha': 255,
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-5, 5)
            }
            self.particles.append(particle)
    
    def _update_particles(self):
        """Update and draw all particles"""
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Update rotation
            particle['rotation'] += particle['rotation_speed']
            
            # Update alpha (fade out)
            particle['alpha'] -= particle['fade_speed'] * 255
            
            # Remove faded particles
            if particle['alpha'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Draw particle
            particle_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            
            # Set color with current alpha
            color = list(particle['color']) + [int(particle['alpha'])]
            
            # Draw a small square
            pygame.draw.rect(
                particle_surface, 
                color, 
                (0, 0, particle['size'], particle['size'])
            )
            
            # Rotate the particle
            rotated_particle = pygame.transform.rotate(particle_surface, particle['rotation'])
            
            # Draw the particle
            self.screen.blit(
                rotated_particle, 
                (particle['x'] - rotated_particle.get_width() // 2, 
                 particle['y'] - rotated_particle.get_height() // 2)
            )
    
    def apply_affect(self, target):
        """Apply the card discard effect to the target"""
        # Calculate how many cards to discard (half of total cards)
        total_cards = len(target.deck.cards_in_deck)
        discard_count = total_cards // 2  # Integer division for rounding down
        
        # First discard from hand
        
        # Then discard from deck if needed
        deck_discard = min(len(target.deck.cards_in_deck), discard_count)
        for _ in range(deck_discard):
            if target.deck.cards_in_deck:
                # Remove a random card from deck
                card_index = random.randint(0, len(target.deck.cards_in_deck) - 1)
                target.deck.cards_in_deck.pop(card_index)
