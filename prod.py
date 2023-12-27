import math

from copy import deepcopy

from base import BaseProd, Resource



class StorageMetal(BaseProd):

    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.storage_metal = self
    
    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(1000 * pow(2, lvl-1), 0, 0)
    
    def capacity(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(5000*math.floor(2.5*pow(math.e, 20/33*lvl)), 0, 0)


class StorageCrystal(BaseProd):

    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.storage_crystal = self
    
    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(1000*pow(2, lvl-1), 500*pow(2, lvl-1), 0)
 
    def capacity(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(0, 5000*math.floor(2.5*pow(math.e, 20/33*lvl)), 0)


class StorageDeut(BaseProd):

    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.storage_deut = self
    
    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(1000*pow(2, lvl-1), 1000*pow(2, lvl-1), 0)
 
    def capacity(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(0, 0, 5000*math.floor(2.5*pow(math.e, 20/33*lvl)))
    


class MetalMine(BaseProd):
    def __init__(self, level, planet, universe):
        self.lvl = level
        self.planet = planet
        self.uni = universe
        self.planet.metal_mine = self
    
    def bonus(self):
        if self.planet.pos == 8:
            return 1.35
        if self.planet.pos == 7 or self.planet.pos == 9:
            return 1.24
        if self.planet.pos == 6 or self.planet.pos == 10:
            return 1.17
        return 1

    def prod(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(30*lvl*pow(1.1, lvl)*self.bonus()*self.uni.eco, 0, 0)

    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(60 * pow(1.5, lvl-1), 15 * pow(1.5, lvl-1), 0)
    
    def energy(self):
        return -10*self.lvl*pow(1.1, self.lvl)
    
    def energy_wdc(self):
        return self.energy()*self.planet.disruption_chamber.energy_reduction_mult()



class CrystalMine(BaseProd):
    def __init__(self, level, planet, universe):
        self.lvl = level
        self.planet = planet
        self.uni = universe
        self.planet.crystal_mine = self

    def bonus(self):
        if self.planet.pos == 1:
            return 1.40
        if self.planet.pos == 2:
            return 1.30
        if self.planet.pos == 3:
            return 1.20
        return 1

    def prod(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(0, 20*lvl*pow(1.1, lvl)*self.bonus()*self.uni.eco, 0)

    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(48 * pow(1.6, lvl-1), 24 * pow(1.6, lvl-1), 0)
    
    def energy(self):
        return -10*self.lvl*pow(1.1, self.lvl)

    def energy_wdc(self):
        return self.energy()*self.planet.disruption_chamber.energy_reduction_mult()


class DeutMine(BaseProd):
    def __init__(self, level, planet, universe):
        self.lvl = level
        self.planet = planet
        self.uni = universe
        self.planet.deut_mine = self

    def prod(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(0, 0, 10*lvl*pow(1.1, lvl)*(1.36 - 0.004*self.planet.t)*self.uni.eco)

    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(225*pow(1.5, lvl-1), 75*pow(1.5, lvl-1), 0)
    
    def energy(self):
        return -20*self.lvl*pow(1.1, self.lvl)

    def energy_wdc(self):
        return self.energy()*self.planet.disruption_chamber.energy_reduction_mult()


class SolarPlant(BaseProd):
    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.solar_plant = self
    
    def prod(self):
        return Resource()

    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(75*pow(1.5, lvl-1), 30*pow(1.5, lvl-1), 0)
    
    def energy(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return 20*lvl*pow(1.1, lvl)
    
    def prod_diff(self):
        plt = deepcopy(self.planet)
        plt.solar_plant.lvl -= 1
        return self.prod() - plt.solar_plant.prod()


class FusionReactor(BaseProd):
    def __init__(self, level, planet, universe):
        self.lvl = level
        self.planet = planet
        self.planet.fusion_reactor = self
        self.uni = universe

    def prod(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(0, 0, -10*lvl*pow(1.1, lvl)*self.uni.eco)

    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(900*pow(1.8, lvl-1), 360*pow(1.8, lvl-1), 180*pow(1.8, lvl-1))
    
    def energy(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return 30*lvl*pow(1.05 + self.planet.player.research.energy.lvl*0.01, lvl)


class Crawlers(BaseProd):
    def __init__(self, number, planet):
        self.lvl = number
        self.planet = planet
        self.planet.crawlers = self
    
    def prod(self):
        return Resource()
    
    def cost(self):
        return Resource()

    def totalcost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return self.cost()*lvl

    def energy(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return  self.energy_diff()*lvl
    
    def energy_diff(self, start=None, end=None):
        if start is None:
            start = self.lvl -1 
        if end is None:
            end = self.lvl
        return -50 * (end - start)


class Satellites(BaseProd):
    def __init__(self, number, planet):
        self.lvl = number
        self.planet = planet
        self.planet.satellites = self
    
    def prod(self, lvl=None):
        return Resource()
    
    def cost_wdc(self):
        return Resource(0, 2000, 500)

    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        if lvl < 100:
            k = 5
        elif lvl < 200:
            k = 10
        elif lvl < 500:
            k = 20
        elif lvl < 1000:
            k = 50
        else:
            k = 500 #math.inf
        return Resource(0, 2000, 500) * k

    def totalcost_wdc(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return self.cost_wdc()*lvl

    def totalcost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return sum(iter(self.cost(i) for i in range(1, lvl+1)), Resource())

    def energy(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return lvl*self.energy_diff()
    
    def energy_diff(self, start=None, end=None):
        if start is None:
            start = self.lvl - 1
        if end is None:
            end = self.lvl
        return (end - start) * math.floor((160 + self.planet.t)/6)


class Crawlers(BaseProd):
    def __init__(self, level, planet, universe):
        self.lvl = level
        self.planet = planet
        self.uni = universe
        self.planet.crawlers = self
    
    def prod(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        if lvl > self.planet.max_crawler_lvl():
            lvl = self.planet.max_crawler_lvl()
        return self.planet.mine_prod()*lvl*0.00045

    def cost(self, lvl=None):
        if lvl is None:
            lvl = self.lvl
        return Resource(2000, 2000, 1000)
    
    def energy(self):
        return -100*self.lvl