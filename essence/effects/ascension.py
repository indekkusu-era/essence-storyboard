import os

from numpy.random import exponential, uniform
from numpy import pi
from utils.objects import Sprite, Move, MoveY, Fade, Scale, Loop, Color, Rotate, VectorScale
from utils.constants import SB_WIDTH, SB_HEIGHT, SB_LEFT, SB_RIGHT
from utils.midiparser.parser import get_timestamps_and_pitches, get_time_signatures

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

class AscendanceClimax:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    _comet = "sb/elements/meteor.png"
    def __init__(self, star_interarrival_time, comet_interarrival_time, star_time, comet_departure_time):
        self.star_interarrival_time = star_interarrival_time
        self.comet_interarrival_time = comet_interarrival_time
        self.comet_departure_time = comet_departure_time
        self.star_time = star_time

    def _black_cover(self, start, end):
        white = Sprite(self._white)
        white.add_action(Color(0, start, end, (0,0,0), (0,0,0)))
        white.add_action(Scale(0, start, end, 5, 5))
        return white
    
    def render(self, t_start, t_end):
        all_sprites = [self._black_cover(t_start, t_end)]
        # Stars
        t = t_start
        while t < t_end:
            sprite = Sprite(self._star)
            random_interarrival = exponential(self.star_interarrival_time)
            random_x = uniform(SB_LEFT, SB_RIGHT)
            random_scale = exponential(2)
            sprite.add_action(Scale(0, t, t + self.star_time, random_scale, random_scale))
            sprite.add_action(Move(0, t, t + self.star_time, (random_x, -20), (random_x, 500)))
            all_sprites.append(sprite)
            t += random_interarrival
        
        # Comets
        t = t_start
        rotation_axis = - pi / 2
        while t < t_end:
            sprite = Sprite(self._comet)
            random_interarrival = exponential(self.comet_interarrival_time)
            random_departure = exponential(self.comet_departure_time)
            random_x = uniform(SB_LEFT, SB_RIGHT)
            random_scale = exponential(1.2)
            sprite.add_action(VectorScale(0, t, t + random_departure, (random_scale, 2), (random_scale, 2)))
            sprite.add_action(Rotate(0, t, t + random_departure, rotation_axis, rotation_axis))
            sprite.add_action(Move(0, t, t + random_departure, (random_x, -20), (random_x, 500)))
            all_sprites.append(sprite)
            t += random_interarrival
        return all_sprites

class AscendanceClimax2:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    def __init__(self, midi_dir, bpm=None):
        self.midi_dir = midi_dir
        self.bpm = bpm

    def _black_cover(self, start, end):
        white = Sprite(self._white)
        white.add_action(Color(0, start, end, (0,0,0), (0,0,0)))
        white.add_action(Scale(0, start, end, 5, 5))
        return white

    def get_time_signatures(self, midifp, t_end):
        time_signatures = get_time_signatures(midifp, self.bpm)
        real_time_signatures = {}
        for k, v in time_signatures.items():
            if k >= t_end:
                continue
            real_time_signatures[k] = v
        return real_time_signatures
    
    def get_timestamps(self, midifp, t_end):
        timestamps, pitches = get_timestamps_and_pitches(midifp, self.bpm)
        real_timestamps = []
        real_pitches = []
        for track_ts, track_pitches in zip(timestamps.values(), pitches.values()):
            for ts, p in zip(track_ts, track_pitches):
                if ts >= t_end:
                    continue
                real_timestamps.append(ts)
                real_pitches.append(p)
        return real_timestamps, real_pitches
    
    def get_all_tracks_data(self, t_end):
        midilist = os.listdir(self.midi_dir)
        time_signatures = self.get_time_signatures(os.path.join(self.midi_dir, midilist[0]), t_end)
        timestamps = []
        pitches = []
        for midi in midilist:
            midi_fp = os.path.join(self.midi_dir, midi)
            track_ts, track_p = self.get_timestamps(midi_fp, t_end)
            timestamps += track_ts; pitches += track_p
        
        return time_signatures, (timestamps, pitches)

    def render(self, t_start, t_end):
        all_sprites = [self._black_cover(t_start, t_end)]
        time_signatures, (timestamps, pitches) = self.get_all_tracks_data(t_end - t_start)
        time_signature_changes = list(time_signatures.keys())
        bar_reset = time_signature_changes[::2] + [t_end - t_start]
        delta = [(bar_reset[i+1] - bar_reset[i]) for i in range(len(bar_reset) - 1)]
        min_pitches = min(pitches); max_pitches = max(pitches)
        for ts, p in zip(timestamps, pitches):
            prev_tps = list(filter(lambda x: x <= ts, bar_reset))
            current_interval = max(prev_tps); current_delta = delta[len(prev_tps) - 1]
            relative_pos_x = (ts - current_interval) / current_delta
            relative_pos_y = (p - min_pitches) / (max_pitches - min_pitches)
            x = SB_LEFT + (SB_RIGHT - SB_LEFT) * relative_pos_x
            y = relative_pos_y * 480
            sprite = Sprite(self._star)
            sprite.add_action(Move(0, t_start + ts, t_start + ts + 1000, (x, y), (x, y)))
            sprite.add_action(Scale(0, t_start + ts, t_start + ts + 500, 0, 2))
            sprite.add_action(Rotate(0, t_start + ts, t_start + ts + 500, -pi/2, 0))
            sprite.add_action(Scale(0, t_start + ts + 500, t_start + ts + 1000, 2, 0))
            sprite.add_action(Rotate(0, t_start + ts + 500, t_start + ts + 1000, 0, pi/2))
            all_sprites.append(sprite)
        return all_sprites
            

class AscendanceClimax3:
    ...
