# ==============================================================================
# Classroom class
#
# Author: Zhiming Zhong
# May 2017
# ==============================================================================

import numpy as np

class Classroom:
    """Create and manage a classroom.
 
    Attributes
    ----------
        
    posn : tuple
        describes the physical boundaries of the institution, in this form: (x_min, x_max, y_min, y_max)

    open: list of bool
   (length == # of time slots. indicates whether the classroom has already been assigned to a course during each time slot) 
   
    """

    NUM_OF_TIMESLOTS = 6

    def __init__(self, posn=[0,0,0,0]):
        self.posn = posn
        self.open = np.ones(self.NUM_OF_TIMESLOTS)