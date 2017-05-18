# ==============================================================================
# Building class
#
# Author: Zhiming Zhong
# May 2017
# ==============================================================================


from institution import Institution

class Building(Institution):
    """Create and manage an institution of the type "building." 
    An institution is any type of environment to which students can be assigned 
    for the duration of a time interval in the simulation.

    Attributes
    ----------
    type : string 
        type of institution 

    infection_probability : float
        probability that a susceptible student in this institution would be infected by an adjacent infected student.
        
    geographical_loc : tuple
        describes the physical boundaries of the institution, in this form: (x_min, x_max, y_min, y_max)
        
    list_students : List
        contains all students currently in the institution
        
    opening_time: float
        hour at which building opens (e.g. 7.25 == 7:15 a.m.)
    
    closing_time: float
        hour at which building opens
    
    door_locs: # List of tuples
        contains coordinates of door locations of building

    """

    def __init__(self, type='building', infection_probability=0.0, geographical_loc=(0, 0, 0, 0), list_students=[], \
                 opening_time=0.0, closing_time=0.0, door_locs=[]):
        Institution.__init__(self, type, infection_probability, geographical_loc, list_students)
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.door_locs = door_locs

