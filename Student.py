# ==============================================================================
# Student class
#
# Author: Hoi Yan Wu
# May 2017
# ==============================================================================


# ==============================================================================
PROPORTION_STARTING_AT_PARKING_AREA = None
PROPORTION_STARTING_AT_HUSKY_VILLAGE = None

#                Parking Area         School Housing           Bus Stop                  
#Proportion 0.0_________________0.xx____________________0.xx_________________1.0

# ==============================================================================

import numpy as np
from Schedule import Schedule
from parkingArea import ParkingArea
from busStop import BusStop
from schoolHousing import SchoolHousing

class Student(object):
    
    
    """
        The constructor of student
        
        Attributes
        ----------
        type : String
            type of the agent, currently we only have Student as agent
        
        infection_probability: float [0.0,1.0)
            initial value: depends on the immunity of the student,
            the value will varied depends on the location and interactions that the student have
        
        is_infected: bool
            True: the student is infected
            False: the student is not infected
        
        schedule: Schedule
            the schedule of the student
            

        
        cur_loc: tuple
            the location that the student located
            
        cur_dest: Institution (not included path)
            either building, bus_stop, off_campus
                
                                
        final_scheduled_dest: Institution
            the final destination of the student when they finished their schedule 
            either: parking area, bus_stop, Husky_village
        
    """

    def __init__(self, type = 'Student', infection_probability = 0.0, is_infected, cur_loc, schedule):
        self.type = 'Student'
        self.infection_probability = infection_probability
        self.is_infected = is_infected
        
        
        random_num_for_starting_area = np.random.random()
        if (random_num_for_starting_area < PROPORTION_STARTING_AT_PARKING_AREA):
            self.starting_area = ParkingArea
        elif (random_num_for_starting_area 
                >= (PROPORTION_STARTING_AT_PARKING_AREA + PROPORTION_STARTING_AT_HUSKY_VILLAGE)):
            self.starting_area = BusStop
        else: 
            self.starting_area = SchoolHousing
            
        
        self.schedule = Schedule(self.starting_area)
                
        
        self.starting_loc = (-1,-1) #tuple
        

        self.cur_dest = schedule[0].Institution
        self.cur_loc = starting_loc

        self.final_scheduled_dest = schedule[-1].Institution 
    
    
    
    
    def get_cloest_door_of_cur_dest(cur_loc, cur_dest):
        """
        Get the cloest door of the current destination 
        
        
        Calculate based on the current location(cur_loc) and the current destination(cur_dest)
            of the student  
        get the door location (door_locs) of the cur_dest
        then, calculate the distance between cur_loc and the dor_locs
        
        return the location of the cloest door 
        """
        
    