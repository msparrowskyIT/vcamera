from point import *
from edge import *
from polygon import *
from copy import deepcopy

class Road:
    def __init__(self, point, width, height, deepth, throwing_area, color = 'red'):
        points3D = self.__create_points3D(point, width, height, deepth)
        edges = self.__create_edges(points3D, throwing_area, color)
        self.polygon = self.__polygon_init(edges, color)
        self.color = color       

    def __create_points3D(self, point3D, width, height, deepth):
        """Create road's points3D."""
        points3D = [point3D]
        points3D.append(Point3D(point3D.x + width, point3D.y, point3D.z))
        points3D.append(Point3D(point3D.x + width, point3D.y + height, point3D.z + deepth))
        points3D.append(Point3D(point3D.x, point3D.y + height, point3D.z + deepth))
        
        return points3D

    def __create_edges(self, points3D, throwing_area, color):
        """Create road's edges."""
        def create_edge(i, j):
            return Edge(deepcopy((points3D[i], points3D[j])), throwing_area, color)

        edges = [create_edge(0, 1)]
        edges.append(create_edge(1, 2))
        edges.append(create_edge(2, 3))
        edges.append(create_edge(3, 0)) 

        return edges

    def __polygon_init(self, edges, color):
        """Create road's side."""
        return Polygon(deepcopy((edges[0], edges[1], edges[2], edges[3])), color)

    def move(self, axis, step, throwing_area):
        "Move road in 3D coordinate system."
        self.polygon.move(axis, step, throwing_area)
        
    def rotate(self, axis, angle, throwing_area):
        "Rotate road in 3D coordinate system."
        self.polygon.rotate(axis, angle, throwing_area)

    def zoom(self, throwing_area):
        "Zoom road in 2D coordinate system."
        self.polygon.zoom(throwing_area)