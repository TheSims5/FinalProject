# ==============================================================================
# Student class
#
# Author: Hoi Yan Wu
# May 2017
# ==============================================================================


# ==============================================================================
# ==============================================================================

import numpy as np
import random
import math
from schedule_list import ScheduleList
from parking_area import ParkingArea
from bus_stop import BusStop
from student_housing import StudentHousing
from virus import Virus


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
            either building, bus_stop, ParkingArea, SchoolHousing, OffCampus
                                      
        final_scheduled_dest: Institution
            the final destination of the student when they finished their schedule 
            either: parking area, bus_stop, Husky_village
            
        final_scheduled_loc: tuple
            the final location of the student 
        
    """
    def __init__(self):
        
        MEAN_STUD_INFEC_PROB = 0.5
        STD_STUD_INFEC_PROB = 0.1
    
    
    
    
        PROPORTION_STARTING_AT_PARKING = 0.4
        PROPORTION_STARTING_AT_HOUSING = 0.2
        PROPORTION_STARTING_AT_BUS = 0.4
        STARTING_POSITION_ARRAY = np.array([PROPORTION_STARTING_AT_PARKING,PROPORTION_STARTING_AT_HOUSING,PROPORTION_STARTING_AT_BUS])


#                Parking Area         Student Housing           Bus Stop                  
#Proportion 0.0_________________0.xx____________________0.xx_________________1.0


        PRE_MAJOR_PROG_PROPORTION = 0.31
        BUSINESS_PROPORTION = 0.17
        STEM_PROPORTION = 0.21
        NURSING_AND_HEALTH_PROPORTION = 0.08
        INTER_ART_AND_SCIENCE_PROPORTION = 0.17
        EDUCATIONAL_PROPORTION = 0.04
        INTERACTIVE_MEDIA_PROPORTION = 0.01
        
        COMMUNITY_PROPORTION_MAP = { 1:0.31, 2:0.17, 3:0.21, 4:0.08, 5:0.17, 6:0.04, 7:0.01}
        COMMUNITY_PROPORTION_ARRAY = np.array([PRE_MAJOR_PROG_PROPORTION, 
                                                BUSINESS_PROPORTION , 
                                                STEM_PROPORTION, 
                                                NURSING_AND_HEALTH_PROPORTION, 
                                                INTER_ART_AND_SCIENCE_PROPORTION, 
                                                EDUCATIONAL_PROPORTION, 
                                                INTERACTIVE_MEDIA_PROPORTION])
    

        COMMUNITY_INT_MAP = { 1:"PRE_MAJOR_PROG", 
                        2:"BUSINESS",
                        3:"STEM",
                        4:"NURSING_AND_HEALTH",
                        5:"INTER_ART_AND_SCIENCE",
                        6:"EDUCATIONAL",
                        7:"INTERACTIVE_MEDIA"}
        
        

        random_num_for_community = np.random.random()
        temp_community_proportion = np.cumsum(COMMUNITY_PROPORTION_ARRAY)
        
        if (random_num_for_community<temp_community_proportion[0]):
            self.community = 1
        elif ( random_num_for_community>=temp_community_proportion[0] 
            and random_num_for_community<temp_community_proportion[1] ):
            self.community = 2
        elif ( random_num_for_community>=temp_community_proportion[1] 
            and random_num_for_community<temp_community_proportion[2] ):
            self.community = 3
        elif ( random_num_for_community>=temp_community_proportion[2] 
            and random_num_for_community<temp_community_proportion[3] ):
            self.community = 4
        elif ( random_num_for_community>=temp_community_proportion[3] 
            and random_num_for_community<temp_community_proportion[4] ):
            self.community = 5
        elif ( random_num_for_community>=temp_community_proportion[4] 
            and random_num_for_community<temp_community_proportion[5] ):
            self.community = 6
        else:
            self.community = 7
            
        self.schedule_list = ScheduleList(self.community)

        self.next_sched_item = 0
        
        self.cur_posn = (-1,-1)
        

        random_num_for_starting_area = np.random.random()
        if (random_num_for_starting_area < STARTING_POSITION_ARRAY[0]):
            self.starting_institution = 11
            #ParkingArea
            
        elif (random_num_for_starting_area >= STARTING_POSITION_ARRAY[0]
            and random_num_for_starting_area < STARTING_POSITION_ARRAY[1]):
            self.starting_institution = 10
            #StudentHousing
            
        else:
            self.starting_institution = 9
            #BusStop
        self.cur_institution = self.starting_institution


        print("starting_insti: " + str(self.starting_institution))

        self.cur_dest_institution = self.schedule_list.schedules[0][0].dest_institution_int
        self.cur_dest_posn = (-1,-1)
        
        
        self.time_spent_in_cur_institution = 0
        
        
        # self.infection_probability = infection_probability
        self.assigned_infec_prob = np.random.normal(MEAN_STUD_INFEC_PROB, STD_STUD_INFEC_PROB)
        self.virus = None                        
        self.final_infec_prob = self.assigned_infec_prob                                                



    def get_closest_door_of_cur_dest(self, institution_int_map):
        """
        Get the cloest door of the current destination 

        Calculate based on the current location(cur_loc) and the current destination(cur_dest)
            of the student  
        get the door location (door_locs) of the cur_dest
        then, calculate the distance between cur_loc and the dor_locs

        return the location of the cloest door (tuple) 
        """

        cur_x = self.cur_posn[0]
        cur_y = self.cur_posn[1]
        
        # institution_int_map[self.cur_dest_institution]: the corresponding institution object will be returned 
        doors = institution_int_map[self.cur_dest_institution].door_posns
        dist_from_door = []
        
        for door in doors:
            door_x = door[0]
            door_y = door[1]
            distance = ((cur_x-door_x)**2 + (cur_y-door_y)**2)**0.5
            dist_from_door.append(distance)
        
        min_distance = min(dist_from_door)
        index_of_door = dist_from_door.index(min_distance)
        self.cur_dest_posn = doors[index_of_door]
        # return cur_dest_posn
        
                    
    def calc_final_infec_prob(self, num_infected, num_total, institution_int_map):
        """ 
        calculate final_infec_probab 
        if final_infec_probab >= np.random.random():
            self.virus = Virus()
        """
        self.final_infec_prob = (num_infected/num_total)\
                                * self.time_spent_in_cur_institution \
                                * institution_int_map[self.cur_institution].infec_prob \
                                * Virus.DEFAULT_PROB \
                                * self.assigned_infec_prob
        # final_infec_prob = 
    
    def move(self, grid, institution_int_map, day, time, dt, x_max, y_max):


        #REMOVE
        print("student cur pos: " + str(self.cur_posn))
        
        # increment the time_spent_in_cur_institution
        self.time_spent_in_cur_institution = self.time_spent_in_cur_institution + dt
        
        
        # see whether this student is infected
        if self.virus == None:
            is_infected = False
        else:
            is_infected = True
            
        # make moved_Completed to False
        moved_Complete = False
        
        # !!!!!!! student at CampusOutdoors is not counted !!!!!!
        # check the cur_end_time for the current schedule item
        # if the activity is not end 
        # the student do not need to move
        cur_end_time = self.schedule_list.schedules[day-1][self.next_sched_item].start_time
        
        # if the student is arrived:
        if self.cur_posn == (-1, -1):
            self.get_closest_door_of_cur_dest(institution_int_map)
            self.cur_posn = self.cur_dest_posn
            moved_Complete = True
            if is_infected:
                grid[self.cur_posn[0], self.cur_posn[1], 1] = grid[self.cur_posn[0], self.cur_posn[0], 1] + 1
            else:
                grid[self.cur_posn[0], self.cur_posn[1], 2] = grid[self.cur_posn[0], self.cur_posn[0], 2] + 1
        elif time < cur_end_time:
            if self.cur_institution == self.schedule_list.schedules[day-1][self.next_sched_item-1].dest_institution_int:
                moved_Complete = True


        if not moved_Complete:
        
            
            # Assume: day starts at 1
            # then see how many activity a student has in that day
            len_of_schedule_of_the_day = len(self.schedule_list.schedules[day-1])
    
    
            # next_dest_institution = self.schedule_list.schedules[day-1][next_sched_item]
            # set the cur_dest_institution
            # the student reach the last activity item
            if self.next_sched_item < len_of_schedule_of_the_day:
                self.cur_dest_institution = self.schedule_list.schedules[day-1][self.next_sched_item].dest_institution_int
            else:
                self.cur_dest_institution = self.schedule_list.schedules[day-1][-1].dest_institution_int
            
                                                                
            # will update the self.cur_dest_posn                                                                                                                           
            self.get_closest_door_of_cur_dest(institution_int_map)
    
    
            temp_posn_N = []
            temp_posn_E = []
            temp_posn_S = []
            temp_posn_W = []


            temp_posn_N.append(self.cur_posn[0])
            temp_posn_N.append(self.cur_posn[1] - 1)

            temp_posn_E.append(self.cur_posn[0] + 1)
            temp_posn_E.append(self.cur_posn[1])

            temp_posn_S.append(self.cur_posn[0])
            temp_posn_S.append(self.cur_posn[1] + 1)

            temp_posn_W.append(self.cur_posn[0] - 1)
            temp_posn_W.append(self.cur_posn[1])

            available_temp_posns = []
            for temp_posn in [temp_posn_N, temp_posn_E, temp_posn_S, temp_posn_W]:
                if temp_posn[0] >0 and temp_posn[0]<x_max:
                    if temp_posn[1]>0 and temp_posn[1]<y_max:
                        if grid[temp_posn[0], temp_posn[1], 0] == 0:
                            available_temp_posns.append(temp_posn)

            for posn in available_temp_posns:
                if posn[0] == self.cur_dest_posn[0] and posn[1] == self.cur_dest_posn[1]:
                    moved_Complete = move_to_cur_dest(self, grid, is_infected, moved_Complete)
                    if moved_Complete: break


                              
            if not moved_Complete:

                temp_distance = []
                for i in range(len(available_temp_posns)):
                    # if available_dimensions[i]!=-1:
                    temp_distance.append(self.calculate_temp_distance(available_temp_posns[i]))
                    # else:
                    #     temp_distance[i] = -1





                min_distance = min(temp_distance)

                indexes_of_posns_min_dist_away = []


                for i in range(len(temp_distance)):
                    if np.isclose(temp_distance[i], min_distance, rtol=1e-05, atol=1e-08, equal_nan=False):
                        indexes_of_posns_min_dist_away.append(i)


                np.random.shuffle(indexes_of_posns_min_dist_away)

                next_step = indexes_of_posns_min_dist_away[0]
                
                final_next_posn = available_temp_posns[next_step]

                # cur_institution, next_sched_item : no need to change
                self.cur_institution = self.cur_institution
                self.next_sched_item = self.next_sched_item

                if is_infected:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] = grid[self.cur_posn[0], self.cur_posn[1], 2] - 1
                    grid[final_next_posn[0], final_next_posn[1], 2] = grid[final_next_posn[1], final_next_posn[1], 2] + 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] = grid[self.cur_posn[0], self.cur_posn[1], 1] - 1
                    grid[final_next_posn[0], final_next_posn[1], 1] = grid[final_next_posn[1], final_next_posn[1], 1] + 1
                self.cur_posn = tuple(final_next_posn)

        return grid


    def move_to_cur_dest(self, grid, is_infected):
        moved_Complete = True
        self.cur_posn = self.cur_dest_posn
        self.cur_institution = self.cur_dest_institution
        self.next_sched_item = self.next_sched_item + 1
        self.time_spent_in_cur_institution = 0

        if is_infected:
            grid[self.cur_posn[0], self.cur_posn[1], 2] = grid[self.cur_posn[0], self.cur_posn[0], 2] - 1
            grid[self.cur_dest_posn[0], self.cur_dest_posn[1], 2] = grid[self.cur_dest_posn[1], self.cur_dest_posn[
                0], 2] + 1
        else:
            grid[self.cur_posn[0], self.cur_posn[1], 1] = grid[self.cur_posn[0], self.cur_posn[0], 1] - 1
            grid[self.cur_dest_posn[0], self.cur_dest_posn[1], 1] = grid[self.cur_dest_posn[1], self.cur_dest_posn[
                0], 1] + 1

        return moved_Complete


    def calculate_temp_distance(self, loc):
        cur_x = self.cur_posn[0]
        cur_y = self.cur_posn[1]
        distance = ((cur_x-loc[0])**2 + (cur_y-loc[1])**2)**0.5
        return distance
