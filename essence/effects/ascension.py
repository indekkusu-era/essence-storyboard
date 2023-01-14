from numpy.random import exponential, uniform
from .rain import Rain
from utils.objects import Sprite, Move, MoveY, Fade, Scale, Loop, Color
from utils.constants import SB_WIDTH, SB_HEIGHT, SB_LEFT, SB_RIGHT

class Ascendance:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    def __init__(self, expected_interarrival_time=200, expected_service_time=198):
        self._expected_interarrival_time = expected_interarrival_time
        self._expected_service_time = expected_service_time

    def _black_cover(self, start, end):
        white = Sprite(self._white)
        white.add_action(Color(0, start, end, (0,0,0), (0,0,0)))
        white.add_action(Scale(0, start, end, 5, 5))
        return white
    
    def random_interarrival(self):
        return exponential(self._expected_interarrival_time)
    
    def random_service(self):
        return exponential(self._expected_service_time)
    
    def arrival(self, arrival_time: int, arrival_pos: tuple):
        return [
            Move(0, arrival_time - 1000, arrival_time, arrival_pos, arrival_pos), 
            Fade(0, arrival_time - 1000, arrival_time, 0, 1),
            Scale(0, arrival_time - 1000, arrival_time, 0, 1.8)
        ]
    
    def departure(self, departure_time: int):
        return [
            Fade(0, departure_time, departure_time + 1000, 1, 0)
        ]

    def render(self, start, zoom_up, end):
        all_sprites = [self._black_cover(start, end)]
        t = start
        last_departure = t
        while t < zoom_up:
            # Generate the Discrete Event System in order to obtain the Expectation
            # It is necessary to do the Simulation when the system is sophisticated and can't be computed EXPLICITLY
            interarrival_time = t + self.random_interarrival()
            departure = max(last_departure, t) + self.random_service()
            x = uniform(SB_LEFT, SB_RIGHT)
            y = uniform(0, SB_HEIGHT)
            sprite = Sprite(self._star)
            sprite.add_actions(self.arrival(t, (x, y)))
            if departure + 1000 < zoom_up:
                sprite.add_actions(self.departure(departure))
            else:
                sprite.add_action(Fade(0, zoom_up, zoom_up + 1, 1, 0))
            all_sprites.append(sprite)
            t = interarrival_time
            last_departure = departure
        
        t = zoom_up
        while t < end:
            sprite = Sprite(self._star)
            random_x = uniform(SB_LEFT, SB_RIGHT)
            interarrival_time = int(t + exponential(20))
            interval = (5 - 4 * (t - zoom_up) / (end - zoom_up)) * 200
            sprite.add_action(Scale(0, t, t + interval, 2, 2))
            sprite.add_action(Move(0, t, t + interval, (random_x, -20), (random_x, 500)))
            all_sprites.append(sprite)
            t = interarrival_time
        
        return all_sprites
