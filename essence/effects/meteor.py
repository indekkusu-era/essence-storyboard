from numpy.random import uniform, exponential
from utils.constants import SB_UPPER, SB_RIGHT, SB_LOWER, SB_LEFT
from utils.objects.sprite import Sprite
from utils.objects.actions import Rotate, Move
import numpy as np

class Meteor:
    _meteor = "sb/elements/meteor.png"
    def __init__(self, arrival_time: int, departure_time: int):
        self.expected_arrival_time = arrival_time
        self.expected_departure_time = departure_time

    def meteor(self, t, position):
        initial_position = (position * (SB_RIGHT - SB_LEFT) + SB_LEFT + 100, SB_UPPER - 20)
        end_position = (position * (SB_RIGHT - SB_LEFT) + SB_LEFT - 100, SB_LOWER + 20)
        rotation_angle = -np.arctan((SB_LOWER - SB_UPPER + 40) / 200)
        dep = self.expected_departure_time
        return [
            Rotate(0, t, t+dep, rotation_angle, rotation_angle),
            Move(0, t, t+dep, initial_position, end_position)
        ]

    def render(self, start, end):
        all_sprites = []
        t = start
        while t < end:
            arr = exponential(self.expected_arrival_time)
            meteor = Sprite(self._meteor)
            meteor.add_actions(self.meteor(t, uniform(0, 1)))
            all_sprites.append(meteor)
            t += arr
        return all_sprites
        