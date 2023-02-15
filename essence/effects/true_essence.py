import numpy as np
from typing import Dict, Tuple
from copy import deepcopy

from numpy.random import exponential, uniform, choice
from utils.objects import Sprite, Move, Fade, VectorScale, Scale, Color, Rotate, MoveX, MoveY, Loop
from utils.constants import SB_WIDTH, SB_HEIGHT, SB_LEFT, SB_RIGHT, SB_LOWER, SB_UPPER
from utils.midiparser.parser import get_timestamps_and_pitches, get_time_signatures
from essence.config import constellation_vertices_timestamps, essence_constellation_edges_pred
from .uncertainty import Uncertainty
from .stars import Plexus3D
from .orb_rotation import OrbRotation
from .bubble import Bubble

from .constellation import ConstellationAnimation

def background():
    gradient = Sprite('sb/backgrounds/gradient.png')
    gradient.add_actions([
        Scale(0, 335785, 374399, 1.5, 1.5),
        Color(0, 335785, 336781, (0,0,0), (69,0,0)),
        Color(0, 344340, 365257, (0,0,60), (0,0,255)),
        Color(0, 365257, 371371, (0,0,255), (255,0,0)),
        Color(0, 374399, 374400, (0,0,0), (0,0,0))
    ])
    return [gradient]

def true_essence_1(start, fade_out_start, end):
    ts = constellation_vertices_timestamps.copy()
    for k in ts.keys():
        ts[k] = start
    constellation = ConstellationAnimation(ts, essence_constellation_edges_pred)
    constellation_render = constellation.render(fade_out_start)
    for i in range(len(constellation_render)):
        for action in constellation_render[i].action.copy():
            if action.event_type == "M":
                mx, my = action.params[:2]
                constellation_render[i].add_actions([
                    Move(0, fade_out_start, end, (mx, my), (320, 240))
                ])
                break
        if constellation_render[i].filename == constellation._star:
            constellation_render[i].add_actions([
                Scale(0, fade_out_start, end, 2, 0)
            ])
        else:
            for action in constellation_render[i].action.copy():
                if action.event_type == "V":
                    vector_x, vector_y = action.params[:2]
                    constellation_render[i].add_actions([
                        VectorScale(0, fade_out_start, end, (vector_x, vector_y), (0,0))
                    ])
    bubbles = Bubble(50).render(start, end, 4500)
    black = Sprite("sb/backgrounds/black.png")
    black.add_action(Fade(0, start, end, 0.4, 0.4))
    return bubbles + [black] + constellation_render

def true_essence_2(start, midi_file):
    hexagon = 'sb/elements/hexagon.png'
    timestamps = get_timestamps_and_pitches(midi_file)
    timestamps = timestamps[0][1]
    max_ts = max(timestamps)
    all_sprites = []
    for timestamp in timestamps:
        hex_ = Sprite(hexagon)
        pos = (uniform(SB_LEFT, SB_RIGHT), uniform(SB_UPPER, SB_LOWER))
        timestamp += start
        hex_.add_actions([
            Move(0, start, start + max_ts, pos, pos),
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

def true_essence_5(start, plexus_appear, end):
    plexus = Plexus3D(800).render(start, end)
    filtered_plexus = []
    for i in range(len(plexus)):
        vectorscale_actions = list(filter(lambda x: x.event_type == 'V' and x.end_time < end, plexus[i].action))
        if 'line' not in plexus[i].filename:
            filtered_plexus.append(plexus[i])
            continue
        if len(plexus[i].action) == 0:
            continue
        if max(vectorscale_actions, key=lambda x: x.end_time).end_time < plexus_appear + 2000:
            continue
        filtered_plexus.append(plexus[i])
        filtered_plexus[-1].add_action(Fade(0, plexus_appear, plexus_appear + 2000, 0, 1))
    return filtered_plexus

def true_essence_6(start, end):
    essence_orbit = OrbRotation(40).render(start, end, 0.0008, 0.002, 0.003)
    essence_red = Sprite('sb/elements/essence_red.png')
    essence_red.add_actions(essence_orbit[-1].action.copy())
    essence_orbit[-1].add_action(Fade(0, start // 4 + end // 4 * 3, end, 1, 0))
    essence_red.add_action(Fade(0, (start + end) // 2, start // 4 + end // 4 * 3, 0, 1))
    return essence_orbit + [essence_red]

def divide_screen(sprites: list[Sprite], divisors: int, offset: int, time_scale=1):
    # normalizing the sb
    new_sprites = []
    scale_down = 1 / (divisors ** 2)
    relative_left = SB_LEFT - 320
    relative_right = SB_RIGHT - 320
    relative_top = SB_UPPER - 240
    relative_bottom = SB_LOWER - 240
    xdiv = (relative_right - relative_left) / divisors
    ydiv = (relative_bottom - relative_top) / divisors
    for row in range(divisors):
        for column in range(divisors):
            x_left = relative_left + column * xdiv
            y_top = relative_top + row * ydiv
            x_right = relative_left + (column + 1) * xdiv
            y_bottom = relative_top + (row + 1) * ydiv
            for sprite in sprites.copy():
                new_sprite = deepcopy(sprite)
                new_action = []
                for action in new_sprite.action:
                    if action.event_type in ["S", "V"]:
                        for i in range(len(action.params)):
                            action.params[i] *= np.sqrt(scale_down)
                    elif action.event_type == "M":
                        old_rel_x_start, old_rel_y_start = action.x_start - 320, action.y_start - 240
                        old_rel_x_end, old_rel_y_end = action.x_end - 320, action.y_end - 240
                        normalized_old_rel_x_start = (old_rel_x_start - relative_left) / (relative_right - relative_left)
                        normalized_old_rel_y_start = (old_rel_y_start - relative_top) / (relative_bottom - relative_top)
                        normalized_old_rel_x_end = (old_rel_x_end - relative_left) / (relative_right - relative_left)
                        normalized_old_rel_y_end = (old_rel_y_end - relative_top) / (relative_bottom - relative_top)
                        x_start = x_left + (x_right - x_left) * normalized_old_rel_x_start + 320
                        y_start = y_top + (y_bottom - y_top) * normalized_old_rel_y_start + 240
                        x_end = x_left + (x_right - x_left) * normalized_old_rel_x_end + 320
                        y_end = y_top + (y_bottom - y_top) * normalized_old_rel_y_end + 240
                        action.params = [x_start, y_start, x_end, y_end]
                    old_start_time = action.start_time
                    action.start_time = int(offset)
                    action.end_time = int(offset + (action.end_time - old_start_time) * time_scale)
                    new_action.append(action)
                new_sprite.action = new_action
                new_sprites.append(new_sprite)
    return new_sprites

def supernova(p1, p2, p3, pend):
    essence1 = Sprite('sb/elements/essence_red.png')
    essenceboom = Sprite('sb/elements/essence_red.png')
    essence1.add_action(Move(0, p1, p2, (320, 240), (320, 240)))
    essence1.add_action(Scale(0, p1, p2, 0.2, 0.2))
    essenceboom.add_action(Move(0, p1, p2, (320, 240), (320, 240)))
    essenceboom.add_action(Fade(0, p1, p2, 0.3, 0.3))
    essenceboom.add_action(Scale(0, p1, p2, 0.2, 2.8))
    initial_sprite = [essence1, essenceboom]
    for _ in range(20):
        star = Sprite('sb/elements/star.png')
        x = uniform(SB_LEFT, SB_RIGHT)
        y = uniform(SB_UPPER, SB_LOWER)
        star.add_action(Move(0, p1, p2, (x, y), (x, y)))
        star.add_action(Scale(0, p1, p2, 1.8, 1.8))
        initial_sprite.append(star)
    all_sprites = initial_sprite.copy()
    all_sprites.extend(divide_screen(initial_sprite, 2, p2, (p3 - p2) / (p2 - p1)))
    all_sprites.extend(divide_screen(initial_sprite, 4, p3, (pend - p3) / (p2 - p1)))
    return all_sprites

def essence_orb():
    orb = Sprite('sb/elements/orb.png')
    orb.add_actions([
        Scale(0, 320470, 321470, 0, 0.1),
        Scale(0, 344340, 344341, 0.1, 0)
    ])
    return orb

def true_essence():
    true_essence_elements = [essence_orb()] + true_essence_1(311936, 320205, 320470) + \
        true_essence_2(320470, 'assets/chiptune.mid') + \
        true_essence_3(328782, 'assets/xi.mid') + \
        true_essence_4(336781, 'assets/artcore.mid') + \
        true_essence_5(344340, 351558, 358565) + \
        true_essence_6(358565, 371371) + \
        supernova(371371, 372128, 372885, 374399) # + \
        # true_essence_7(365257, 371371)
    return true_essence_elements + background()
