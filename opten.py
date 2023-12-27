import math

from accounts import *
from facilities import *
from copy import deepcopy

def _price_energy_nextlvl(item):
    c = item.cost(item.lvl+1).uv()
    e = item.energy_diff(start=item.lvl, end=item.lvl+1) 
    return c/e if e != 0 else math.inf

def _balance_basic_energy(plt):
    min_value = math.inf
    item, lvls = plt.fusion_reactor, 1
    # solar_plant
    price_energy_sp = _price_energy_nextlvl(plt.solar_plant)
    if price_energy_sp < min_value:
        item, lvls = plt.solar_plant, 1
        min_value = price_energy_sp
    #satellites
    price_energy_st = _price_energy_nextlvl(plt.satellites)
    if price_energy_st < min_value:
        item, lvls = plt.satellites, 1
        min_value = price_energy_st
    # disruption chamber
    price_energy_dc = _price_energy_nextlvl(plt.disruption_chamber)
    if price_energy_dc < min_value:
        item, lvls = plt.disruption_chamber, 1
        min_value = price_energy_dc
    # lvl up
    item.lvl += lvls
    #plt.player.last_updated = item


def balance_energy(ply, absolute=True):
    plt = ply.planet
    min_price, min_ply= math.inf, ply
    range_fusion = range(0, 30) if absolute else range(ply.planet.fusion_reactor.lvl, 30)
    range_energy = range(0, 30) if absolute else range(ply.research.energy.lvl, 30)
    sp_start = 0 if absolute else plt.solar_plant.lvl
    st_start = 0 if absolute else plt.satellites.lvl
    dc_start = 0 if absolute else plt.disruption_chamber.lvl
    for i in range_fusion: #if plt.deut_mine.lvl >= 5 else (0,):
        for j in range_energy if i>0 else (0,):
            plt.fusion_reactor.lvl = i
            ply.research.energy.lvl = j
            plt.solar_plant.lvl = sp_start
            plt.satellites.lvl = st_start
            plt.disruption_chamber.lvl = dc_start
            while(plt.energy() <= 0):
                _balance_basic_energy(plt)
            price = ply.price_eprod() #ply.price_eprod_ecorr()
            #print(ply)
            if min_price > price or min_price is math.inf:
                min_price, min_ply= (price, deepcopy(ply))

    plt.fusion_reactor.lvl = min_ply.planet.fusion_reactor.lvl
    ply.research.energy.lvl = min_ply.research.energy.lvl
    plt.solar_plant.lvl = min_ply.planet.solar_plant.lvl
    plt.satellites.lvl = min_ply.planet.satellites.lvl
    plt.disruption_chamber.lvl = min_ply.planet.disruption_chamber.lvl
    ply.last_updated = min_ply.last_updated
    
if __name__ == "__main__":

    uni = Universe(8)
    ply = Player("mrio", uni)
    research = Research(ply)
    plasma = Plasma(17, research)
    energy = Energy(0, research)
    astro = Astro(20, research)
    plt = Planet(1, 8, 30, ply)


    # Resources
    mm = MetalMine(37, plt, uni)
    cm = CrystalMine(31, plt, uni)
    dm = DeutMine(32, plt, uni)

    # Energy
    sp = SolarPlant(0, plt)
    fr = FusionReactor(0, plt, uni)
    disrupt = DisruptionChamber(0,plt)
    sat = Satellites(0, plt)
    dc = DisruptionChamber(0, plt)

    StorageMetal(13,  plt)
    StorageCrystal(10,  plt)
    StorageDeut(10,  plt)
    Crawlers(0, plt)
    rb = Robot(13, plt)
    nn = Nanite(5, plt)
    ply.research.astro.lvl = 19
    print("---- astro 19 ----")
    balance_energy(ply)
    print(ply)
    print("---- astro 20 ----")
    ply.research.astro.lvl = 20
    balance_energy(ply)
    print(ply)

