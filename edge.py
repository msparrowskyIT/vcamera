from point import *

class Edge:
    "Representation of single edge in 3D/2D coordinate system."

    def __init__(self, points3D, distance, color = 'red'):
        self.points3D = points3D
        self.coefs3D = self.__coefs3D()
        self.points2D = self.__points2D(self.points3D, distance)
        self.coefs2D = self.__coefs2D()
        self.color = color

    def __repr__(self):
        str = f"Edge 3D: x = {self.points3D[0].x} + {self.coefs3D['a']}*t, y = {self.points3D[0].y} + {self.coefs3D['b']}*t, z = {self.points3D[0].z} + {self.coefs3D['c']}*t."
        str += f"Edge 2D: y = {self.coefs2D['a']}*x + {self.coefs2D['b']}" if self.points2D else f"Edge 2D: {None}."

        return str

    def __points2D(self, points3D, distance):
        """Calculate edge's representation in 2D coordinate system.
        If any of points is behind observer, the 2D representation doesn't exist."""
        try:
            points2D = tuple(p.to2D(distance) for p in points3D)
        except PointBehindObserver:
            points2D = None

        return points2D

    def __coefs3D(self):
        "Calculate edge's 3D coefficients: x = x0 + a*x, y = y0 + b*y, z = z0 + c*z."
        a = self.points3D[1].x - self.points3D[0].x
        b = self.points3D[1].y - self.points3D[0].y
        c = self.points3D[1].z - self.points3D[0].z

        return {'a': a, 'b': b, 'c': c}

    def __coefs2D(self):
        "Calculate edge's 2D coefficients: y = a*x + b."
        if(not self.points2D):
            return None
        else:
            try:
                a = (self.points2D[1].y - self.points2D[0].y) / (self.points2D[1].x - self.points2D[0].x)
            except ZeroDivisionError:
                a = 0
            b = self.points2D[1].y - a * self.points2D[1].x
            
            return {'a': a, 'b': b}

    def __update(self, distance):
        "Update edge's coeffitients and 2D representation in context of changing points3D."
        self.coefs3D = self.__coefs3D()
        self.points2D = self.__points2D(self.points3D, distance)
        self.coefs2D = self.__coefs2D()

    def cross3D(self, value, axis):
        "Return Point3D if parameter value is in edge's range."
        def x_cross(x):
            if(self.points3D[0].x <= x <= self.points3D[1].x):
                t = (x - self.points3D[0].x) / self.coefs3D['a']
                return Point3D(x, self.points3D[0].y + self.coefs3D['b'] * t, self.points3D[0].z + self.coefs3D['c'] * t)

            return None

        def y_cross(y):
            if(self.points3D[0].y <= y <= self.points3D[1].y):
                t = (y - self.points3D[0].y) / self.coefs3D['b']
                return Point3D(self.points3D[0].x + self.coefs3D['a'] * t, y, self.points3D[0].z + self.coefs3D['c'] * t)

            return None

        def z_cross(z):
            if(self.points3D[0].z <= z <= self.points3D[1].z):
                t = (z - self.points3D[0].z) / self.coefs3D['c']
                return Point3D(self.points3D[0].x + self.coefs3D['a'] * t, self.points3D[0].y + self.coefs3D['b'] * t, z)

            return None

        cross = {
            'x': x_cross,
            'y': y_cross,
            'z': z_cross
        }.get(axis)

        return cross(value) if cross else None
        
    def cross2D(self, value, axis):
        "Return Point2D if parameter value is in edge's range."
        def x_cross(x):
            if(self.points2D[0].x <= x <= self.points2D[1].x):
                return Point2D(x, self.coefs2D['a'] * x + self.coefs2D['b'])
            
            return None
        
        def y_cross(y):
            if(self.points2D[0].y <= y <= self.points2D[1].y):
                return Point2D((y - self.coefs2D['b']) / self.coefs2D['a'], y)
            
            return None
        
        if(not self.points2D):
            return None
        else:
            cross = {
                'x': x_cross,
                'y': y_cross
            }.get(axis)
            
            return cross(value) if self.points2D and cross else None

    def move(self, axis, step, distance):
        "Move edge in 3D coordinate system and update coefficients and 2D representation."
        list(map(lambda p: p.move(axis, step), self.points3D))
        self.__update(distance)
        
    def rotate(self, axis, angle, distance):
        "Rotate edge in 3D coordinate system and update coefficients and 2D representation."
        self.points3D = tuple(p.rotate(axis, angle) for p in self.points3D)
        self.__update(distance)

    def zoom(self, distance):
        "Zoom edge in 2D coordinate system and update coefficients."
        self.points2D = self.__points2D(self.points3D, distance)
        self.coefs2D = self.__coefs2D()