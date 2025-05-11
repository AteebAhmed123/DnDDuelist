import pygame

class SpriteUtil:
    def __init__(self, sprite_path):
        self.SPRITE_PATH = sprite_path
        self.sprite_sheet = self.load_sprite_sheet()

    def load_sprite_sheet(self):
        return pygame.image.load(self.SPRITE_PATH).convert_alpha()

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
            print(f"Error creating image: {e}")
            return None
    