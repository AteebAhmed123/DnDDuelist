from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil

class BlastAllVsBlastMe(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Using same dimensions as DuelistParadox

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/UncertaintyBomb.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)

    def get_sprite_coords(self):
        return self.CARD_COORDS 