from Cards.DuelistParadox import DuelistParadox
from Cards.BlastAllVsBlastMe import BlastAllVsBlastMe
from Cards.ReflectOrGain import ReflectOrGain
from SpriteUtil.SpriteUtil import SpriteUtil

class Deck:
    def __init__(self, screen):
        """Initialize a deck with up to 20 cards"""
        self.screen = screen
        self.cards = []
        self.max_cards = 20
        self.hand = Hand(screen)
        
        # Initialize deck sprite
        self.SPRITE_PATH = "./Assets/Cards/deck.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.deck_coords = (0, 0, 130, 200)  # Adjust based on your sprite dimensions
        
        # Initialize with some default cards
        self._initialize_default_cards()
    
    def _initialize_default_cards(self):
        """Add some default cards to the deck"""
        # Add 3 copies of each card type for a total of 9 cards
        for _ in range(4):
            self.add_card(DuelistParadox(self.screen))
            self.add_card(ReflectOrGain(self.screen))
            self.add_card(BlastAllVsBlastMe(self.screen))
            self.add_card(BlastAllVsBlastMe(self.screen))
    
    def add_card(self, card):
        """Add a card to the deck if there's room"""
        if len(self.cards) < self.max_cards:
            self.cards.append(card)
            return True
        return False
    
    def draw_hand(self):
        """Draw the first 5 cards from the deck to the hand"""
        self.hand.clear()
        cards_to_draw = 4
        
        for i in range(cards_to_draw):
            self.hand.add_card(self.cards[i])
    
    def render(self, center_x, y_position):
        """Render the current hand of cards and the deck sprite"""
        # Render the hand
        # Render the deck sprite at bottom right
        deck_image = self.sprite.get_sprite(self.deck_coords)
        deck_x = self.screen.get_width() - 180  # 20px margin from right edge
        deck_y = self.screen.get_height() - 230  # 20px margin from bottom edge
        self.screen.blit(deck_image, (deck_x, deck_y))
        
        self.hand.render(center_x, y_position)
        

class Hand:
    def __init__(self, screen):
        """Initialize a hand that can hold up to 5 cards"""
        self.screen = screen
        self.cards = []
        self.max_cards = 4
        self.card_positions = []  # Store positions of cards for click detection
    
    def add_card(self, card):
        """Add a card to the hand if there's room"""
        if len(self.cards) < self.max_cards:
            self.cards.append(card)
            return True
        return False
    
    def clear(self):
        """Remove all cards from the hand"""
        self.cards = []
        self.card_positions = []
    
    def remove_card(self, index):
        """Remove a card at the specified index"""
        if 0 <= index < len(self.cards):
            self.cards.pop(index)
            if index < len(self.card_positions):
                self.card_positions.pop(index)
            return True
        return False
    
    def handle_click(self, mouse_pos):
        """Handle click on cards, return index of clicked card or -1"""
        for i, card in enumerate(self.cards):
            if card.is_clicked(mouse_pos):
                print(f"Card {i} clicked!")
                return i
        return -1
    
    def render(self, center_x, y_position):
        """Render all cards in the hand side by side"""
        if not self.cards:
            return
        start_x = center_x
        
        # Render each card
        for i, card in enumerate(self.cards):
            x_pos = start_x + (145*i)
            card.render((x_pos, y_position))
            self.card_positions.append((x_pos, y_position)) 