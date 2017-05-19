# ==============================================================================
# ParkingArea class
#
# Author: Hoi Yan Wu
# May 2017
# ==============================================================================

from institution import Institution

class ParkingArea(Institution):
    
    """Create and manage a Parking Area. 
    An institution is any type of environment to which students 
    can be assigned for the duration of a time interval in the simulation.
            
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
        
    """
    def __init__(self, type= 'parking_area', infection_probability=0.0, geographical_loc=(0, 0, 0, 0), list_students=[], \
                 door_locs=[]):
        Institution.__init__(self, type, infection_probability, geographical_loc, list_students)
        self.door_locs = door_locs
        