from Characters.Character import CharacterBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
import pygame
import os

class Mage(CharacterBlueprint):
    def __init__(self):
        super().__init__()
        self.SPRITE_PATH = "./Assets/mage_sprite.png"
        self.sprite = SpriteUtil(51, 4, 78, 95, self.SPRITE_PATH)


    def image_at(self, position_to_draw = None):
        sprite_image = self.sprite.get_sprite()
        print(sprite_image)
        placement_sprite_image = self.sprite.draw_sprite_image_at(sprite_image, position_to_draw)
        return sprite_image, placement_sprite_image
