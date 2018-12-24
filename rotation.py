from math import sin, cos

class Rotation:

    @classmethod
    def get_matrix(cls, axis, angle):
        a_sin = sin(angle)
        a_cos = cos(angle)

        return {
            'x': [
                [1,     0,      0],
                [0, a_cos, -a_sin],
                [0, a_sin,  a_cos]
            ],
            'y': [
                [ a_cos, 0, a_sin],
                [     0, 1,     0],
                [-a_sin, 0, a_cos]
            ],
            'z': [
                [a_cos, -a_sin, 0],
                [a_sin,  a_cos, 0],
                [    0,      0, 1]
            ]
        }.get(axis)