METAL_RATIO = 2.7
CRYSTAL_RATIO = 1.7

class BaseProd():
    def totalcost(self, lvl_end=None, lvl_start=1):
        if lvl_end is None:
            lvl_end= self.lvl
        return sum(iter(self.cost(l) for l in range(lvl_start, lvl_end + 1)), Resource())

    def prod_diff(self, start=None, end = None):
        if start is None:
            start = self.lvl - 1
        if end is None:
            end = self.lvl
        return self.prod(end) - self.prod(start)

    def energy_diff(self, start=None, end = None):
        if start is None:
            start = self.lvl - 1
        if end is None:
            end = self.lvl
        return self.energy(end) - self.energy(start)


class Resource():
    def __init__(self, metal=0, crystal=0, deut=0, ratio_metal=METAL_RATIO, ratio_crystal=CRYSTAL_RATIO):
        self.m = metal
        self.c = crystal
        self.d = deut
        self.ratio_metal = ratio_metal
        self.ratio_crystal = ratio_crystal
    
    def uv(self):
        return self.m + self.c*self.ratio_metal/self.ratio_crystal + self.d*self.ratio_metal 
    
    def __add__(self, other):
        return Resource(self.m+other.m, self.c+other.c, self.d+other.d)

    def __sub__(self, other):
        return Resource(self.m-other.m, self.c-other.c, self.d-other.d)

    def __mul__(self, n):
        return Resource(n*self.m, n*self.c, n*self.d)

    def __str__(self):
        return f'{self.m:12,.0f}   {self.c:12,.0f}   {self.d:12,.0f}'
    
    __repr__ = __str__

