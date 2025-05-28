import pygame
import os
class SpriteUtil:
    def __init__(self, sprite_path):
        self.SPRITE_PATH = sprite_path
        self.sprite_sheet = self.load_sprite_sheet()

    def load_sprite_sheet(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # go up one level
        parent1 = os.path.dirname(dir_path)
        parent2 = os.path.dirname(parent1)
        return pygame.image.load(os.path.join(parent2, self.SPRITE_PATH)).convert_alpha()

    def draw_sprite_image_at(self, sprite_image, position = None):    
        if position is None:
            position = (0,0)
        return sprite_image.get_rect(center=position)

    def get_sprite(self, sprite_rect):
        try:
            rect = pygame.Rect(
                pygame.Rect(
                    sprite_rect[0], 
                    sprite_rect[1], 
                    sprite_rect[2], 
                    sprite_rect[3]))    
            image = pygame.Surface(rect.size, pygame.SRCALPHA)
            image.blit(self.sprite_sheet, (0, 0), rect)        
            return image
        except Exception as e:
            return None