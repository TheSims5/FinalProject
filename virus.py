#==============================================================================
# Virus class
#
# Author: Martin Devera
# May 2017
#==============================================================================

import numpy as np

class Virus(object):
    """Create and manage a virus.


    
    Attributes
    ----------
    probability: float 
       Virus's inherent probability (0.0 - 1.0) of infection.
       
    incubation_period: int
        Incubation period in days
        
    infecting_starts: int
        Timestep that the virus first infected an agent
    
    infecting_ends: int
        Timestep that the virus is no longer contagious/cured
        
    sickness_lasts: int
        Number of timesteps that the virus lasted
        
    extra_immunity_boost: float
        seasonal variation factor boost in virus infection probability
    
    extra_immunity_lasts: int
        Number of timesteps the seasonal boost lasts
        
    mutation_day: int
        Day where the virus recieves mutation boost factor to infection probability
        
    mutation_boost: float
        Factor to boost to infection probability

    """

    DEFAULT_PROB = 0.2
    
    
    def __init__(self, probability=0.5, incubation_period=2, infecting_starts=0,infecting_ends=-1, \
                sickness_lasts=0, extra_immunity_boost=0, extra_immunity_lasts=0, mutation_day = -1, \
                mutation_boost = 0):
                
        self.probability = probability 
        self.incubation_period= incubation_period
        self.infecting_starts= infecting_starts 
        self.infecting_ends= infecting_ends
        self.sickness_lasts = sickness_lasts
        self.extra_immunity_boost= extra_immunity_boost
        self.extra_immunity_lasts = extra_immunity_lasts
        self.mutation_day = mutation_day 
        self.mutation_boost = mutation_boost

    #Returns a float representing the probability of getting infected for a given agent in
    # a given institution on a given day
    def getProbability(self, institution, agent, day):
        prob = institution.number_infectious_agents(institution, agent.time)/institution.number_of_agents(institution, agent.time)
        prob = prob * agent.time * institution.probability * agent.probability *self.probability * (int(day/self.mutation_day)* (1+self.mutation_boost))
        return prob
        
