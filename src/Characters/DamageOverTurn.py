from WeatherManager import WeatherType

class DamageOverTurn:
    def __init__(self, damage, turn, spell_type):
        self.damage = damage
        self.for_turns = turn
        self.spell_type = spell_type

    def apply_damage(self, target, weather_manager):
        if self.for_turns > 0:
            damange_multiplier = 1.0
            if  self.spell_type == "Fireball" and weather_manager.weather_type == WeatherType.HEAT:
                damange_multiplier = 3
            elif  self.spell_type == "WaterGeyser" and weather_manager.weather_type == WeatherType.RAIN:
                damange_multiplier = 3
            elif  self.spell_type == "WindSlash" and weather_manager.weather_type == WeatherType.WIND:
                damange_multiplier = 3
            elif  self.spell_type == "EarthSpike" and weather_manager.weather_type == WeatherType.EARTH:
                damange_multiplier = 3
            target.health.reduce_health(self.damage * damange_multiplier)
            self.for_turns = self.for_turns - 1
        else:
            self = None
            return False
        return True