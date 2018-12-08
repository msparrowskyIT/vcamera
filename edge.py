from point import *
import math

class Edge:
    "Representation of single edge in 3D/2D coordinate system."

    def __init__(self, points3D, distance, color = 'red'):
        self.s_point3D, self.e_point3D = self.__points3D_init(points3D)
        self.coefs3D = self.__coefs3D_init()

        self.s_point2D, self.e_point2D = self.__points2D_init(points3D, distance)
        self.coefs2D = self.__coefs2D_init()

        self.color = color

    def __repr__(self):
        str = f"Edge 3D: x = {self.points3D[0].x} + {self.coefs3D['a']}*t, y = {self.points3D[0].y} + {self.coefs3D['b']}*t, z = {self.points3D[0].z} + {self.coefs3D['c']}*t.\n"
        str += f"Edge 2D: y = {self.coefs2D['a']}*x + {self.coefs2D['b']}" if self.points2D else f"Edge 2D: {None}."

        return str

    def __points3D_init(self, points3D):
        "Points3D in correct order."
        return points3D if points3D[0].y <= points3D[1].y else points3D[::-1]

    def __points2D_init(self, points3D, distance):
        "Points3D in 2D coordinate system, if exists."
        try:
            points2D = tuple(p.to2D(distance) for p in points3D)
            if(points2D[0].y > points2D[1].y): 
                points2D = points2D[::-1]
        except PointBehindObserver:
            points2D = (None, None)

        return points2D

    def __coefs3D_init(self):
        "Calculate edge's 3D coefficients: x = x0 + a*x, y = y0 + b*y, z = z0 + c*z."
        a = self.e_point3D.x - self.s_point3D.x
        b = self.e_point3D.y - self.s_point3D.y
        c = self.e_point3D.z - self.s_point3D.z

        return {'a': a, 'b': b, 'c': c}

    def __coefs2D_init(self):
        "Calculate edge's 2D coefficients: y = a*x + b. If y is vertical return None."
        if(not all((self.s_point2D, self.e_point2D))):
            return None
        else:
            try:
                a = (self.e_point2D.y - self.s_point2D.y) / (self.e_point2D.x - self.s_point2D.x)
                b = self.e_point2D.y - a * self.e_point2D.x
                return {'a': a, 'b': b}
            except ZeroDivisionError:
                return None

    def cross3D(self, value, axis, rate = 1):
        "Return Point3D if parameter rate*value is in edge's range on axis."
        def x_cross(x):
            if(self.s_point3D.x <= x <= self.e_point3D.x):
                t = (x - self.s_point3D.x) / self.coefs3D['a']
                return Point3D(x, self.s_point3D.y + self.coefs3D['b'] * t, self.s_point3D.z + self.coefs3D['c'] * t)
            else:
                return None

        def y_cross(y):
            if(self.s_point3D.y <= y <= self.e_point3D.y):
                t = (y - self.s_point3D.y) / self.coefs3D['b']
                return Point3D(self.s_point3D.x + self.coefs3D['a'] * t, y, self.s_point3D.z + self.coefs3D['c'] * t)
            else:
                return None

        def z_cross(z):
            if(self.s_point3D[0].z <= z <= self.e_point3D.z):
                t = (z - self.s_point3D.z) / self.coefs3D['c']
                return Point3D(self.s_point3D.x + self.coefs3D['a'] * t, self.s_point3D.y + self.coefs3D['b'] * t, z)
            else:
                return None

        cross = {
            'x': x_cross,
            'y': y_cross,
            'z': z_cross
        }.get(axis)

        return cross(rate*value) if cross else None
        
    def cross2D(self, value, axis, rate=1):
        "Return Point2D if parameter value is in edge's range."
        def x_cross(x):
            if(self.s_point2D.x <= x <= self.e_point2D.x):
                if(self.coefs2D): 
                    point2D = Point2D(x, self.coefs2D['a'] * x + self.coefs2D['b'])
                else:
                    point2D = Point2D(x, math.inf)
                return point2D
            else:
                return None
        
        def y_cross(y):
            if(self.s_point2D.y <= y <= self.e_point2D.y):
                if(self.coefs2D):
                    try:
                        point2D = Point2D((y - self.coefs2D['b']) / self.coefs2D['a'], y)
                    except ZeroDivisionError:
                        point2D = Point2D(math.inf, y)
                else:
                    point2D = Point2D(self.s_point2D.x, y)
                return point2D
            else:
                return None
        
        if(not all((self.s_point2D, self.e_point2D))):
            return None
        else:
            cross = {
                'x': x_cross,
                'y': y_cross
            }.get(axis)
            
            return cross(value) if self.points2D and cross else None

    def __update3D(self, distance):
        "Update edge's after 3D processing."
        self.coefs3D = self.__coefs3D_init()
        self.points2D = self.__points2D_init((self.s_point3D, self.e_point3D), distance)
        self.coefs2D = self.__coefs2D_init()

    def __update2D(self, distance):
        "Update edge's after 2D processing."
        self.points2D = self.__points2D_init((self.s_point3D, self.e_point3D), distance)
        self.coefs2D = self.__coefs2D_init()

    def move(self, axis, step, distance):
        "Move edge in 3D coordinate system."
        list(map(lambda p: p.move(axis, step), (self.s_point3D, self.e_point3D)))
        self.__update3D(distance)
        
        
    def rotate(self, axis, angle, distance):
        "Rotate edge in 3D coordinate system."
        list(map(lambda p: p.rotate(axis, angle), (self.s_point3D, self.e_point3D)))
        self.__update3D(distance)

    def zoom(self, distance):
        "Zoom edge in 2D coordinate system."
        self.__update2D(distance)