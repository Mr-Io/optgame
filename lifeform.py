from base import BaseProd
from prod import Resource

class DisruptionChamber(BaseProd):
    def __init__(self, level, planet) -> None:
        self.lvl = level
        self.planet = planet
        self.planet.disruption_chamber = self
    
    def prod(self, lvl=None):
        return Resource()

    def prod_diff(self):
        return Resource()

    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(20000*pow(1.2, lvl-1)*lvl, 15000*pow(1.2, lvl-1)*lvl, 10000*pow(1.2, lvl-1)*lvl)

    def energy(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return self.energy_diff()*self.lvl 
    
    def energy_diff(self, start=None, end=None):
        if not start:
            start = self.lvl - 1
        if not end:
            end = self.lvl
        return (end - start) * (0.015*self.planet.energy_base() - 0.005*self.planet.mine_energy() - 0.005*self.planet.crawlers.energy())

    def energy_reduction_mult(self):
        return (1 - self.lvl*0.005)
