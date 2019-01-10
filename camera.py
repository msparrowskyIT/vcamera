from point import *
from prim import *
from road import *
from polygon import *
from scan import *
from math import pi
import tkinter as tk

def draw():
    canvas.delete(tk.ALL)

    def center(point2D):
        return (WIDTH/2 + point2D.x, HEIGHT/2 - point2D.y)

    for y, edges2D in ScanLineAlgoritm.scan(polygons, DISTANCE).items():
        for e in edges2D:
            canvas.create_line(*center(e.s_point), *center(e.e_point), fill = e.color)

    # for p in polygons:
    #     for e in p.edges:
    #         canvas.create_line(*center(e.edge2D.s_point), *center(e.edge2D.e_point), fill = 'white')


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
DISTANCE = 200
ZOOM_STEP = 5
MOVE_STEP = 25
ROTATION_STEP = pi/15

# *****
prims = [
    Prim(Point3D(-40, -20, 100), 80, 50, 50, DISTANCE, 'purple'),
    Prim(Point3D(25, -20, 50), 25, 25, 25, DISTANCE),
    Prim(Point3D(-50, -20, 50), 25, 25, 25, DISTANCE, 'green'),
]

roads = [
    Road(Point3D(-12.5, -20, 50), 25, 0, 40, DISTANCE, 'white')
]

polygons = []
for p in prims + roads:
    if (hasattr(p, 'polygons')):
        polygons.extend(p.polygons)
    else:
        polygons.append(p.polygon)

# *****
e1 = Edge((Point3D(-50, 0, 110), Point3D(0, 0, 110)), DISTANCE)
e2 = Edge((Point3D(-50, 0, 110), Point3D(-25, 100, 90)), DISTANCE)
e3 = Edge((Point3D(0, 0, 110), Point3D(-25, 100, 90)), DISTANCE)
t1 = Polygon((e1,e2,e3))

e4 = Edge((Point3D(0, 100, 110), Point3D(50, 100, 110)), DISTANCE)
e5 = Edge((Point3D(0, 100, 110), Point3D(25, 0, 90)), DISTANCE)
e6 = Edge((Point3D(50, 100, 110), Point3D(25, 0, 90)), DISTANCE)
t2 = Polygon((e4,e5,e6))

e7 = Edge((Point3D(-50, 50, 100), Point3D(-50, 100, 100)), DISTANCE)
e8 = Edge((Point3D(-50, 50, 100), Point3D(50, 75, 100)), DISTANCE)
e9 = Edge((Point3D(-50, 100, 100), Point3D(50, 75, 100)), DISTANCE)
t3 = Polygon((e7,e8,e9), 'yellow')

e10 = Edge((Point3D(-50, 25, 100), Point3D(50, 0, 100)), DISTANCE)
e11 = Edge((Point3D(-50, 25, 100), Point3D(50, 50, 100)), DISTANCE)
e12 = Edge((Point3D(50, 0, 100), Point3D(50, 50, 100)), DISTANCE)
t4 = Polygon((e10,e11,e12), 'yellow')

# polygons = [t1, t2, t3, t4]

def key(event):

    handler = {
        '2': lambda: move('y', MOVE_STEP, polygons),
        '8': lambda: move('y', -MOVE_STEP, polygons),
        '4': lambda: move('x', MOVE_STEP, polygons),
        '6': lambda: move('x', -MOVE_STEP, polygons),
        '0': lambda: move('z', MOVE_STEP, polygons),
        '5': lambda: move('z', -MOVE_STEP, polygons),

        '-': lambda: zoom(-ZOOM_STEP, polygons),
        '+': lambda: zoom(ZOOM_STEP, polygons),

        'd': lambda: rotate('y', ROTATION_STEP, polygons),
        'c': lambda: rotate('y', -ROTATION_STEP, polygons),
        's': lambda: rotate('x', ROTATION_STEP, polygons),
        'x': lambda: rotate('x', -ROTATION_STEP, polygons),
        'a': lambda: rotate('z', ROTATION_STEP, polygons),
        'z': lambda: rotate('z', -ROTATION_STEP, polygons)

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