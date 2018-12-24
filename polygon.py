from point import *
from edge import *

class Polygon:
    "Repesentation of single Polygon in 3D/2D coordinate system. It's made up of arbitrary number of edges."

    def __init__(self, edges, color='red'):
        self.edges = edges
        self.color = color

    def move(self, axis, step, throwing_area):
        "Move Polygon in 3D coordinate system."
        list(map(lambda e: e.move(axis, step, throwing_area), self.edges))
        
    def rotate(self, axis, angle, throwing_area):
        "Rotate Polygon in 3D coordinate system."
        list(map(lambda e: e.rotate(axis, angle, throwing_area), self.edges))

    def zoom(self, throwing_area):
        "Zoom Polygon in 2D coordinate system."
        list(map(lambda e: e.zoom(throwing_area), self.edges))