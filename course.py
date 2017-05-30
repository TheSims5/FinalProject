#==============================================================================
# Course class
#
# Author: The Sims 5
# May 2017
#==============================================================================
import numpy as np
from classroom import Classroom

CAPACITY = 50
class Course(object):
    """
        
    """

    def __init__(self, start_time, end_time, dest_institution_int, classroom):
        self.start_time = start_time
        self.end_time = end_time
        self.dest_institution_int = dest_institution_int
        self.capacity = CAPACITY
        self.cur_num_of_students = 0
        self.classroom_x_min = classroom.posn[0]
        self.classroom_y_min = classroom.posn[2]
        self.x_size_of_classroom = classroom.posn[1]-classroom.posn[0]-2
        self.y_size_of_classroom = classroom.posn[3]-classroom.posn[2]-2
        
        
        self.open_seats = np.ones((self.y_size_of_classroom,self.x_size_of_classroom), dtype = np.bool)
        
        # self.communities = communities

    def display(self):
        print("start_time: " + str(self.start_time))
        print("end_time: " + str(self.end_time))
        print("destination institution: " + str(self.dest_institution_int))

    

