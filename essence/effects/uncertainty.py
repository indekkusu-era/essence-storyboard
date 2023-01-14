import numpy as np
from utils.midiparser.parser import get_timestamps_and_pitches
from utils.objects.actions import Move, Rotate, VectorScale
from utils.objects import Sprite
from utils.constants import SB_UPPER, SB_LOWER, SB_LEFT, SB_RIGHT

class Uncertainty:
    _default_sprite = "sb/elements/meteor.png"
    _bullet_interval = 500
    def __init__(self, midi_fp):
        self.midi_fp = midi_fp

    def bullet_effect(self, t, position):
        initial_position = (position * (SB_RIGHT - SB_LEFT) + SB_LEFT + 100, SB_UPPER - 20)
        end_position = (position * (SB_RIGHT - SB_LEFT) + SB_LEFT - 100, SB_LOWER + 20)
        rotation_angle = -np.arctan((SB_LOWER - SB_UPPER + 40) / 200)
        return [
            VectorScale(0, t, t+self._bullet_interval, (0.2, 1), (0.2, 1)),
            Rotate(0, t, t+self._bullet_interval, rotation_angle, rotation_angle),
            Move(0, t, t+self._bullet_interval, initial_position, end_position)
        ]

    def render(self, t_start):
        timestamps, pitches = get_timestamps_and_pitches(self.midi_fp)
        timestamps = timestamps[1] + timestamps[2]; pitches = pitches[1] + pitches[2]
        maxpitch = max(pitches); minpitch = min(pitches)
        pitches = [(p - minpitch) / (maxpitch - minpitch) for p in pitches]
        all_sprites = []
        for t, p in zip(timestamps, pitches):
            relative_t = int(t_start + t)
            effects = self.bullet_effect(relative_t, p)
            sprite = Sprite(self._default_sprite)
            sprite.add_actions(effects)
            all_sprites.append(sprite)
        return all_sprites
