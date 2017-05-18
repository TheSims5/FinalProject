#==============================================================================
# Institution class
#
# Author: Zhiming Zhong
# May 2017
#==============================================================================

from institution import Institution

class Path(Institution):
    """Create and manage a path. An institution is any type of environment to which students can be assigned 
    for the duration of a time interval in the simulation.
    """

    def __init__(self, type='off_campus', infection_probability=0.0, geographical_loc=(0,0,0,0), list_students=[]):
        Institution.__init__(self, type, infection_probability, geographical_loc, list_students)