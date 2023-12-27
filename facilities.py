import math

from copy import deepcopy

from base import BaseProd, Resource

class Shipyard(BaseProd):
    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.shipyard = self
    
    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(400*pow(2, lvl-1), 200*pow(2, lvl-1), 100*pow(2, lvl-1))
    
    def time_mult(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return 1/(1+lvl)
    
    def price_time(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return self.cost(lvl).uv()/self.time_mult_diff(start=lvl-1, end=lvl)
    
    def time_mult_diff(self, start=None, end=None):
        if not start:
            start = self.lvl
        if not end:
            end = self.lvl - 1
        return self.time_mult(start) - self.time_mult(end)

class Lab(BaseProd):
    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.lab = self
    
    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(200*pow(2, lvl-1), 400*pow(2, lvl-1), 200*pow(2, lvl-1))
    


class Robot(BaseProd):
    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.robot = self
    
    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(400*pow(2, lvl-1), 120*pow(2, lvl-1), 200*pow(2, lvl-1))
    
    def time_mult(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return 1/(1+lvl)
    
    def price_time(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return self.cost(lvl).uv()/self.time_mult_diff(start=lvl-1, end=lvl)
    
    def time_mult_diff(self, start=None, end=None):
        if not start:
            start = self.lvl
        if not end:
            end = self.lvl - 1
        return self.time_mult(start) - self.time_mult(end)
    

class Nanite(BaseProd):
    def __init__(self, level, planet):
        self.lvl = level
        self.planet = planet
        self.planet.nanite = self
    
    def cost(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return Resource(1000000*pow(2, lvl-1), 500000*pow(2, lvl-1), 100000*pow(2, lvl-1))
    
    def time_mult(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return 1 / pow(2, lvl)
    
    def price_time(self, lvl=None):
        if not lvl:
            lvl = self.lvl
        return self.cost(lvl).uv()/self.time_mult_diff(start=lvl-1, end=lvl)
    
    def time_mult_diff(self, start=None, end=None):
        if not start:
            start = self.lvl - 1
        if not end:
            end = self.lvl
        return self.time_mult(start) - self.time_mult(end)
    