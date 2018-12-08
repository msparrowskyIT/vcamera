from point import *
from edge import *

class Polygon:
    "Repesentation of single Polygon in 3D/2D coordinate system. It's made up of arbitrary number of edges."

    def __init__(self, edges, color='red'):
        self.edges = edges
        self.color = color

    def __repr__(self):
        return "Polygon:" + "\n\t".join((e.__repr__() for e in self.edges))

    def move(self, axis, step, distance):
        "Move Polygon in 3D coordinate system."
        list(map(lambda e: e.move(axis, step, distance), self.edges))
        
    def rotate(self, axis, angle, distance):
        "Rotate Polygon in 3D coordinate system."
        list(map(lambda e: e.rotate(axis, angle, distance), self.edges))

    def zoom(self, distance):
        "Zoom Polygon in 2D coordinate system."
        list(map(lambda e: e.zoom(distance), self.edges))