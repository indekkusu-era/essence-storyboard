import numpy as np
from typing import Dict, Tuple

from numpy.random import exponential, uniform, randint
from utils.objects import Sprite, Move, Fade, VectorScale, Scale, Color, Rotate, MoveX, MoveY, Loop
from utils.constants import SB_WIDTH, SB_HEIGHT, SB_LEFT, SB_RIGHT, SB_LOWER, SB_UPPER
from utils.midiparser.parser import get_timestamps_and_pitches, get_time_signatures
from effects.uncertainty import Uncertainty

from .constellation import ConstellationAnimation

def essence():
    essence_sprite = Sprite('sb/elements/orb.png')
    return essence_sprite

def background():
    ...

def true_essence_1(start, fade_out_start, end, vertices, parents):
    constellation = ConstellationAnimation(vertices, parents)
    constellation_render = constellation.render(fade_out_start)
    for i in range(len(constellation_render)):
        for action in constellation_render[i].actions:
            if action.event_type == "M":
                mx, my = action.params[:2]
                constellation_render[i].add_actions([
                    Move(0, fade_out_start, end, (mx, my), (320, 240))
                ])
        if constellation_render[i].filename == constellation._star:
            constellation_render[i].add_actions([
                Scale(0, fade_out_start, end, 2, 0)
            ])
        else:
            for action in constellation_render[i].actions:
                if action.event_type == "V":
                    vector_x, vector_y = action.params[:2]
                    constellation_render[i].add_actions([
                        VectorScale(0, fade_out_start, end, (vector_x, vector_y), (0,0))
                    ])
    return constellation_render

def true_essence_2(start, midi_file, bpm):
    hexagon = 'sb/elements/hexagon.png'
    timestamps = get_timestamps_and_pitches(midi_file, bpm)[0]
    max_ts = max(timestamps)
    all_sprites = []
    for timestamp in timestamps:
        hex_ = Sprite(hexagon)
        pos = (uniform(SB_LEFT, SB_RIGHT), uniform(SB_UPPER, SB_LOWER))
        timestamp += start
        hex_.add_actions([
            Move(0, start, max_ts, pos, pos),
            Scale(0, timestamp, timestamp + 1000, 0, 0.2),
            Fade(0, timestamp, timestamp + 500, 0, 1),
            Fade(0, timestamp+500, timestamp+1000, 1, 0)
        ])
        all_sprites.append(hex_)
    return all_sprites

def true_essence_3(start, midi_file):
    uncertainty = Uncertainty(midi_file)
    return uncertainty.render(start)

def true_essence_4(start, midi_file):
    uncertainty = Uncertainty(midi_file)
    return uncertainty.render(start)

def true_essence_5(start, end):
    ...

def true_essence_6(start, end):
    ...

def true_essence_7(start, end):
    ...

def true_essence_8(start, end):
    ...
