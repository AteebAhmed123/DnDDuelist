from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil

class DuelistParadox(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/DuelistParadox.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)

    def get_sprite_coords(self):
        return self.CARD_COORDS