from point import Point3D, PointBehindObserver

class Prim:
    "Representation of prime in 3d coordinate system"
    def __init__(self, point, width, height, deepth, color = 'red'):
        # front points
        self.points = [point]
        self.points.append(Point3D(point.x + width, point.y, point.z))
        self.points.append(Point3D(point.x + width, point.y + height, point.z))
        self.points.append(Point3D(point.x, point.y + height, point.z))
        #back points
        self.points.append(Point3D(point.x, point.y, point.z + deepth))
        self.points.append(Point3D(point.x + width, point.y, point.z + deepth))
        self.points.append(Point3D(point.x + width, point.y + height, point.z + deepth))
        self.points.append(Point3D(point.x, point.y + height, point.z + deepth))
        self.color = color

    def __repr__(self):
        return f"Prim: {self.points}"

    def change_color(self, color):
        self.color = color

    def move(self, axis, step):
        list(map(lambda point: point.move(axis, step), self.points))

    def rotate(self, axis, angle):
        list(map(lambda point: point.rotate(axis, angle), self.points))

    def __get_poligons3D(self):
        poligons3D = []
        # front wall
        poligons3D.append((self.points[0], self.points[1], self.points[2], self.points[3]))
        # back wall
        poligons3D.append((self.points[4], self.points[5], self.points[6], self.points[7]))
        # side walls
        poligons3D.append((self.points[0], self.points[1], self.points[5], self.points[4]))
        poligons3D.append((self.points[1], self.points[2], self.points[6], self.points[5]))
        poligons3D.append((self.points[2], self.points[3], self.points[7], self.points[6]))
        poligons3D.append((self.points[0], self.points[3], self.points[7], self.points[4]))
        return poligons3D

    def get_poligons2D(self, distance):
        poligons3D = self.__get_poligons3D()
        poligons2D = []
        for poligon3D in poligons3D:
            try:
                points2D = tuple(map(lambda point3D: point3D.to2D(distance), poligon3D))
                poligons2D.append(points2D)
            except PointBehindObserver:
                pass
                #print(f"Poligon: {poligon3D} contains point behind observer.")

        return poligons2D
