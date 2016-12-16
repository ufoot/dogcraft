import freetype
import functools

_face = None
_char_cache = {}
_text_cache = {}

FONT_FILE = "data/FreeSansBold.ttf"
COLUMN_SPACE = 1
CHAR_SIZE = 1000


def initialize_font():
    global _face
    _face = freetype.Face(FONT_FILE)
    _face.set_char_size(CHAR_SIZE)


def get_char(c):
    """Returns an array of cols for a char, filled with true or false if that pixel is to be drawn or not."""
    global _face
    global _char_cache
    if c in _char_cache:
        return _char_cache[c]
    _face.load_char(c)
    bitmap = _face.glyph.bitmap
    w = bitmap.width
    l = len(bitmap.buffer)
    if w <= 0 or l <= 0:
        return []
    h = int(l / w)
    ret = []
    for i in range(w):
        ret.append([])
        for j in range(h):
            ret[i].append(bitmap.buffer[(h - j - 1) * w + i] >= 127)
    _char_cache[c] = ret
    return ret


def get_text(t):
    """Returns an array of cols for a complete sentence, filled with true or false if that pixel is to be drawn or not."""
    global _text_cache
    if t in _text_cache:
        return _text_cache[c]
    if len(t) <= 0:
        return []
    bitmaps = [get_char(c) for c in t]
    widths = [len(b) for b in bitmaps]
    heights = [len(b[0]) if len(b) > 0 else 0 for b in bitmaps]
    width = functools.reduce(lambda a, b: a + b + COLUMN_SPACE, widths)
    height = functools.reduce(lambda a, b: max(a, b), heights)
    if width <= 0 or height <= 0:
        return []
    ret = []
    for i in range(width):
        ret.append([])
        for j in range(height):
            ret[i].append(False)
    i = 0
    for bitmap in bitmaps:
        for column in bitmap:
            ret[i][:len(column)] = column
            i += 1
        i += COLUMN_SPACE
    _letter_cache = ret
    return ret

if __name__ == '__main__':
    initialize_font()
    print(get_text("DataDog"))
