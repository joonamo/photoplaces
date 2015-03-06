class color():
    def __init__(self,r,g,b):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)

    def __str__(self):
        return ("rgb(%d, %d, %d)" % (self.r, self.g, self.b))

    def __repr__(self):
        return ("rgb(%d, %d, %d)" % (self.r, self.g, self.b))

    def __add__(self, other):
        return color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, other):
        return color(self.r - other.r, self.g - other.g, self.b - other.b)

    def __mul__(self, other):
        if isinstance(other, color):
            return color(self.r * other.r, self.g * other.g, self.b * other.b)
        else:
            other = float(other)
            return color(self.r * other, self.g * other, self.b * other)

    def __truediv__(self, other):
        if isinstance(other, color):
            return color(self.r / other.r, self.g / other.g, self.b / other.b)
        else:
            other = float(other)
            return color(self.r / other, self.g / other, self.b / other)      

def lerp(v0, v1, t):
    return v0 + (v1 - v0) * t

def generate_color_map(colors):
    colors.append(colors[0])
    result = [None] * 13
    result[0] = colors[0]
    result[12] = colors[0]
    last_idx = 0
    for i in xrange(1, len(colors)):
        idx = int(float(i) / (len(colors) - 1) * 12)
        for j in xrange(last_idx + 1, idx + 1):
            result[j] = lerp(colors[i], colors[i - 1], (1.0 - (j - last_idx) / float(idx - last_idx)))
        last_idx = idx

    out = ""
    for i in xrange(12):
        out += ".month_%d {fill: %s;}\n" % (i + 1, result[i])
    return out
