#==============================================================================
# StudentHousing class
#
# Author: Zhiming Zhong
# May 2017
#==============================================================================


from institution import Institution

class StudentHousing(Institution):
    """Create and manage a student housing institution. An institution is any type of environment to which students 
    can be assigned for the duration of a time interval in the simulation.
            
            
    Attributes
    ----------
    name : string 
        name of institution 

    infec_prob : float
        probability that a susceptible student in this institution would be infected by the virus
        
    posn : tuple
        describes the physical boundaries of the institution, in this form: (x_min, x_max, y_min, y_max)
        
    door_posns: list of tuples
        each tuple is the x, y position of a door to the institution.

    """

    def __init__(self, name, infec_prob=0.0, posn=(0,0,0,0), door_posns = []):
        Institution.__init__(self, name, infec_prob, posn)
        self.door_posns = door_posns
