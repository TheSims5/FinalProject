#Virus Class

import numpy as np

class Virus(object):
    """Create and manage a virus.

    Attributes
    ----------
    #ToDo
    """
    def __init__(self, infection_probability = 0.2, incubation_period=2, infecting_starts=0,infecting_ends=100,sickness_lasts=0,extra_immunity_boost=0, extra_immunity_lasts=0):
                
        self.infection_probability = self.getProbability(self)
        self.incubation_period= incubation_period
        self.infecting_starts= infecting_starts
        self.infecting_ends= infecting_ends
        self.sickness_lasts = sickness_lasts
        self.extra_immunity_boost= extra_immunity_boost
        self.extra_immunity_lasts = extra_immunity_lasts

    def getProbability(self):
        #todo, use formula from table 1
        pass
        
        