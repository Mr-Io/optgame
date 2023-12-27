from math import floor, inf
from copy import deepcopy

from base import BaseProd
from prod import Resource

def round_100(x):
    return round(x/100)*100

class Research():
    def __init__(self, player):
        self.player= player
        player.research = self


class Energy(BaseProd):
    def __init__(self, level, research) -> None:
        self.lvl = level
        research.energy = self

    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(0, 800*pow(2, lvl-1),  400*pow(2, lvl-1))
    

class Plasma(BaseProd):
    def __init__(self, level, research) -> None:
        self.lvl = level
        self.research = research
        research.plasma = self

    
    def prod_diff(self):
        total = Resource()
        for p in self.research.player.planets:
            total += p.mine_prod()
        total.m *= 0.01
        total.c *= 0.0066
        total.d *= 0.0033
        return total

    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(2000*pow(2, lvl-1),  4000*pow(2, lvl-1), 1000*pow(2, lvl-1))
    

class Astro(BaseProd):
    def __init__(self, level, research) -> None:
        self.lvl = level
        self.research = research
        research.astro = self

    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(round_100(4000*pow(1.75, lvl-1)),  round_100(8000*pow(1.75, lvl-1)), round_100(4000*pow(1.75, lvl-1)))
    
    def n_planets(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return 1 + floor((self.lvl+1)/2)


class Inter(BaseProd):
    def __init__(self, level, research) -> None:
        self.lvl = level
        self.research = research
        research.inter= self

    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(240000*pow(2, lvl-1),  400000*pow(2, lvl-1), 160000*pow(2, lvl-1))
    
    def n_labs(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return 1 + lvl 
    
    def time_mult(self, inter_lvl=None, lab_lvl=None, extra=0):
        if not inter_lvl:
            inter_lvl = self.lvl
        if not lab_lvl:
            lab_lvl = self.research.player.planet.lab.lvl
        return 1/(1+lab_lvl*self.n_labs(inter_lvl) + extra)
    
    def price_time(self, inter_lvl=None, lab_lvl=None):
        if not inter_lvl:        
            inter_lvl = self.lvl
        if not lab_lvl:
            lab_lvl = self.research.player.planet.lab.lvl
        dt = (self.time_mult(inter_lvl=inter_lvl-1, lab_lvl=lab_lvl)-self.time_mult(inter_lvl=inter_lvl, lab_lvl=lab_lvl))
        return self.cost(inter_lvl).uv()/dt if dt != 0 else inf
    
    def price_time_extralab(self, inter_lvl=None, lab_lvl=None):
        lab = self.research.player.planet.lab
        if not inter_lvl:        
            inter_lvl = self.lvl
        if not lab_lvl:
            lab_lvl = lab.lvl
        return lab.cost(lab_lvl+1).uv()/(self.time_mult(inter_lvl=inter_lvl, lab_lvl=lab_lvl)-self.time_mult(inter_lvl=inter_lvl, lab_lvl=lab_lvl, extra=1))