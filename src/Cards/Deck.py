from Cards.AllDecks import AllDecks
from Cards.DuelistParadox import DuelistParadox
from Cards.MagicMissive import MagicMissive
from Cards.ThanosSnapCard import ThanosSnapCard
from Cards.CollapseBarrier import CollapseBarrier
from Cards.ElementalAfflication import ElementalAfflication
from Cards.ElementalWeather import ElementalWeather
from Cards.PhaseBias import PhaseBias
from Cards.QuantumTunneling import QuantumTunneling
from SpriteUtil.SpriteUtil import SpriteUtil
import random
import pygame

class Deck(AllDecks):

    POSSIBLE_CARDS = {
        DuelistParadox: 0.35,
        MagicMissive: 0.25,
        ThanosSnapCard: 0.25,
        CollapseBarrier: 0.25,
        ElementalAfflication: 0.25,  # Re-enabled for testing
        PhaseBias: 0.25,  # 10% chance for Phase Bias cards
        QuantumTunneling: 0.35  # Increased for testing
    }

    # POSSIBLE_CARDS = {
    #     DuelistParadox: 0.35,
    #     # MagicMissive: 0.15, 
    #     # # ThanosSnapCard: 0.20,
    #     CollapseBarrier: 0.35,
    #     # ElementalAfflication: 0.35,  # Re-enabled for testing
    #     # PhaseBias: 0.1,  # 10% chance for Phase Bias cards
    #     QuantumTunneling: 0.35  # Increased for testing
    #     # ElementalWeather: 0.5
    # }

    # POSSIBLE_CARDS = {
    #     DuelistParadox: 0.35,
    #     # MagicMissive: 0.15, 
    #     # # ThanosSnapCard: 0.20,
    #     CollapseBarrier: 0.35,
    #     # ElementalAfflication: 0.35,  # Re-enabled for testing
    #     # PhaseBias: 0.1,  # 10% chance for Phase Bias cards
    #     QuantumTunneling: 0.35  # Increased for testing
    #     # ElementalWeather: 0.5
    # }

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