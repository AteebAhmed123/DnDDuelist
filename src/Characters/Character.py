from pygame.sprite import Sprite
from abc import ABC, abstractmethod

class CharacterBlueprint(Sprite):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_sprites(self):
        pass

    @abstractmethod
    def animate(self, deck_position):
        pass
    
    @abstractmethod
    def attack(self):
        pass