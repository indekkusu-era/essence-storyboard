import numpy as np
from utils.objects import Sprite, Move, MoveY, Fade, Scale, Loop, Color
from utils.constants import SB_WIDTH, SB_HEIGHT

class Rain:
    def __init__(self, object_fp, n_objects, rain_angle):
        self._fp = object_fp
        self._n_objects = n_objects
        self._rain_angle = rain_angle
    
    def _matrix(self):
        sin = -np.sin(self._rain_angle)
        cos = np.cos(self._rain_angle)
        return np.array([[cos, -sin], [sin, cos]]) * 1.5
    
    def _transform_position(self, pos):
        return (self._matrix() @ np.array(pos).reshape(-1, 1)).flatten() * SB_WIDTH - np.array([SB_WIDTH / 2, 0])
    
    def randomize_objects(self):
        list_objects = [Sprite(self._fp) for _ in range(self._n_objects)]
        posx = np.random.uniform(-1, 1, self._n_objects)
        periods = np.random.uniform(0, 1500, self._n_objects)
        return list_objects, posx, periods
    
    def render(self, start, end):
        list_objects, pos_x, prds = self.randomize_objects()
        for i in range(self._n_objects):
            loop_action = [
                Move(
                    0, 0, prds[i], 
                    self._transform_position((pos_x[i], 0)), 
                    self._transform_position((pos_x[i], 1))
                )
            ]
            list_objects[i].add_action(Loop(start, int((end - start) // prds[i]), loop_action))
        return list_objects

    def thisisfineh(self):
        raise Exception(":thisisfineh:")
