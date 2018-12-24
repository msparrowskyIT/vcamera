from rotation import *
import numpy as np

class PointException(Exception):
    pass

class Point2D:
    "Representation of single point in 2D coordinate system."
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __is_close(self, other, abs_error):
        "Check round/truncation absolut error."
        return abs(self.x - other.x) <= abs_error and abs(self.y - other.y) <= abs_error

    def __eq__(self, other):
        return  self.__is_close(other, 1e-5) if isinstance(other, Point2D) else False

class Point3D(Point2D):
    "Representation of single point in 3D coordinate system."

    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y)
        self.z = z

    def __is_close(self, other, abs_error):
        "Check round/truncation absolut error."
        return self._Point2D__is_close(other, abs_error) and abs(self.z - other.z) <= abs_error

    def __eq__(self, other):
        return self.__is_close(other, 1e-5) if isinstance(other, Point3D) else False

    def move(self, axis, step):
        "Move point by step in x, y, z axis."
        m = {
                'x': lambda: (self.x + step, self.y, self.z),
                'y': lambda: (self.x, self.y + step, self.z),
                'z': lambda: (self.x, self.y, self.z + step)
            }.get(axis)

        if(m):
            self.x, self.y, self.z = m()

    def rotate(self, axis, angle):
        "Rotate point by angle in x, y, z axis."
        r_matrix = np.array(Rotation.get_matrix(axis, angle))
        p_matrix = np.array([[self.x], [self.y], [self.z]])
        r_point = np.matmul(r_matrix, p_matrix)
        self.x, self.y, self.z = r_point[0][0], r_point[1][0], r_point[2][0]

    def to2D(self, throwing_area):
        "Transform point from 3D to 2D coordinate system. Same as zoom operation if throwing area's distance is changed."
        if(self.z <= 0):
            raise PointException("Coordinate z is equal or less than 0.")
        
        transformation_rate = throwing_area/self.z
        return Point2D(transformation_rate*self.x, transformation_rate*self.y)