import math

from opten import balance_energy
from accounts import *
from facilities import *

def _balance_storage(plt, hours=48):
    prod = plt.prod()*hours# daily production
    # metal
    if prod.m > plt.storage_metal.capacity().m:
        plt.storage_metal.lvl += 1
        plt.player.last_updated = plt.storage_metal
    # crystal 
    if prod.c > plt.storage_crystal.capacity().c:
        plt.storage_crystal.lvl += 1
        plt.player.last_updated = plt.storage_crystal
    # deut
    if prod.d > plt.storage_deut.capacity().d :
        plt.storage_deut.lvl += 1
        plt.player.last_updated = plt.storage_deut

def _balance_time(plt): 
    nn = plt.nanite
    rb = plt.robot
    sh = plt.shipyard
    while(plt.nanite.lvl < plt.player.n_planets()//2):
        item = None
        nn_price = nn.price_time(nn.lvl+1)
        rb_price = rb.price_time(rb.lvl+1)
        sh_price = sh.price_time(sh.lvl+1)
        #print(f"price nn: {nn_price}")
        #print(f"price rb: {rb_price}")
        #print(f"price sh: {sh_price}")
        if rb.lvl >= 10 and nn_price <= rb_price and nn_price <= sh_price:
            item = nn
        elif rb.lvl >= 2 and sh_price <= rb_price:
            item = sh
        else:
            item = rb
        item.lvl += 1
        #print(f"lvl up {item}")
        plt.player.last_updated = item

def _balance_research(plt): 
    lab = plt.lab
    inter = plt.player.research.inter
    while (inter.n_labs() < plt.player.n_planets()):
        item = None
        inter_price = inter.price_time(inter_lvl= inter.lvl+1)
        lab_price = inter.price_time_extralab()
        #print(f"price inter: {inter_price}")
        #print(f"price lab: {lab_price}")
        if inter_price < lab_price:
            item = inter
        else:
            item = lab
        item.lvl += 1
        #print(f"lvl up {item}")
        plt.player.last_updated = item

def _price_prod_nextlvl(ply, item, min_item, min_price, min_lvl_incr):
        lvl_incr = 1
        if isinstance(item, Astro) and item.lvl != 0:
            lvl_incr = 2
        elif isinstance(item, Crawlers):
            lvl_incr = int(ply.planet.energy()//50)
            if lvl_incr == 0:
                lvl_incr = 1
            max_lvl_incr = ply.planet.max_crawler_lvl()- ply.planet.crawlers.lvl
            if lvl_incr > max_lvl_incr:
                lvl_incr = max_lvl_incr
        item.lvl += lvl_incr
        balance_energy(ply)
        pp = ply.price_eprod_ecorr() if lvl_incr != 0 else math.inf
        #print(f"{pp:10,.4f} - {item} - lvl:{item.lvl} (increase:{lvl_incr})")
        item.lvl -= lvl_incr
        if pp < min_price:
            return item, pp, lvl_incr
        else:
            return min_item, min_price, min_lvl_incr


def next(ply):
    plt = ply.planet
    if plt.energy() <= 0:
        return balance_energy(ply)
    else:
        _balance_time(plt)
        _balance_storage(plt)
        _balance_research(plt)
        # metal mine
        min_item, min_pp, min_lvl_incr = None, math.inf, 1
        for item in (plt.metal_mine, plt.crystal_mine, plt.deut_mine, plt.crawlers, ply.research.plasma, ply.research.astro):
            min_item, min_pp, min_lvl_incr = _price_prod_nextlvl(ply, item, min_item, min_pp, min_lvl_incr)
        # lvl up winner
        min_item.lvl += min_lvl_incr
        plt.player.last_updated = min_item
        balance_energy(ply)
        #print(f"winner: {min_item}m increase {min_lvl_incr} lvls")

if __name__ == "__main__":
    uni = Universe(8)
    ply = Player("mrio", uni)
    research = Research(ply)
    plasma = Plasma(0, research)
    energy = Energy(0, research)
    astro = Astro(0, research)
    inter = Inter(0, research)
    plt = Planet(1, 8, 30, ply)


    # Resources
    mm = MetalMine(0, plt, uni)
    cm = CrystalMine(0, plt, uni)
    dm = DeutMine(0, plt, uni)
    cw = Crawlers(0, plt, uni)
    sp = SolarPlant(0, plt)
    fr = FusionReactor(0, plt, uni)
    disrupt = DisruptionChamber(0,plt)
    sat = Satellites(0, plt)
    #lifeforms
    dc = DisruptionChamber(0, plt)

    StorageMetal(0,  plt)
    StorageCrystal(0,  plt)
    StorageDeut(0,  plt)
    rb = Robot(0, plt)
    sh = Shipyard(0, plt)
    nn = Nanite(0, plt)
    lab = Lab(0, plt)
    print(ply)
    while ply.totalcost().uv() < pow(10, 14):
        next(ply)
        print(ply)
    while ply.planet.energy() < 0:
        balance_energy(ply)
        print(ply)

