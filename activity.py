#==============================================================================
# Activity class
#
# Author: Zhiming Zhong
# May 2017
#==============================================================================



class Activity(object):
    """Create and manage an Activity. 

    Attributes
    ----------
    type: int
        type of Activity. (0 == course, 1 == other)
        
    start_time : int
        minute that the Activity begins
        
    end_time : int
        minute that the Activity ends
        
    dest_intitution_int: int
        number representation of the institution where the Activity takes place.
        
    communities: list
        contains int representation of each community that can perform this Activity.
        
    """


    def __init__(self, start_time=0, end_time=0, dest_institution_int=0, communities=[]):
        self.start_time = start_time
        self.end_time = end_time
        self.dest_institution_int = dest_institution_int
        self.communities = communities

    def display(self):
        print("start_time: " + str(self.start_time))
        print("end_time: " + str(self.end_time))
        print("destination institution: " + str(self.dest_institution_int))
        print("communities: " + str(self.communities))

