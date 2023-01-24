import numpy as np
from typing import Dict, Tuple

from numpy.random import exponential, uniform, randint
from utils.objects import Sprite, Move, Fade, VectorScale, Scale, Color, Rotate, MoveX, MoveY, Loop
from utils.constants import SB_WIDTH, SB_HEIGHT, SB_LEFT, SB_RIGHT, SB_LOWER, SB_UPPER
from utils.midiparser.parser import get_timestamps_and_pitches, get_time_signatures

class ConstellationAnimation:
    _star = "sb/elements/star.png"
    _line = "sb/elements/line.png"
    def __init__(self, vertices_positions_timestamps: Dict[Tuple[float], int], parents: Dict[int, list[int]]):
        self._vertices_timestamps = vertices_positions_timestamps
        self._parents = parents
    
    @property
    def positions(self):
        return list(self._vertices_timestamps.keys())

    @classmethod
    def lines(self, start, end, pos1: Tuple[float], pos2: Tuple[float]):
        line = Sprite(self._line, 'CentreLeft')
        x, y = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan(y / x)
        if x < 0:
            theta += np.pi
        scalex = r / 121
        line.add_action(Move(0, start, end, pos1, pos1))
        line.add_action(VectorScale(0, start, end, (scalex, 1), (scalex, 1)))
        line.add_action(Rotate(0, start, end, theta, theta))
        line.add_action(Fade(0, end, end+1, 1, 0))
        return line

    def render(self, end):
        all_sprites = []
        for (pos, timestamp), (_id, predecessors) in zip(self._vertices_timestamps.items(), enumerate(self._parents)):
            star = Sprite(self._star)
            star.add_action(Scale(0, timestamp, end, 2, 2))
            star.add_action(Move(0, timestamp, end, pos, pos))
            for predecessor in predecessors:
                pred_position = self.positions[predecessor]
                all_sprites.append(self.lines(timestamp, end, pos, pred_position))
            all_sprites.append(star)
        return all_sprites

