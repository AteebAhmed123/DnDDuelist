from Cards.CardBlueprint import CardBlueprint
from SpriteUtil.SpriteUtil import SpriteUtil
from Spells.Lightning import Lightning
class DuelistParadox(CardBlueprint):
    # Define sprite coordinates for the card
    CARD_COORDS = (0, 0, 250, 350)  # Assuming the card takes up the full sprite
    name = "Duelist's Paradox"
    description = "Strikes the opponent with lightning, dealing 10 damage."
    damage = 10
    

    def __init__(self, screen):
        super().__init__(screen)
        self.SPRITE_PATH = "./Assets/Cards/DuelistParadox.png"
        self.sprite = SpriteUtil(self.SPRITE_PATH)
        self.spell = Lightning(self.screen)
        self.activated_card = False

    def get_sprite_coords(self):
        return self.CARD_COORDS
    
    def activate_card(self, caster, target):
        return self.apply_affect(caster, target)


    def apply_affect(self, caster, target):
        return self.spell.animate_spell(caster, target)
        
    