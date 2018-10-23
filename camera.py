from point import Point3D
from prim import Prim
from math import pi
import tkinter as tk

def draw():
    canvas.delete(tk.ALL)

    def center(point2D):
        return (WIDTH/2 + point2D.x, HEIGHT/2 - point2D.y)

    for prim in prims:
        for poligon2D in prim.get_poligons2D(DISTANCE):
            canvas.create_line(*center(poligon2D[0]), *center(poligon2D[1]), *center(poligon2D[2]), *center(poligon2D[3]), *center(poligon2D[0]), fill = prim.color)

def move(axis, step):
    list(map(lambda prim: prim.move(axis, step), prims))


def rotate(axis, angle):
    list(map(lambda prim: prim.rotate(axis, angle), prims))

def zoom(step):
    global DISTANCE
    DISTANCE += step


WIDTH = HEIGHT = 502
DISTANCE = 200
ZOOM_STEP = 5
MOVE_STEP = 2
ROTATION_STEP = pi/90

prims = [
    Prim(Point3D(-45, -20, 105), 90, 40, 40, 'purple'),
    Prim(Point3D(25, -20, 50), 25, 25, 25),
    Prim(Point3D(-50, -20, 50), 25, 25, 25, 'green')
]

def key(event):

    handler = {
        '2': lambda: move('y', MOVE_STEP),
        '8': lambda: move('y', -MOVE_STEP),
        '4': lambda: move('x', MOVE_STEP),
        '6': lambda: move('x', -MOVE_STEP),
        '0': lambda: move('z', MOVE_STEP),
        '5': lambda: move('z', -MOVE_STEP),

        '-': lambda: zoom(-ZOOM_STEP),
        '+': lambda: zoom(ZOOM_STEP),

        'd': lambda: rotate('y', ROTATION_STEP),
        'c': lambda: rotate('y', -ROTATION_STEP),
        's': lambda: rotate('x', ROTATION_STEP),
        'x': lambda: rotate('x', -ROTATION_STEP),
        'a': lambda: rotate('z', ROTATION_STEP),
        'z': lambda: rotate('z', -ROTATION_STEP)

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

