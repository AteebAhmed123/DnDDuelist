import pygame

class SpriteUtil:
    def __init__(self, 
                 sprite_start_x, 
                 sprite_start_y, 
                 sprite_width, 
                 sprite_height, 
                 sprite_path):

        self.sprite_start_x = sprite_start_x
        self.sprite_start_y = sprite_start_y
        self.sprite_width = sprite_width  # Match the size used in GameManager
        self.sprite_height = sprite_height
        self.SPRITE_PATH = sprite_path

        self.sprite_sheet = self.load_sprite_sheet()

    def load_sprite_sheet(self):
        return pygame.image.load(self.SPRITE_PATH).convert_alpha()

    def get_sprite(self):
        try:
            rect = pygame.Rect(
                pygame.Rect(
                    self.sprite_start_x, 
                    self.sprite_start_y, 
                    self.sprite_width, 
                    self.sprite_height))    
            image = pygame.Surface(rect.size, pygame.SRCALPHA)
            image.blit(self.sprite_sheet, (0, 0), rect)        
            return image
        except Exception as e:
            print(f"Error creating image: {e}")
            return None
        

    def draw_sprite_image_at(self, sprite_image, position = None):    
        if position is None:
            position = (0,0)
        return sprite_image.get_rect(center=position)