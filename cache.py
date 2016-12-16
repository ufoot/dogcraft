def _cache_key(x, y, z):
    return "%d:%d:%d" % (x, y, z)


class RenderCache(object):
    """RenderCache is here to avoid saturating the command pipeline,
       it does add-up code but on frequent refreshes it will actually
       communicate with Minecraft only if the data changed for real."""

    def __init__(self, mc):
        self._cache = {}
        self.query = 0
        self.hit = 0
        self.miss = 0
        self.mc = mc

    def setBlock(self, x, y, z, block, data={}):
        self.query += 1
        if not self.query % 100000:
            print("cache hit=%d miss=%d" % (self.hit, self.miss))
        key = _cache_key(x, y, z)
        if key in self._cache and self._cache[key] == (block, data):
            self.hit += 1
            return True  # HIT
        self._cache[key] = (block, data)
        self.mc.setBlock(x, y, z, block, data)
        self.miss += 1
        return False  # MISS
