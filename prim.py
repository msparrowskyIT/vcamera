from point import Point3D, PointBehindObserver
from edge import *
from side import *
from copy import deepcopy

class Prim:
    "Representation of prime in 3d coordinate system"
    
    def __init__(self, point, width, height, deepth, distance, color = 'red'):
        points3D = self.__create_points3D(point, width, height, deepth)
        edges = self.__create_edges(points3D, distance, color)
        self.sides = self.__create_sides(edges, color)
        self.color = color

    def __create_points3D(self, point3D, width, height, deepth):
        """Create prime's points3D."""
        # front: left bottom, right bottom, right top, left top points
        points3D = [point3D]
        points3D.append(Point3D(point3D.x + width, point3D.y, point3D.z))
        points3D.append(Point3D(point3D.x + width, point3D.y + height, point3D.z))
        points3D.append(Point3D(point3D.x, point3D.y + height, point3D.z))
        #back: left bottom, right bottom, right top, left top points
        points3D.append(Point3D(point3D.x, point3D.y, point3D.z + deepth))
        points3D.append(Point3D(point3D.x + width, point3D.y, point3D.z + deepth))
        points3D.append(Point3D(point3D.x + width, point3D.y + height, point3D.z + deepth))
        points3D.append(Point3D(point3D.x, point3D.y + height, point3D.z + deepth))

        return points3D

    def __create_edges(self, points3D, distance, color):
        """Create prime's edges."""
        def create_edge(i, j):
            return Edge(deepcopy((points3D[i], points3D[j])), distance, color)
        
        # front: bottom, right, top, left edges    
        edges = [create_edge(0, 1)]
        edges.append(create_edge(1, 2))
        edges.append(create_edge(2, 3))
        edges.append(create_edge(3, 0))
        # back: bottom, right, top, left edges
        edges.append(create_edge(4, 5))
        edges.append(create_edge(5, 6))
        edges.append(create_edge(6, 7))
        edges.append(create_edge(7, 4))
        # side: left bottom, right bottom, right top, left top edges
        edges.append(create_edge(0, 4))
        edges.append(create_edge(1, 5))
        edges.append(create_edge(2, 6))
        edges.append(create_edge(3, 7))

        return edges

    def __create_sides(self, edges, color):
        """Create prime's sides."""
        def create_side(i, j, k, l):
            return Side(deepcopy((edges[i], edges[j], edges[k], edges[l])), color)

        # front, back sides 
        sides = [create_side(0, 1, 2, 3)]
        sides.append(create_side(4, 5, 6, 7))
        # top, bottom sides 
        sides.append(create_side(2, 10, 6, 11))
        sides.append(create_side(0, 9, 4, 8))
        # left, right sides
        sides.append(create_side(8, 7, 11, 3))
        sides.append(create_side(9, 5, 10, 1))

        return sides

    def move(self, axis, step, distance):
        "Move prim in 3D coordinate system."
        list(map(lambda s: s.move(axis, step, distance), self.sides))
        
    def rotate(self, axis, angle, distance):
        "Rotate prim in 3D coordinate system."
        list(map(lambda s: s.rotate(axis, angle, distance), self.sides))

    def zoom(self, distance):
        "Zoom prim in 2D coordinate system."
        list(map(lambda s: s.zoom(distance), self.sides))