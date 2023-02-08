import numpy as np
from numpy.random import uniform
from utils.three_dimensions import BoundaryCamera
from scipy.spatial import distance_matrix

from utils.objects import Sprite, Move, Scale, Color, VectorScale, Rotate

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
        camera_velocity = 1000 / (end - start)
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

class Plexus3D:
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    _line = "sb/elements/line.png"
    lineWidth = 100
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
        camera_velocity = 1000 / (end - start)
        ms_p = 1000 / 24
        sprites = [self._black_cover(start, end)]
        for star in pos:
            t = start
            self._camera.position = (0,0,0)
            star_sprite = Sprite(self._star)
            (old_x, old_y), old_size = self._camera.transform(star)
            old_x *= 150; old_y *= 100
            nearest_star_pos = pos[np.argsort(np.sum((pos - star) ** 2, axis=1))[1]]
            (old_x_nn, old_y_nn), _ = self._camera.transform(nearest_star_pos)
            constellation_line = Sprite(self._line)
            while t <= end:
                x_cam, y_cam, z_cam = self._camera.position
                (x, y), size = self._camera.transform(star)
                (x_nn, y_nn), size_nn = self._camera.transform(nearest_star_pos)
                x *= 150; y *= 100
                x_nn *= 150; y_nn *= 100
                if size == 0:
                    (old_x, old_y), old_size = (x, y), size
                    (old_x_nn, old_y_nn) = (x_nn, y_nn)
                    self._camera.position = (x_cam + ms_p * camera_velocity, y_cam, z_cam)
                    t += ms_p
                    continue
                size *= camera_velocity * (end - start) / 8
                star_sprite.add_action(Scale(0, t, t+ms_p, old_size, size))
                star_sprite.add_action(Move(0, t, t+ms_p, (old_x + 320, old_y + 240), (x + 320, y + 240)))
                if size_nn == 0:
                    (old_x, old_y), old_size = (x, y), size
                    (old_x_nn, old_y_nn) = (x_nn, y_nn)
                    self._camera.position = (x_cam + ms_p * camera_velocity, y_cam, z_cam)
                    t += ms_p
                    continue
                old_r = np.sqrt((old_y - old_y_nn) ** 2 + (old_x - old_x_nn) ** 2) / self.lineWidth
                new_r = np.sqrt((y - y_nn) ** 2 + (x - x_nn) ** 2) / self.lineWidth
                old_theta = np.arctan((old_y - old_y_nn) / (old_x - old_x_nn))
                theta = np.arctan((y - y_nn) / (x - x_nn))
                if np.isnan(old_theta):
                    old_theta = np.pi / 2
                if np.isnan(theta):
                    theta = np.pi / 2
                if (old_x_nn - old_x) < 0:
                    old_theta += np.pi
                if (x_nn - x) < 0:
                    theta += np.pi
                old_line_pos = ((old_x + old_x_nn) / 2 + 320, (old_y + old_y_nn) / 2 + 240)
                line_pos = ((x + x_nn) / 2 + 320, (y + y_nn) / 2 + 240)
                constellation_line.add_action(Move(0, t, t+ms_p, old_line_pos, line_pos))
                constellation_line.add_action(VectorScale(0, t, t+ms_p, (old_r, 1), (new_r, 1)))
                constellation_line.add_action(Rotate(0, t, t+ms_p, old_theta, theta))
                (old_x, old_y), old_size = (x, y), size
                (old_x_nn, old_y_nn) = (x_nn, y_nn)
                self._camera.position = (x_cam + ms_p * camera_velocity, y_cam, z_cam)
                t += ms_p
            sprites.append(star_sprite)
            sprites.append(constellation_line)
        return sprites
