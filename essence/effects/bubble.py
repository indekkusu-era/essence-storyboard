import numpy as np
from numpy.random import uniform, exponential
from utils.objects import Sprite, Move, MoveY, Fade, Scale, Loop, Color
from utils.constants import SB_WIDTH, SB_HEIGHT

class Bubble:
    _bubbl = 'sb/elements/orb.png'
    def __init__(self, n_particles):
        self._n_particles = n_particles
    
    def render(self, start: int, end: int, loop_period=5000):
        sprites = []
        for _ in range(self._n_particles):
            bub_pos = uniform(-108, 746)
            start_time = uniform(loop_period) + start
            loop_period_ = uniform(loop_period // 2, loop_period)
            bubl = Sprite(self._bubbl)
            bubl.add_action(Scale(0, start, end, 0.01, 0.01))
            actions = [
                Move(0, 0, loop_period_, (bub_pos, SB_HEIGHT+20), (bub_pos, 0)),
                Fade(2, 0, loop_period_, 1, 0)
            ]
            loop = Loop(int(start_time), int((end - start_time) // loop_period_), actions)
            bubl.add_action(loop)
            sprites.append(bubl)
        return sprites
