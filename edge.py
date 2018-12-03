from point import *

class Edge:
    "Representation of single edge in 2D coordinate system."

    def __init__(self, points3D, distance):
        self.points3D = points3D
        self.coefs3D = self.__coefs3D()
        self.points2D = tuple(p.to2D(distance) for p in points3D)
        self.coefs2D = self.__coefs2D()

    def __repr__(self):
        return f"""Edge:
        3D: {self.points3D}, x = {self.points3D[0].x} + {self.coefs3D['a']}*t, y = {self.points3D[0].y} + {self.coefs3D['b']}*t, z = {self.points3D[0].z} + {self.coefs3D['c']}*t.
        2D: {self.points2D}, y = {self.coefs2D['a']}*x + {self.coefs2D['b']}"""

    def __coefs3D(self):
        "Calculate edge's 3D coefficients: x = x0 + a*x, y = y0 + b*y, z = z0 + c*z."
        a = self.points3D[1].x - self.points3D[0].x
        b = self.points3D[1].y - self.points3D[0].y
        c = self.points3D[1].z - self.points3D[0].z

        return {'a': a, 'b': b, 'c': c}

    def __coefs2D(self):
        "Calculate edge's 2D coefficients: y = a*x + b."
        try:
            a = (self.points3D[1].y - self.points3D[0].y) / (self.points3D[1].x - self.points3D[0].x)
        except ZeroDivisionError:
            a = 0
        b = self.points3D[1].y - a * self.points3D[1].x

        return {'a': a, 'b': b}

    def cross3D(self, value, axis):
        "Return Point3D if parameter value is in edge's range."
        def x_cross(x):
            if(self.points3D[0].x <= x <= self.points3D[1].x):
                t = (x - self.points3D[0].x) / self.coefs3D['a']
                return Point3D(x, self.ponits3D[0].y + self.coefs3D['b'] * t, self.ponits3D[0].z + self.coefs3D['c'] * t)

            return None

        def y_cross(y):
            if(self.points3D[0].y <= y <= self.points3D[1].y):
                t = (y - self.points3D[0].y) / self.coefs3D['b']
                return Point3D(self.ponits3D[0].x + self.coefs3D['a'] * t, y, self.ponits3D[0].z + self.coefs3D['c'] * t)

            return None

        def z_cross(z):
            if(self.points3D[0].z <= z <= self.points3D[1].z):
                t = (z - self.points3D[0].z) / self.coefs3D['c']
                return Point3D(self.ponits3D[0].x + self.coefs3D['a'] * t, self.ponits3D[0].y + self.coefs3D['b'] * t, z)

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

        cross = {
            'x': x_cross,
            'y': y_cross
        }.get(axis)

        return cross(value) if cross else None


p1 = Point3D(1, 1, 1)
p2 = Point3D(2, 2, 1)

e = Edge((p1, p2), 1)
print(e)
print(e.cross2D(1.5, 'y'))