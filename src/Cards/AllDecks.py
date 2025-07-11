from Cards.DuelistParadox import DuelistParadox
from Cards.MagicMissive import MagicMissive
from Cards.ThanosSnapCard import ThanosSnapCard
from Cards.CollapseBarrier import CollapseBarrier
from SpriteUtil.SpriteUtil import SpriteUtil
import random
import pygame
from abc import ABC, abstractmethod

class AllDecks(ABC):
    """Abstract class for all decks"""
    @abstractmethod
    def _initialize_default_cards(self):
        pass

    def __init__(self, screen, max_cards, sprite_path, deck_coords):
        """Initialize a deck with up to 20 cards"""
        self.screen = screen
        self.cards_in_deck = []
        self.max_cards = max_cards
        # self.hand = Hand(screen)
        
        # Initialize deck sprite
        self.SPRITE_PATH = sprite_path
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.deck_coords = deck_coords  # Adjust based on your sprite dimensions
        # Initialize with some default cards
        self._initialize_default_cards()

        
    def _initialize_default_cards(self):
        """Add some default cards to the deck"""
        # Add 3 copies of each card type for a total of 9 cards
        for _ in range(0, self.max_cards):
            all_cards = list(self.POSSIBLE_CARDS.keys())
            weights = list(self.POSSIBLE_CARDS.values())
            card_class = random.choice(random.choices(all_cards, weights=weights, k=1))
            self.add_card(card_class(self.screen))

    def add_card(self, card):
        """Add a card to the deck if there's room"""
        if len(self.cards_in_deck) < self.max_cards:
            self.cards_in_deck.append(card)
            return True
        return False

    
    def render(self, center_x, y_position):
        """Render the current hand of cards and the deck sprite"""
        # Render the hand
        # Render the deck sprite at bottom right
        deck_image = self.sprite.get_sprite(self.deck_coords)
        deck_x = center_x + self.X_OFFSET # 20px margin from right edge
        deck_y = y_position + self.Y_OFFSET  # 20px margin from bottom edge
        self.screen.blit(deck_image, (deck_x, deck_y))
        
        # Display card count on top of the deck
        card_count = len(self.cards_in_deck)
        font = pygame.font.SysFont('Arial', 18, bold=True)
        count_text = font.render(f"{card_count}", True, (255, 255, 255))
        
        # Create a small background for the text
        text_bg = pygame.Surface((count_text.get_width() + 10, count_text.get_height() + 6), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 180))  # Semi-transparent black
        
        # Position the count in the top-right corner of the deck
        count_x = deck_x + deck_image.get_width() - count_text.get_width() - 15
        count_y = deck_y + 10
        
        # Draw background and text
        self.screen.blit(text_bg, (count_x - 5, count_y - 3))
        self.screen.blit(count_text, (count_x, count_y))
        
        # self.hand.render(center_x, y_position)
    
    def draw_card_from_deck(self, number_of_cards):
        """Draw a card from the deck"""
        cards_drawn = []
        for _ in range(number_of_cards):
            cards_drawn.append(self.cards_in_deck.pop(0))
        return cards_drawn