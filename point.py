from rotation import *
import numpy as np

class PointBehindObserver(Exception):
    pass



class Point2D:
    "Representation of single point in 2D coordinate system"
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point2D: [{self.x}, {self.y}]"

class Point3D(Point2D):
    "Representation of single point in 3D coordinate system"

    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y)
        self.z = z

    # def __repr__(self):
    #     return f"Point3D: [{self.x}, {self.y}, {self.z}]"

    def move(self, axis, step):
        "Move point on step in x, y, z direction"
        m = {
                'x': lambda: (self.x + step, self.y, self.z),
                'y': lambda: (self.x, self.y + step, self.z),
                'z': lambda: (self.x, self.y, self.z + step)
            }.get(axis)

        (self.x, self.y, self.z) = m()

    def rotate(self, axis, angle):
        "Rotate point on angle in x, y, z direction"
        r_matrix = np.array(Rotation.get_matrix(axis, angle))
        p_matrix = np.array([[self.x], [self.y], [self.z]])
        r_point = np.matmul(r_matrix, p_matrix)

        (self.x, self.y, self.z) = (r_point[0][0], r_point[1][0], r_point[2][0])

    def to2D(self, distance):
        "Evaluate point from 3D to 2D coordinate system"
        if(self.z <= 0):
            raise PointBehindObserver("Coordinate z is equal or less than 0.")

        rate = distance/self.z
        return Point2D(rate*self.x, rate*self.y)
