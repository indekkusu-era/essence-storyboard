import os

from numpy.random import exponential, uniform, choice
from numpy import pi, cos, sin
from utils.objects import Sprite, Move, Fade, Scale, Color, Rotate, MoveX, MoveY, Loop
from utils.constants import SB_WIDTH, SB_HEIGHT, SB_LEFT, SB_RIGHT, SB_LOWER, SB_UPPER
from utils.midiparser.parser import get_timestamps_and_pitches, get_time_signatures

class Ascendance:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    def __init__(self, expected_interarrival_time=200, expected_service_time=198):
        self._expected_interarrival_time = expected_interarrival_time
        self._expected_service_time = expected_service_time
    
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
        all_sprites = []
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
    
class AscendanceBuildUp:
    def __init__(self, n_star_per_generate: int, generating_timestamps: list[int], disappear_timestamps: list[int]):
        self.n_star_per_generate = n_star_per_generate
        self.generating_timestamps = generating_timestamps
        self.disappear_timestamps = disappear_timestamps
    
    def render(self):
        all_sprites = []
        for ts in self.generating_timestamps:
            for _ in range(self.n_star_per_generate):
                star = Sprite('sb/elements/star.png')
                x = uniform(SB_LEFT, SB_RIGHT)
                y = uniform(SB_UPPER, SB_LOWER)
                end = choice(self.disappear_timestamps)
                star.add_actions([
                    Scale(0, ts, end, 1.8, 1.8),
                    Move(0, ts, end, (x, y), (x, y)),
                    Scale(0, end, end + 1, 1.8, 0)
                ])
                all_sprites.append(star)
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
    
    def render(self, t_start, t_end):
        all_sprites = []
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
        
        return all_sprites

class AscendanceClimax2:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    def __init__(self, midi_dir, bpm=None):
        self.midi_dir = midi_dir
        self.bpm = bpm

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
        all_sprites = []
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
    _white = 'sb/white/white.png'
    def __init__(self, timestamps, n_pairs):
        self.timestamps = timestamps
        self.n_pairs = n_pairs

    def create_horizontal_helix(self, timestamp, pos_y, radius, initial_x, dest_x, offset):
        star1 = Sprite("sb/elements/star.png")
        # star2 = Sprite("sb/elements/star.png")
        star1.add_action(MoveX(0, timestamp + offset, timestamp + offset + 400, initial_x, dest_x))
        # star2.add_action(MoveX(0, timestamp + offset, timestamp + offset + 400, initial_x, dest_x))
        helix_loop_actions_1 = [
            MoveY(17, 0, 100, pos_y - radius / 2, pos_y + radius / 2),
            MoveY(17, 100, 200, pos_y + radius / 2, pos_y - radius / 2)
        ]
        # helix_loop_actions_2 = [
        #     MoveY(17, 0, 100, pos_y + radius / 2, pos_y - radius / 2),
        #     MoveY(17, 100, 200, pos_y - radius / 2, pos_y + radius / 2)
        # ]
        loop1 = Loop(timestamp + offset, 2, helix_loop_actions_1)
        # loop2 = Loop(timestamp + offset, 2, helix_loop_actions_2)
        star1.add_action(loop1)
        # star2.add_action(loop2)
        return [star1]

    def create_vertical_helix(self, timestamp, pos_x, radius, initial_y, dest_y, offset):
        star1 = Sprite("sb/elements/star.png")
        # star2 = Sprite("sb/elements/star.png")
        star1.add_action(MoveY(0, timestamp + offset, timestamp + offset + 400, initial_y, dest_y))
        # star2.add_action(MoveY(0, timestamp + offset, timestamp + offset + 400, initial_y, dest_y))
        helix_loop_actions_1 = [
            MoveX(17, 0, 100, pos_x - radius / 2, pos_x + radius / 2),
            MoveX(17, 100, 200, pos_x + radius / 2, pos_x - radius / 2)
        ]
        # helix_loop_actions_2 = [
        #     MoveX(17, 0, 100, pos_x + radius / 2, pos_x - radius / 2),
        #     MoveX(17, 100, 200, pos_x - radius / 2, pos_x + radius / 2)
        # ]
        loop1 = Loop(timestamp + offset, 2, helix_loop_actions_1)
        # loop2 = Loop(timestamp + offset, 2, helix_loop_actions_2)
        star1.add_action(loop1)
        # star2.add_action(loop2)
        return [star1]

    def render(self):
        all_sprites = []
        # create ascendance
        ascendance_bg = AscendanceClimax(50, 0, 400, 0)
        all_sprites += ascendance_bg.render(min(self.timestamps), max(self.timestamps))
        # generate helix for timestamps
        for timestamp in self.timestamps:
            pos = uniform(0, 1)
            rng = uniform(0, 1)
            for i in range(self.n_pairs):
                # create sprites for each pair using the new method
                if rng >= 0.5:
                    pos_y = pos * 480
                    horizontal_sprites = self.create_horizontal_helix(timestamp, pos_y, 100, SB_LEFT, SB_RIGHT, i * 20)
                    all_sprites.extend(horizontal_sprites)
                else:
                    pos_x = SB_LEFT + (SB_RIGHT - SB_LEFT) * pos
                    vertical_sprites = self.create_vertical_helix(timestamp, pos_x, 100, SB_UPPER, SB_LOWER, i*20)
                    all_sprites.extend(vertical_sprites)
        return all_sprites

