import numpy as np
from numpy import sin, cos
from numpy.linalg import inv

class Camera:
    def __init__(self, position=(0,0,0), rotation=(0,0,0)):
        self._position = position
        self._rotation = rotation
    
    @property
    def position(self):
        return self._position
    
    @property
    def rotation(self):
        return self._rotation
    
    @position.setter
    def position(self, new_position):
        self._position = new_position
    
    @rotation.setter
    def rotation(self, new_rotation):
        self._rotation = new_rotation
    
    @property
    def rotation_matrix(self):
        theta, phi, psi = self.rotation
        rx = np.array([[1,0,0], [0,cos(theta),-sin(theta)], [0,sin(theta),cos(theta)]])
        ry = np.array([[cos(phi),0,-sin(phi)], [0,1,0], [sin(phi),0,cos(phi)]])
        rz = np.array([[cos(psi),-sin(psi),0], [sin(psi),cos(psi),0], [0,0,1]])
        return rx @ ry @ rz
    
    def transform(self, object_position: tuple):
        x, y, z = object_position
        x_cam, y_cam, z_cam = self.position
        relative_pos = np.array((x - x_cam, y - y_cam, z - z_cam)).reshape(-1, 1)
        inv_size, x_2d, y_2d = (inv(self.rotation_matrix) @ relative_pos).flatten()
        if inv_size <= 0:
            return (0,0), 0

        size = 1 / inv_size
        # todo: scale this according to the triangle
        return (x_2d, y_2d), size

class BoundaryCamera(Camera):
    def __init__(self, position=(0,0,0), rotation=(0,0,0), boundary=(1280,720)):
        super().__init__(position, rotation)
        self._boundary = boundary
    
    def left(self):
        return -self._boundary[0] / 2
    
    def right(self):
        return self._boundary[0] / 2
    
    def upper(self):
        return self._boundary[1] / 2
    
    def lower(self):
        return -self._boundary[1] / 2
    
    def transform(self, object_position: tuple):
        (x, y), size = super().transform(object_position)
        if size == 0:
            return (0,0), 0
        if self.left() <= x <= self.right() and self.lower() <= y <= self.upper():
            return (x, y), size
        return (0,0), 0
