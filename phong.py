import math
import tkinter
import itertools
import numpy as np


WIDTH = 400
HEIGHT = 400
MOVE_STEP = 50

OBSERVER = [0, 0, 0]
CENTER = [0, 0, 200]
SOURCE = [-100, 0, 100]
RADIUS = 75

window = tkinter.Tk()
image = tkinter.PhotoImage(width=WIDTH, height=HEIGHT)
label = tkinter.Label(image=image, bg="black")
label.pack()

def glob_z_coord(x, y):
    c = CENTER[2]**2 + (x - CENTER[0])**2 + (y - CENTER[1])**2 - RADIUS**2

    b = -2 * CENTER[2]
    delta = b**2 - 4 * c

    if delta == 0:
        return -b / 2
    elif delta > 0:
        z1 = (-b - math.sqrt(delta)) / 2
        z2 = (-b + math.sqrt(delta)) / 2
        return min(z1, z2)

def vector(s_point, e_point):
    return [coor_e - coor_s for coor_s, coor_e in zip(s_point, e_point)]


def norm(vector):
    return (sum(coor**2 for coor in vector))**0.5


def versor(vector):
    n = norm(vector)
    return [coor / n for coor in vector]


def illumination(point):
    I_a = 0.5
    I_d = 1
    k_a = 0.05
    k_d = 0.5
    k_s = 0.5
    m = 100

    n = versor(vector(CENTER, point))
    v = versor(vector(point, OBSERVER))
    l = versor(vector(point, SOURCE))
    r = versor(np.subtract(np.multiply(2*np.dot(n,l), n), l))
    # r = versor(np.subtract(np.multiply(np.multiply(n, 2), np.multiply(n, l)), l))

    return I_a*k_a + I_d*(k_d * max(np.dot(n, l), 0) + k_s * max(np.dot(r, v), 0)**m)


def render():
    for x, y in itertools.product(range(-RADIUS, RADIUS), range(-RADIUS, RADIUS)):
        view_coord = (WIDTH//2 + x, HEIGHT//2 + y)
        real_coord = (CENTER[0] + x, CENTER[1] + y)
        # z=400
        z = glob_z_coord(*real_coord)
        if z:
            intensity = min(int(illumination([real_coord[0], real_coord[1], z]) * 255), 255)
            image.put('#{0:02x}{0:02x}{0:02x}'.format(intensity), view_coord)
        else:
            image.put('black', view_coord)


def move(step, coord):
    SOURCE[coord] += step

def key(event):
    handler = {
        '4': lambda: move(-MOVE_STEP, 0),
        '6': lambda: move(MOVE_STEP, 0),
        '2': lambda: move(MOVE_STEP, 1),
        '8': lambda: move(-MOVE_STEP, 1),
        '5': lambda: move(MOVE_STEP, 2),
        '0': lambda: move(-MOVE_STEP, 2),
    }.get(event.char)

    if handler:
        handler()
        render()


window.bind('<Key>', key)
render()

tkinter.mainloop()
