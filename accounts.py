import math

from functools import reduce

from lifeform import *
from prod import *
from research import *

class Universe():
    def __init__(self, economy):
        self.eco = economy

class Player():
    def __init__(self, name, universe, research=None) -> None:
        self.id = name
        self.uni = universe
        self.research = research
        self.planet = None
        self.last_updated = None
    
    def n_planets(self):
        return self.research.astro.n_planets()

    def price_eprod(self):
        c = self.totalcost().uv()
        p = self.prod().uv()
        return c/p if p != 0 else c 
    
    def price_eprod_ecorr(self):
        c = self.totalcost().uv()
        p = self.prod().uv()
        es = self.planet.energy() * self.n_planets()
        ep = (self.planet.energy_base() + self.planet.disruption_chamber.energy())*self.n_planets()
        ppe = p / ep if ep != 0 else 0
        return c/(p + ppe*es) if (p + ppe*es) > 0 else c

    
    def prod(self):
        return self.planet.prod()*self.n_planets()

    def totalcost(self):
        return self.planet.totalcost()*self.n_planets() + self._totalcost_research()
    
    def _totalcost_research(self):
        res = Resource()
        res += self.research.energy.totalcost(lvl_start=13)
        res += self.research.plasma.totalcost(lvl_start=8)
        res += self.research.astro.totalcost()
        return res
    
    def __str__(self):
        return ''.join(f"{self.price_eprod():10,.4f} {self.price_eprod_ecorr():10,.4f} {self.n_planets():2d}: {self.research.inter.lvl:2d} {self.planet.lab.lvl:2d} -- {self.planet} {self.last_updated.__class__.__name__ if self.last_updated else None} ")

    __repr__ = __str__

class Planet():
    def __init__(self, id, position, temperature, player):
        self.id = id
        self.pos = position
        self.t = temperature
        self.player = player
        self.last_updated = None
        self.player.planet = self
    
    def totalcost(self):
        return self._totalcost_resources() + self._totalcost_facilities() + self._totalcost_lifeform()

    def _totalcost_resources(self):
        res = Resource()
        res += self.metal_mine.totalcost()
        res += self.crystal_mine.totalcost() 
        res += self.deut_mine.totalcost()
        res += self.solar_plant.totalcost()
        res += self.fusion_reactor.totalcost()
        res += self.satellites.totalcost()
        res += self.storage_metal.totalcost()
        res += self.storage_crystal.totalcost()
        res += self.storage_deut.totalcost()
        res += self.crawlers.totalcost()
        return res

    def _totalcost_facilities(self):
        res = Resource()
        res += self.robot.totalcost()
        #res += self.shipyard.totalcost() 
        #res += self.lab.totalcost()
        #res += self.silo.totalcost()
        res += self.nanite.totalcost()
        #res += self.terraformer.totalcost() 
        return res
    
    def _totalcost_lifeform(self):
        res = Resource()
        #res += self.meditation_enclave.totalcost()
        #res += self.crystal_farm.totalcost()
        #res += self.rune_technologium.totalcost()
        #res += self.rune_forge.totalcost()
        #res += self.oriktorium.totalcost()
        #res += self.magma_force.totalcost()
        res += self.disruption_chamber.totalcost()
        #res += self.megalith.totalcost()
        #res += self.crystal_refinery.totalcost()
        #res += self.deuterium_synthetiser.totalcost()
        #res += self.mineral_research_center.totalcost()
        #res += self.advanced_recycling_plant.totalcost()
        return res
    
    def mine_prod(self):
        return self.metal_mine.prod() + self.crystal_mine.prod() + self.deut_mine.prod()

    def mine_energy(self):
        return self.metal_mine.energy() + self.crystal_mine.energy() + self.deut_mine.energy()
    
    def plasma_prod(self):
        mp = self.mine_prod()
        return Resource(mp.m*0.01, mp.c*0.0066,  mp.d*0.0033)*self.player.research.plasma.lvl
    
    def prod(self):
        prod = self.mine_prod() + self.plasma_prod() + self.fusion_reactor.prod()
        if prod.d < 0:
            prod.d = 0
        return prod
    
    def energy_base(self):
        return self.solar_plant.energy() + self.fusion_reactor.energy() + self.satellites.energy()
    
    def energy(self):
        return self.mine_energy() + self.crawlers.energy() + self.energy_base() + self.disruption_chamber.energy()
    
    def max_crawler_lvl(self):
        return int(min(1112, 8*1.1*(self.metal_mine.lvl + self.crystal_mine.lvl + self.deut_mine.lvl)))
    
    def __str__(self):
        return f" {self.nanite.lvl:2d} {self.robot.lvl:2d} {self.shipyard.lvl:2d} -- {self.metal_mine.lvl:2d} {self.crystal_mine.lvl:2d} {self.deut_mine.lvl:2d} ({self.storage_metal.lvl:2d} {self.storage_crystal.lvl:2d} {self.storage_deut.lvl:2d}) {self.crawlers.lvl:3d}/{self.max_crawler_lvl()} - {self.player.research.plasma.lvl:2d}  --  {self.solar_plant.lvl:2d} {self.fusion_reactor.lvl:2d} {self.satellites.lvl:3d} - {self.player.research.energy.lvl:2d} - {self.disruption_chamber.lvl:2d}  -- {self.energy():6,.0f}  -- "
    
    __repr__ = __str__


    