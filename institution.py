#==============================================================================
# Institution class
#
# Author: Zhiming Zhong
# May 2017
#==============================================================================



class Institution(object):
    """Create and manage an institution. An institution is any type of environment to which students can be assigned 
    for the duration of a time interval in the simulation.

    Attributes
    ----------
    name: string
        name of institution
        
    infection_probability : float
        probability that a susceptible student in this institution would be infected by an adjacent infected student.
        
    posn : tuple
        describes the physical boundaries of the institution, in this form: (x_min, x_max, y_min, y_max)
        
    """

    def __init__(self, name, infection_probability=0.0, posn=(0,0,0,0)):
        self.name = name
        self.infection_probability = infection_probability
        self.posn = posn