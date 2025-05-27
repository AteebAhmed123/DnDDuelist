from enum import Enum
from Spells.ElementalWeather.Rain import Rain
from Spells.ElementalWeather.WindTornado import WindTornado
from Spells.ElementalWeather.Heatwave import HeatWave
from Spells.ElementalWeather.Earthquake import Earthquake 

class WeatherManager:

    def __init__(self, turn_indicator):
        self.weather_active_turns = 0
        self.turn_indicator = turn_indicator
        self.weather_spell = None
        self.weather_type = None
        self.turn_at_spell_start = 0

    def set_active_weather(self, weather_spell, weather_active_turns):
        self.stop_weather()
        self.weather_spell = weather_spell
        self.weather_active_turns = weather_active_turns
        self.turn_at_spell_start = self.turn_indicator.get_total_turns()

        if (type(weather_spell) == Rain):
            self.weather_type = WeatherType.RAIN
        elif (type(weather_spell) == WindTornado):
            self.weather_type = WeatherType.WIND
        elif (type(weather_spell) == HeatWave):
            self.weather_type = WeatherType.HEAT
        elif (type(weather_spell) == Earthquake):
            self.weather_type = WeatherType.EARTH

        self.start_weather()

    def get_weather_type(self):
        return self.weather_type

    def start_weather(self):
        self.weather_spell.start()

    def animate_weather(self):
        if (self.weather_spell != None):
            if self.is_weather_over():
                self.stop_weather()
                return
            self.weather_spell.animate_spell()
        
    def is_weather_over(self):
        current_turn = self.turn_indicator.get_total_turns()
        if (current_turn > self.turn_at_spell_start + self.weather_active_turns):
            return True

        return False

    def stop_weather(self):
        if self.weather_spell != None:
            self.weather_spell.stop()
            self.weather_spell = None

class WeatherType(Enum):
    RAIN = 0
    WIND = 1
    HEAT = 2
    EARTH = 3

