import numpy as np
from numpy.random import uniform
from utils.three_dimensions import BoundaryCamera

from utils.objects import Sprite, Move, Scale, Color

class StarZoom:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    def __init__(self, n_stars):
        self._n_stars = n_stars
        self._camera = BoundaryCamera(boundary=(640, 480))
    
    def _black_cover(self, start, end):
        white = Sprite(self._white)
        white.add_action(Color(0, start, end, (0,0,0), (0,0,0)))
        white.add_action(Scale(0, start, end, 5, 5))
        return white
    
    def render(self, start, end):
        objs = uniform(-1, 1, (3, self._n_stars))
        mat = np.array([[1000, 0, 0], [0, 320, 0], [0, 0, 240]])
        pos = (mat @ objs).T
        # i wanna do fancy splines stuff but that is later lol
        camera_velocity = 750 / (end - start)
        ms_p = 1000 / 24
        sprites = [self._black_cover(start, end)]
        for star in pos:
            t = start
            self._camera.position = (0,0,0)
            star_sprite = Sprite(self._star)
            (old_x, old_y), old_size = self._camera.transform(star)
            old_x *= 150; old_y *= 100
            while t <= end:
                x_cam, y_cam, z_cam = self._camera.position
                (x, y), size = self._camera.transform(star)
                x *= 150; y *= 100
                if size == 0:
                    (old_x, old_y), old_size = (x, y), size
                    self._camera.position = (x_cam + ms_p * camera_velocity, y_cam, z_cam)
                    t += ms_p
                    continue
                size *= camera_velocity * (end - start) / 8
                star_sprite.add_action(Scale(0, t, t+ms_p, old_size, size))
                star_sprite.add_action(Move(0, t, t+ms_p, (old_x + 320, old_y + 240), (x + 320, y + 240)))
                (old_x, old_y), old_size = (x, y), size
                self._camera.position = (x_cam + ms_p * camera_velocity, y_cam, z_cam)
                t += ms_p
            sprites.append(star_sprite)
        return sprites

                
            
            
