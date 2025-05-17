from Cards.DuelistParadox import DuelistParadox
from Cards.BlastAllVsBlastMe import BlastAllVsBlastMe
from Cards.ReflectOrGain import ReflectOrGain
from SpriteUtil.SpriteUtil import SpriteUtil
import random
class Deck:

    POSSIBLE_CARDS = [
        DuelistParadox,
        ReflectOrGain,
        BlastAllVsBlastMe
    ]
    
    def __init__(self, screen):
        """Initialize a deck with up to 20 cards"""
        self.screen = screen
        self.cards_in_deck = []
        self.max_cards = 20
        # self.hand = Hand(screen)
        
        # Initialize deck sprite
        self.SPRITE_PATH = "./Assets/Cards/deck.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.deck_coords = (0, 0, 130, 200)  # Adjust based on your sprite dimensions
        # Initialize with some default cards
        self._initialize_default_cards()

        
    def _initialize_default_cards(self):
        """Add some default cards to the deck"""
        # Add 3 copies of each card type for a total of 9 cards
        for _ in range(0, self.max_cards):
            card_class = random.choice(self.POSSIBLE_CARDS)
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
        deck_x = self.screen.get_width() - 180  # 20px margin from right edge
        deck_y = self.screen.get_height() - 230  # 20px margin from bottom edge
        self.screen.blit(deck_image, (deck_x, deck_y))
        
        # self.hand.render(center_x, y_position)
    
    def draw_card_from_deck(self, number_of_cards):
        """Draw a card from the deck"""
        cards_drawn = []
        for _ in range(number_of_cards):
            cards_drawn.append(self.cards_in_deck.pop(0))
        return cards_drawn

        
    # def draw_hand(self):
    #     """Draw the first 5 cards from the deck to the hand"""
    #     self.hand.clear()
    #     cards_to_draw = 4
        
    #     for i in range(cards_to_draw):
    #         self.hand.add_card(self.cards[i])