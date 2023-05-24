import math

def lerp(a, b, t):
    return a + (b - a) * t

def clamp(value, bottom, top):
    return max(bottom, min(value, top))

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)