from point import Point3D
from prim import Prim
from polygon import *
from scan import *
import tkinter as tk
from math import pi

def draw():
    canvas.delete(tk.ALL)

    def center(point2D):
        return (WIDTH/2 + point2D.x, HEIGHT/2 - point2D.y)

    he = ScanLineAlgoritm.scan(p, DISTANCE)
    i=0
    color = ['red', 'green', 'white', 'blue']
    for y, edges2D in ScanLineAlgoritm.scan(p, DISTANCE).items():
        for e in edges2D:
            canvas.create_line(*center(e.s_point), *center(e.e_point), fill = e.color)

def move(axis, step, polygons):
    global DISTANCE
    list(map(lambda p: p.move(axis, step, DISTANCE), polygons))

def rotate(axis, angle, polygons):
    global DISTANCE
    list(map(lambda p: p.rotate(axis, angle, DISTANCE), polygons))

def zoom(step, polygons):
    global DISTANCE
    DISTANCE += step if DISTANCE + step >= 0 else 0
    list(map(lambda p: p.zoom(DISTANCE), polygons))


WIDTH = HEIGHT = 502
DISTANCE = 100
ZOOM_STEP = 2.5
MOVE_STEP = 5
ROTATION_STEP = pi/30

prims = [
    Prim(Point3D(-40, -20, 100), 80, 50, 50, DISTANCE, 'purple'),
    Prim(Point3D(25, -20, 50), 25, 25, 25, DISTANCE),
    # Prim(Point3D(-50, -20, 50), 25, 25, 25, DISTANCE, 'green'),
]

p = []
for prim in prims:
    p.extend(prim.polygons)

# e1 = Edge((Point3D(-25, 0, 25), Point3D(25, 0, 50)), DISTANCE)
# e2 = Edge((Point3D(25, 0, 50), Point3D(25, 25, 50)), DISTANCE)
# e3 = Edge((Point3D(25, 25, 50), Point3D(-25, 25, 25)), DISTANCE)
# e4 = Edge((Point3D(-25, 25, 25), Point3D(-25, 0, 25)), DISTANCE)
# p1 = Polygon((e1,e2,e3,e4), 'red')

# e5 = Edge((Point3D(-25, 0, 50), Point3D(25, 0, 25)), DISTANCE)
# e6 = Edge((Point3D(25, 0, 25), Point3D(25, 25, 25)), DISTANCE)
# e7= Edge((Point3D(25, 25, 25), Point3D(-25, 25, 50)), DISTANCE)
# e8= Edge((Point3D(-25, 25, 50), Point3D(-25, 0, 50)), DISTANCE)
# p2 = Polygon((e5,e6,e7,e8), 'green')

# p = [p1] + [p2]


# e1 = Edge((Point3D(-25, 0, 25), Point3D(25, 0, 50)), DISTANCE)
# e2 = Edge((Point3D(-25, 0, 25), Point3D(0, 25, 37.5)), DISTANCE)
# e3 = Edge((Point3D(25, 0, 50), Point3D(0, 25, 37.5)), DISTANCE)
# p1 = Polygon((e1,e2,e3), 'red')

# e4 = Edge((Point3D(-25, 0, 50), Point3D(25, 0, 25)), DISTANCE)
# e5 = Edge((Point3D(-25, 0, 50), Point3D(0, 25, 37.5)), DISTANCE)
# e6= Edge((Point3D(25, 0, 25), Point3D(0, 25, 37.5)), DISTANCE)
# p2 = Polygon((e4,e5,e6), 'green')

# p = [p2] + [p1]


# roads = [
#     Road(Point3D(-12.5, -20, 50), 25, 0, 40)
# ]

def key(event):

    handler = {
        '2': lambda: move('y', MOVE_STEP, p),
        '8': lambda: move('y', -MOVE_STEP, p),
        '4': lambda: move('x', MOVE_STEP, p),
        '6': lambda: move('x', -MOVE_STEP, p),
        '0': lambda: move('z', MOVE_STEP, p),
        '5': lambda: move('z', -MOVE_STEP, p),

        '-': lambda: zoom(-ZOOM_STEP, p),
        '+': lambda: zoom(ZOOM_STEP, p),

        'd': lambda: rotate('y', ROTATION_STEP, p),
        'c': lambda: rotate('y', -ROTATION_STEP, p),
        's': lambda: rotate('x', ROTATION_STEP, p),
        'x': lambda: rotate('x', -ROTATION_STEP, p),
        'a': lambda: rotate('z', ROTATION_STEP, p),
        'z': lambda: rotate('z', -ROTATION_STEP, p)

    }.get(event.char)

    if handler:
        handler()
        draw()

window = tk.Tk()
canvas = tk.Canvas(window, width = WIDTH, height = HEIGHT, bg='black')
window.bind('<Key>', key)
draw()
canvas.pack()

tk.mainloop()
