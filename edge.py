from point import *
from enum import Enum

class EdgeException(Exception):
    pass

class EdgeType(Enum):
    X_CONST = 1,
    Y_CONST = 2,
    Z_CONST = 3,
    NO_CONST = 4

class Edge2D:
    "Representation of single edge in 2D coordinate system."
    
    def __init__(self, points2D, color ='red'):
        self.s_point, self.e_point = points2D
        self.type = self.__type_init()
        self.coefs = self.__coefs_init()
        self.color = color

    def __type_init(self):
        "Init edge type."
        types = []
        if(self.s_point.x == self.e_point.x): types.append(EdgeType.X_CONST)
        if(self.s_point.y == self.e_point.y): types.append(EdgeType.Y_CONST)
        if(len(types) == 2): raise EdgeException("Edge must be delimited by two different points2D.")

        return types[0] if types else EdgeType.NO_CONST

    def __coefs_init(self):
        "Init edge's coefficients: x = x0 + a*t, y = y0 + b*t"
        a = self.e_point.x - self.s_point.x
        b = self.e_point.y - self.s_point.y
        
        return {'a': a, 'b': b}

    def update(self):
        "Update type and coefficients after extreme point change."
        self.type = self.__type_init()
        self.coefs = self.__coefs_init()

    def get_point(self, t):
        "Calculate Point2D from directional vector."
        return Point2D(self.s_point.x + self.coefs['a'] * t, self.s_point.y + self.coefs['b'] * t)

    def get_axis_param(self, axis, func):
        "Call function with extreme points coordinates in certain axis."
        p = {
            'x': (self.s_point.x, self.e_point.x),
            'y': (self.s_point.y, self.e_point.y)
        }.get(axis)

        return func(p) if p else None

    def __is_correct_range(self, axis, value):
        "Check is value in correct range in certain axis."
        c = {
            'x': lambda: self.get_axis_param('x', min) <= value <= self.get_axis_param('x', max),
            'y': lambda: self.get_axis_param('y', min) <= value <= self.get_axis_param('y', max),
        }.get(axis)

        return c() if c else False

    def contain(self, point2D):
        "Check does point2D satisfy the edge's equation."
        if(not(self.__is_correct_range('x', point2D.x) and self.__is_correct_range('y', point2D.y))):
            return False
        elif(self.type == EdgeType.X_CONST or self.type == EdgeType.Y_CONST):
            return True
        else:
            t = (point2D.x - self.s_point.x) / self.coefs['a']
            return point2D == self.get_point(t)
            
    def cross_with_axis(self, axis, value):
        "Calculate Point2D if parameter value is in edge's range."
        def x_cross():
            if(self.__is_correct_range('x', value)):
                if(self.type != EdgeType.X_CONST):
                    t = (value - self.s_point.x) / self.coefs['a']
                    return self.get_point(t)
                else:
                    return (self.s_point, self.e_point)
            else:
                return []
        
        def y_cross():
            if (self.__is_correct_range('y', value)):
                if(self.type != EdgeType.Y_CONST):
                    t = (value - self.s_point.y) / self.coefs['b']
                    return self.get_point(t)
                else:
                    (self.s_point, self.e_point)
            else:
                return []
        
        c = {
            'x': x_cross,
            'y': y_cross
        }.get(axis)

        return c() if c else None

    def cross_with_edge(self, edge2D):
        "Calculate Point2D if edges have common points."
        def get_common_extreme_points():
            cross_points = []
            cross_points.extend([p for p in (self.s_point, self.e_point) if not p in cross_points and edge2D.contain(p)])
            cross_points.extend([p for p in (edge2D.s_point, edge2D.e_point) if not p in cross_points and self.contain(p)])
            return tuple(cross_points)

        denominator = self.coefs['a'] * edge2D.coefs['b'] - self.coefs['b'] * edge2D.coefs['a']
        if(denominator != 0):
            numerator = edge2D.coefs['a'] * (self.s_point.y - edge2D.s_point.y) + edge2D.coefs['b'] * (edge2D.s_point.x - self.s_point.x)
            t = numerator / denominator
            cross_point = self.get_point(t)
            return cross_point if self.contain(cross_point) and edge2D.contain(cross_point) else None
        else:
            return get_common_extreme_points()

class Edge3D:

    def __init__(self, points3D, color='red'):
        self.s_point, self.e_point = points3D
        self.type = self.__type_init()
        self.coefs = self.__coefs_init()
        self.color = color

    def update(self):
        "Update type and coefficients after extreme point change."
        self.type = self.__type_init()
        self.coefs = self.__coefs_init()

    def __type_init(self):
        "Init edge type."
        types = []
        if(self.s_point.x == self.e_point.x): types.append(EdgeType.X_CONST)
        if(self.s_point.y == self.e_point.y): types.append(EdgeType.Y_CONST)
        if(self.s_point.z == self.e_point.z): types.append(EdgeType.Z_CONST) 
        if(len(types) == 3): 
            raise EdgeException("Edge must be delimited by two different points3D.")

        return types if types else [EdgeType.NO_CONST]

    def __coefs_init(self):
        "Calculate edge's 3D coefficients: x = x0 + a*t, y = y0 + b*t, z = z0 + c*t."
        a = self.e_point.x - self.s_point.x
        b = self.e_point.y - self.s_point.y
        c = self.e_point.z - self.s_point.z

        return {'a': a, 'b': b, 'c': c}

    def update(self):
        "Update type and coefficients after extreme point change."
        self.type = self.__type_init()
        self.coefs = self.__coefs_init()

    def get_axis_param(self, axis, func):
        "Get 3D parameters in axis like min, max."
        p = {
            'x': (self.s_point.x, self.e_point.x),
            'y': (self.s_point.y, self.e_point.y),
            'z': (self.s_point.z, self.e_point.z)
        }.get(axis)

        return func(p) if p else None

    def get_point(self, t):
        "Calculate Point3D from length of directional vector."
        return Point3D(self.s_point.x + self.coefs['a'] * t, self.s_point.y + self.coefs['b'] * t, self.s_point.z + self.coefs['c'] * t)

    def get_transformation_ratio(self, point2D, throwing_area):
        "Calculate transformation ratio for 3D point2D."
        denominator_xz = self.coefs['a'] * throwing_area - self.coefs['c'] * point2D.x
        if(denominator_xz):
            numerator_xz = self.s_point.z * point2D.x - self.s_point.x * throwing_area 
            return numerator_xz / denominator_xz
        
        denominator_yz = self.coefs['b'] * throwing_area - self.coefs['c'] * point2D.y
        if(denominator_yz):
            numerator_yz = self.s_point.z * point2D.y - self.s_point.y * throwing_area 
            return numerator_yz / denominator_yz

        return (-1, 1)

    def move(self, axis, step, throwing_area):
        "Move edge in 3D coordinate system."
        list(map(lambda p: p.move(axis, step), (self.s_point, self.e_point)))
        self.update()

    def rotate(self, axis, angle, throwing_area):
        "Rotate edge in 3D coordinate system."
        list(map(lambda p: p.rotate(axis, angle), (self.s_point, self.e_point)))
        self.update()

    def to2D(self, throwing_area):
        "Transform edge from 3D to 2D coordinate system. Same as zoom operation if throwing area's distance is changed."
        try:
            points2D = tuple([p3D.to2D(throwing_area) for p3D in (self.s_point, self.e_point)])
            return Edge2D(points2D, self.color)
        except PointException:
            return None
                
class Edge:

    def __init__(self, points3D, throwing_area, color='red'):
        self.edge3D = Edge3D(points3D, color)
        self.edge2D = self.edge3D.to2D(throwing_area)
        self.color = color

    def is_representation2D(self):
        return self.edge2D != None

    def __update(self, throwing_area):
        self.edge2D = self.edge3D.to2D(throwing_area)

    def move(self, axis, step, throwing_area):
        "Move edge in 3D coordinate system."
        self.edge3D.move(axis, step, throwing_area)
        self.__update(throwing_area)

    def rotate(self, axis, angle, throwing_area):
        "Rotate edge in 3D coordinate system."
        self.edge3D.rotate(axis, angle, throwing_area)
        self.__update(throwing_area)

    def zoom(self, throwing_area):
        "Zoom edge in 2D coordinate system."
        try:
            points2D = tuple([p.to2D(throwing_area) for p in (self.edge3D.s_point, self.edge3D.e_point)])
            self.edge2D = Edge2D(points2D, self.edge3D.color)
        except (PointException, EdgeException):
            self.edge2D = None