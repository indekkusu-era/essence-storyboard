import numpy as np
from numpy import exp, cos
from numpy.random import exponential, uniform

from utils.three_dimensions import BoundaryCamera
from utils.three_dimensions.coord_transformers import cartesian_to_cylindrical, cylindrical_to_cartesian
from utils.three_dimensions.coord_transformers import spherical_to_cartesian

from utils.objects import Sprite, Color, Scale, Move, Fade

class OrbRotation:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    def __init__(self, expected_generation_time: int):
        self._expected_generation_time = expected_generation_time
        self._camera = BoundaryCamera(boundary=(640, 480))
    
    def _black_cover(self, start, end):
        white = Sprite(self._white)
        white.add_action(Color(0, start, end, (0,0,0), (0,0,0)))
        white.add_action(Scale(0, start, end, 5, 5))
        return white

    def object_rotation(self, coord0: tuple, center_point: tuple, alpha: float, beta: float, gamma: float):
        def rot_t(t):
            x0, y0, z0 = coord0
            xc, yc, zc = center_point
            relative_coord = (x0 - xc, y0 - yc, z0 - zc)
            ri, thetai, zi = cartesian_to_cylindrical(*relative_coord)
            rt = ri * exp(-alpha * t)
            thetat = beta * t + thetai
            zt = zi * exp(-alpha * t) * cos(gamma * t)
            xt, yt, zt = cylindrical_to_cartesian(rt, thetat, zt)
            return (xt + xc, yt + yc, zt + zc)
        return rot_t
    
    def render(self, start: int, end: int, alpha: float, beta: float, gamma: float, fps=24):
        self._camera.position = (-10, 0, 0)
        ms_per_frame = 1000 / fps
        t = start
        all_sprites = [self._black_cover(start, end)]
        while t < end:
            next_star_event = exponential(self._expected_generation_time)
            star = Sprite(self._star)
            rho0 = 1
            theta0 = uniform(0, np.pi * 2)
            phi0 = uniform(0, np.pi)
            x0, y0, z0 = spherical_to_cartesian(rho0, theta0, phi0)
            rot_function = self.object_rotation((x0, y0, z0), (0,0,0), alpha, beta, gamma)
            t0 = t
            (old_x, old_y), old_size = self._camera.transform(rot_function(0))
            old_x *= 6000; old_y *= 3000; old_size *= 75/8 # these are kind of magic numbers but yea
            while t0 < end:
                relative_t = t0 - t
                xt, yt, zt = rot_function(relative_t)
                (posx, posy), size = self._camera.transform((xt, yt, zt))
                posx *= 6000; posy *= 3000; size *= 75/8
                if size == 0:
                    old_x, old_y, old_size = posx, posy, size
                    t0 += ms_per_frame
                    t0 = int(t0)
                star.add_action(Scale(0, t0, int(t0 + ms_per_frame), old_size, size))
                star.add_action(Move(0, t0, int(t0 + ms_per_frame), (old_x + 320, old_y + 240), (posx + 320, posy + 240)))
                t0 += ms_per_frame
                t0 = int(t0)
                old_x, old_y, old_size = posx, posy, size
            t += int(next_star_event)
            all_sprites.append(star)
        return all_sprites
