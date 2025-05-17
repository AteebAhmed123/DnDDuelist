from Cards.Deck import Deck

class Hand:
    def __init__(self, screen):
        """Initialize a hand that can hold up to 5 cards"""
        self.screen = screen
        self.cards_in_hand = []
        self.max_cards = 4
        self.card_positions = []
        self.deck = Deck(screen)  # Store positions of cards for click detection
        self.bootstrap_cards_from_deck()
    
    def bootstrap_cards_from_deck(self):
        """Bootstrap cards from the deck"""
        self.cards_in_hand = self.deck.draw_card_from_deck(self.max_cards)
    
    def clear(self):
        """Remove all cards from the hand"""
        self.cards_in_hand = []
        self.card_positions = []

    def add_card(self, card):
        """Add a card to the hand"""
        if len(self.cards_in_hand) < self.max_cards:
            self.cards_in_hand.append(card)
    

    def remove_card(self, index):
        """Remove a card at the specified index"""
        if 0 <= index < len(self.cards_in_hand):
            self.cards_in_hand.pop(index)
            if index < len(self.card_positions):
                self.card_positions.pop(index)
            return True
        return False
    
    def handle_click(self, mouse_pos):
        """Handle click on cards, return index of clicked card or -1"""
        for i, card in enumerate(self.cards_in_hand):
            if card.is_clicked(mouse_pos):
                print(f"Card {i} clicked!")
                return i
        return -1
    
    def render(self, center_x, y_position):
        """Render all cards in the hand side by side"""
        if not self.cards_in_hand:
            return
        start_x = center_x
        
        # Render each card
        for i, card in enumerate(self.cards_in_hand):
            x_pos = start_x + (145*i)
            card.render((x_pos, y_position))
            self.card_positions.append((x_pos, y_position)) 