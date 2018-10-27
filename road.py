from point import Point3D, PointBehindObserver

class Road:
    def __init__(self, point, width, height, deepth, color = 'gray'):
        self.points = [point]
        self.points.append(Point3D(point.x + width, point.y, point.z))
        self.points.append(Point3D(point.x + width, point.y + height, point.z + deepth))
        self.points.append(Point3D(point.x, point.y + height, point.z + deepth))
        self.color = color

    def __repr__(self):
        return f"Road: {self.points}"

    def change_color(self, color):
        self.color = color

    def move(self, axis, step):
        list(map(lambda point: point.move(axis, step), self.points))

    def rotate(self, axis, angle):
        list(map(lambda point: point.rotate(axis, angle), self.points))

    def get_poligons2D(self, distance):
        poligons2D = []
        try:
            points2D = tuple(map(lambda point3D: point3D.to2D(distance), self.points))
            poligons2D.append(points2D)
        except PointBehindObserver:
            pass
            #print(f"Poligon: {poligon3D} contains point behind observer.")

        return poligons2D
