import pygame
from pygame.sprite import Sprite
from SpriteUtil.SpriteUtil import SpriteUtil

class HealthBar(SpriteUtil):
    def __init__(self):
        self.health = 100
        self.SPRITE_HEALTH_BACKGROUND_PATH = "./Assets/Health/healthbackground.png"
        self.SPRITE_PATH = "./Assets/Health/healthbar.png"

    def reduce_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def increase_health(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100