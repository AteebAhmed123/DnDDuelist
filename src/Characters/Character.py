from pygame.sprite import Sprite
from abc import ABC, abstractmethod

class CharacterBlueprint(Sprite):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def initialise_sprite(self, sprite_path):
        pass
    