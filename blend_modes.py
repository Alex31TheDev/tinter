import math

def multiplicative_blend(pixel, color):
    return (math.floor(pixel[0] * color[0]),
            math.floor(pixel[1] * color[1]),
            math.floor(pixel[2] * color[2]))

blend_modes = [multiplicative_blend]
