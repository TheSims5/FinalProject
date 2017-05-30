#==============================================================================
# Activity class
#
# Author: Zhiming Zhong
# May 2017
#==============================================================================

from course import Course
import numpy as np

class Activity(object):
    """Create and manage an Activity. 

    Attributes
    ----------
    # type: int
    #     type of Activity. (0 == course, 1 == other)
        
    start_time : int
        minute that the Activity begins
        
    end_time : int
        minute that the Activity ends
        
    dest_intitution_int: int
        number representation of the institution where the Activity takes place.
        
    communities: list
        contains int representation of each community that can perform this Activity.
        
    """


    def __init__(self, course):
        self.start_time = course.start_time - np.random.randint(10,15)
        self.end_time = course.end_time
        self.dest_institution_int = course.dest_institution_int
        self.course = course
        self.seat_posn = None
        # self.communities = communities

    def display(self):
        print("start_time: " + str(self.start_time))
        print("end_time: " + str(self.end_time))
        print("destination institution: " + str(self.dest_institution_int))


