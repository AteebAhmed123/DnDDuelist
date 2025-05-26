from Cards.AllDecks import AllDecks
from Cards.DuelistParadox import DuelistParadox
from Cards.MagicMissive import MagicMissive
from Cards.ThanosSnapCard import ThanosSnapCard
from Cards.CollapseBarrier import CollapseBarrier
from Cards.ElementalAfflication import ElementalAfflication
from Cards.ElementalWeather import ElementalWeather
from SpriteUtil.SpriteUtil import SpriteUtil
import random
import pygame

class Deck(AllDecks):

    POSSIBLE_CARDS = {
        # DuelistParadox: 0.3,
        # MagicMissive: 0.35, 
        # ThanosSnapCard: 0.05,
        # CollapseBarrier: 0.3,
        ElementalWeather: 1
    }

    X_OFFSET = 500
    Y_OFFSET = -175
    
    def __init__(self, screen):
        """Initialize a deck with up to 20 cards"""
        super().__init__(screen, 20, "./Assets/Cards/deck.png", (0, 0, 130, 200))
        # self.screen = screen
        # self.cards_in_deck = []
        # self.max_cards = 20
        # # self.hand = Hand(screen)
        
        # # Initialize deck sprite
        # self.SPRITE_PATH = "./Assets/Cards/deck.png"
        # self.sprite = SpriteUtil(self.SPRITE_PATH)
        # self.deck_coords = (0, 0, 130, 200)  # Adjust based on your sprite dimensions
        # # Initialize with some default cards
        self._initialize_default_cards()