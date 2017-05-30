#==============================================================================
# Student class
#
# Author: Shijie Xiong, modified by Zhiming Zhong
# May 2017
#==============================================================================

import numpy as np
import numpy.random as rand
import math
from schedule import Schedule
import copy


MEAN_INHERENT_INFEC_THRESHOLD = 0.5
#   (see comment for assigned_infec_prob_threshold)

STD_INHERENT_INFEC_THRESHOLD = 0.12
#   (see comment for assigned_infec_prob_threshold)

assigned_infec_prob_threshold = np.random.normal(MEAN_INHERENT_INFEC_THRESHOLD, STD_INHERENT_INFEC_THRESHOLD)
#  (a healthy Student who is on a cell whose surface & aerosol infec prob add up to a
# value >  than this value will become infected. this is a value selected from the
# normal(?) distrib with mean and std dev as specified in the corresponding
# constants in Student class.)

SNEEZE_COUGH_PROB = 0.2
#   (probability a Student sneezes/coughs per min)

SURFACE_PROB = 0.02
#   (probability a Student increases the surface_infec_prob by SURFACE_INFEC_PROB in campus per min)

AEROSOL_INFEC_PROB_INCREMENT = 0.05
#   (The value to increment aerosol_infec_prob in campus by each time a Student does sneeze/cough)

SURFACE_INFEC_PROB_INCREMENT = 0.2
#   (The value to increment aerosol_infec_prob in campus by each time a Student does infect the surface in a cell)

AEROSOL_INFEC_PROB_DECR_PER_MIN = 1.0/180
#  (value to decrement aerosol_infec_prob each min, for each cell)

SURFACE_INFEC_PROB_DECR_PER_MIN = 1.0/300
#  (value to decrement surface_infec_prob each min, for each cell)

#Probability for each kind of moving option.
PROB_STAY_RANDOM = 0.2      # Probability is 0.2. range 0.0 - 0.2
PROB_MOVE_NORTH = 0.4       # Probability is 0.2. range 0.2 - 0.4
PROB_MOVE_SOUTH = 0.6       # Probability is 0.2. range 0.4 - 0.6
PROB_MOVE_WEST = 0.8        # Probability is 0.2. range 0.6 - 0.8
PROB_MOVE_EAST = 1.0        # Probability is 0.2. range 0.8 - 1.0

# Door posns for parking area 1, 2, and bus stop.
POTENTIAL_STARTING_POSNS = [[300, 395], [590, 215] ,[840, 480]]


class Student:

    def __init__(self):

        self.schedule = None     # must be set by driver.

        # an index in the schedule Activity list, initially set to None.
        # will be set to 0 when cur_time == starting_time of very 1st Activity in Schedule.
        self.cur_sched_activity_idx = None

        # (an index in the schedule Activity list)
        self.next_sched_activity_idx = 0

        # : list of 2 ints # (initially [-1,-1])
        self.cur_posn   = [-1, -1]

        self.last_x = 0   # for self-avoiding walk. Used for random walking and moving toward a door.
        self.last_y = 0   # for self-avoiding walk. Used for random walking and moving toward a door.

        self.cur_institution = None  # int   None represents off campus.

        #self.starting_posn = get_starting_posn()
        self.starting_posn = copy.deepcopy(POTENTIAL_STARTING_POSNS[rand.randint(0, len(POTENTIAL_STARTING_POSNS))])  # door of parking area.

        #cur_dest_institution_int = None            # We set this when we have a current Activity.  No need.... just keep cur_dest_posn
        #self.cur_dest_posn = None    #: tuple(int, int)     # Updtae this once an Activity starts.


        # State of the Student
        self.doing_random_walk = False   # Flag for random walking
        self.walking_to_class = False   # Flag for heading to class
        self.sitting_in_class = False   # Flag for sitting in class already
        self.leaving_class = False      # Flag for leaving class
        self.heading_home = False       # Set this to True when Student has completed all scheduled activities.
        self.home_after_completing_schedule = False

        self.is_infected = False
        self.is_contagious = False

        # self.prev_posn = None



    def get_distance(self, x1, y1, x2, y2):
        ''' Calculates and returns the distance between the two given points.'''
        return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))



    def check_schedule(self, cur_time):
        '''Checks self.schedule. Changes the state of the student accordingly.'''


        if self.cur_sched_activity_idx == None \
            and self.cur_posn == [-1, -1]  \
            and self.schedule.activities[self.next_sched_activity_idx].start_time > cur_time:
            pass


        elif self.cur_sched_activity_idx == None \
                and self.next_sched_activity_idx >= len(self.schedule.activities) \
                and not self.home_after_completing_schedule:
            # Completed Schedule, but is not home yet.
            self.heading_home = True
            self.doing_random_walk = False

        elif self.cur_sched_activity_idx != None:
            # In the middle of an Activity.

            self.doing_random_walk = False
            if self.schedule.activities[self.cur_sched_activity_idx].end_time <= cur_time:
                self.leaving_class = True

        else:
            # Student is between activities. (cur_sched_activity_idx == None)

            if self.schedule.activities[self.next_sched_activity_idx].start_time <= cur_time:
                # It's time to start next activity.

                if self.next_sched_activity_idx == 0:
                    self.cur_posn = copy.deepcopy(self.starting_posn)
                    self.cur_posn[0] += 1

                self.doing_random_walk = False
                self.walking_to_class = True
                self.cur_sched_activity_idx = copy.deepcopy(self.next_sched_activity_idx)
                self.next_sched_activity_idx += 1


            else:
                self.doing_random_walk = True




    def move(self, grid, cur_time, INSTITUTION_INT_MAP):
        '''   '''

        #REMOVE:
        print("CUR TIME IN MOVE:   "  + str(cur_time))

        if self.home_after_completing_schedule:
            # Do not need to call update_infec_status_and_cell_infec_probs()
            return grid

        self.check_schedule(cur_time)       # Call the function to check schedule and change state



        if self.cur_posn == [-1, -1] and self.cur_sched_activity_idx == None:
            self.update_infec_status_and_cell_infec_probs(grid)
            return grid


        elif self.heading_home:
            self.head_home(grid)
            self.update_infec_status_and_cell_infec_probs(grid)
            return grid

        elif self.sitting_in_class and not self.leaving_class:
            self.update_infec_status_and_cell_infec_probs(grid)
            return grid

        elif self.doing_random_walk:
            # Random walk outdoors, taking one step. Update and return grid.
            self.random_walk_one_step(grid)
            self.update_infec_status_and_cell_infec_probs(grid)
            return grid


        # Access the door list through the int map by the index given by the schedule


        door_posns = INSTITUTION_INT_MAP[
            self.schedule.activities[self.cur_sched_activity_idx].dest_institution_int].door_posns


        door_posns_array_of_tuples = np.array(door_posns)
        door_list_x = door_posns_array_of_tuples[:, 0]  # get the list of all the 1st elements of each tuple in door_posns_array_of_tuples.
        door_list_y = door_posns_array_of_tuples[:, 1]  # get the list of all the 2nd elements of each tuple in door_posns_array_of_tuples.
        closest_door_x, closest_door_y = self.get_closest_door_posn(door_list_x, door_list_y)

        # Access the seat given through the schedule
        seat_given_x = self.schedule.activities[self.cur_sched_activity_idx].seat_posn[0]
        seat_given_y = self.schedule.activities[self.cur_sched_activity_idx].seat_posn[1]


        if self.leaving_class:
            self.leave_class(grid, closest_door_x, closest_door_y, seat_given_x, seat_given_y)


        else:
            # At this point, we know self.walking_to_class is True.
            # Student is currently in the middle of an Activity, not sitting in class yet.
            # Student is outdoors. May be directly adjacent to
            # a door of its cur destination institution. If so, move directly to seat.
            # If not, move toward closest door of cur destination institution
            # Update grid.

            # Check if student is adjacent to a door of the current destination institution,
            # if so, move Student into the seat directly
            if (closest_door_x == self.cur_posn[0] + 1 and closest_door_y == self.cur_posn[1]) \
                    or (closest_door_x == self.cur_posn[0] - 1 and closest_door_y == self.cur_posn[1]) \
                    or (closest_door_x == self.cur_posn[0] and closest_door_y == self.cur_posn[1] + 1) \
                    or (closest_door_x == self.cur_posn[0] and closest_door_y == self.cur_posn[1] - 1):
                self.move_directly_to_seat(grid, seat_given_x, seat_given_y)


            # At this point, we know the Student is outdoors, walking to class, and is not adjacent to a door of the
            # current destination instit.
            # Move one cell toward closest door of cur destination institution
            else:
                self.move_one_cell_toward_door(grid, closest_door_x, closest_door_y)


        self.update_infec_status_and_cell_infec_probs(grid)

        return grid



    def leave_class(self, grid, door_x, door_y, seat_given_x, seat_given_y):
        '''Leave classroom, moving to a outdoor grid cell adjacent to the given door of the current institution.
        Update grid. Increment self.cur_sched_activity_idx'''


        # Four if statements to check which direction is outdoors
        # I assume the outdoor path's type is 0
        # If it's outdoor, assign the student to the correct position.
        if grid[door_x - 1, door_y, 0] == 0:         # West.
            if self.is_infected is True:
                grid[seat_given_x, seat_given_y, 2] -= 1
                grid[door_x - 1, door_y, 2] += 1
                self.cur_posn[0] = door_x - 1
                self.cur_posn[1] = door_y
            else:
                grid[seat_given_x, seat_given_y, 1] -= 1
                grid[door_x - 1, door_y, 1] += 1
                self.cur_posn[0] = door_x - 1
                self.cur_posn[1] = door_y
        elif grid[door_x + 1, door_y, 0] == 0:
            if self.is_infected is True:
                grid[seat_given_x, seat_given_y, 2] -= 1
                grid[door_x + 1, door_y, 2] += 1
                self.cur_posn[0] = door_x + 1
                self.cur_posn[1] = door_y
            else:
                grid[seat_given_x, seat_given_y, 1] -= 1
                grid[door_x + 1, door_y, 1] += 1
                self.cur_posn[0] = door_x + 1
                self.cur_posn[1] = door_y
        elif grid[door_x, door_y - 1, 0] == 0:
            if self.is_infected is True:
                grid[seat_given_x, seat_given_y, 2] -= 1
                grid[door_x, door_y - 1, 2] += 1
                self.cur_posn[0] = door_x
                self.cur_posn[1] = door_y - 1
            else:
                grid[seat_given_x, seat_given_y, 1] -= 1
                grid[door_x, door_y - 1, 1] += 1
                self.cur_posn[0] = door_x
                self.cur_posn[1] = door_y - 1
        elif grid[door_x, door_y + 1, 0] == 0:
            if self.is_infected is True:
                grid[seat_given_x, seat_given_y, 2] -= 1
                grid[door_x, door_y + 1, 2] += 1
                self.cur_posn[0] = door_x
                self.cur_posn[1] = door_y + 1
            else:
                grid[seat_given_x, seat_given_y, 1] -= 1
                grid[door_x, door_y + 1, 1] += 1
                self.cur_posn[0] = door_x
                self.cur_posn[1] = door_y + 1

        self.cur_sched_activity_idx = None

        self.leaving_class = False
        self.doing_random_walk = True
        self.sitting_in_class = False
        self.walking_to_class = False



    def move_directly_to_seat(self, grid, seat_given_x, seat_given_y):
        '''Moves Student directly to seat_posn of current Activity. Updates Student's 
        state (sitting in class / walking to class) accordingly.'''

        if self.is_infected is True:
            grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
            grid[seat_given_x, seat_given_y, 2] += 1
        else:
            grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
            grid[seat_given_x, seat_given_y, 1] += 1

        self.cur_posn[0] = seat_given_x
        self.cur_posn[1] = seat_given_y
        self.walking_to_class = False
        self.sitting_in_class = True





    def random_walk_one_step(self, grid):
        '''Take one step in a random direction, outdoors (or remain in same position). Update grid.'''

        a_rand = rand.random()
        if a_rand < PROB_STAY_RANDOM:
            return

        addends = [[1, 0], [0, 1], [-1, 0], [0, -1]]

        while True:
            temp_cur_posn = self.cur_posn
            rand.shuffle(addends)
            if self.last_x == 0 and self.last_y != 0:
                if addends[0][0] == 0 and addends[0][1] == -self.last_y:
                    continue
                else:
                    temp_cur_posn[0] += addends[0][0]
                    temp_cur_posn[1] += addends[0][1]
                    if grid[temp_cur_posn[0], temp_cur_posn[1], 0] == 0:
                        if self.is_infected is True:
                            grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                            grid[temp_cur_posn[0], temp_cur_posn[1], 2] += 1
                        else:
                            grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                            grid[temp_cur_posn[0], temp_cur_posn[1], 1] += 1

                        self.cur_posn[0] = temp_cur_posn[0]
                        self.cur_posn[1] = temp_cur_posn[1]
                        self.last_x = addends[0][0]
                        self.last_y = addends[0][1]
                        print("In random_walk(), new position:   " + str(temp_cur_posn))       #REMOVE
                        return grid
                    else:
                        continue
            elif self.last_x != 0 and self.last_y == 0:
                if addends[0][0] == -self.last_x and addends[0][1] == 0:
                    continue
                else:
                    temp_cur_posn[0] += addends[0][0]
                    temp_cur_posn[1] += addends[0][1]
                    if grid[temp_cur_posn[0], temp_cur_posn[1], 0] == 0:
                        if self.is_infected is True:
                            grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                            grid[temp_cur_posn[0], temp_cur_posn[1], 2] += 1
                        else:
                            grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                            grid[temp_cur_posn[0], temp_cur_posn[1], 1] += 1

                        self.cur_posn[0] = temp_cur_posn[0]
                        self.cur_posn[1] = temp_cur_posn[1]
                        self.last_x = addends[0][0]
                        self.last_y = addends[0][1]
                        print("In random_walk(), new position:   " + str(temp_cur_posn))  # REMOVE
                        return grid
                    else:
                        continue
            else:
                temp_cur_posn[0] += addends[0][0]
                temp_cur_posn[1] += addends[0][1]
                if grid[temp_cur_posn[0], temp_cur_posn[1], 0] == 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        grid[temp_cur_posn[0], temp_cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        grid[temp_cur_posn[0], temp_cur_posn[1], 1] += 1

                    self.cur_posn[0] = temp_cur_posn[0]
                    self.cur_posn[1] = temp_cur_posn[1]
                    self.last_x = addends[0][0]
                    self.last_y = addends[0][1]
                    print("In random_walk(), new position:   " + str(temp_cur_posn))  # REMOVE
                    return grid
                else:
                    continue




    # def random_walk_one_step(self, grid):
    #     '''Take one step in a random direction, outdoors (or remain in same position). Update grid.'''
    #
    #     a_rand = rand.random()
    #     if a_rand < PROB_STAY_RANDOM:
    #         return
    #
    #     addends = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    #
    #
    #     rand.shuffle(addends)
    #
    #     temp_cur_posn = self.cur_posn
    #
    #
    #     for i in range(len(addends)):
    #         temp_cur_posn[0] += addends[i][0]
    #         temp_cur_posn[1] += addends[i][1]
    #
    #         if grid[temp_cur_posn[0], temp_cur_posn[1], 0] == 0:
    #             if self.is_infected is True:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
    #                 grid[temp_cur_posn[0], temp_cur_posn[1], 2] += 1
    #             else:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
    #                 grid[temp_cur_posn[0], temp_cur_posn[1], 1] += 1
    #
    #             self.cur_posn[0] = temp_cur_posn[0]
    #             self.cur_posn[1] = temp_cur_posn[1]
    #
    #             #print("Random walk one step, cur_posn: " + str(self.cur_posn))
    #
    #             return
    #
    #
    #     '''
    #     #Joey's orig version of random_walk_one_step:
    #
    #         if a_rand < PROB_MOVE_NORTH:
    #             if self.is_infected is True:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
    #                 grid[self.cur_posn[0], self.cur_posn[1] + 1, 2] += 1
    #                 self.cur_posn[1] += 1
    #             else:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
    #                 grid[self.cur_posn[0], self.cur_posn[1] + 1, 1] += 1
    #                 self.cur_posn[1] += 1
    #         elif a_rand < PROB_MOVE_SOUTH:
    #             if self.is_infected is True:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
    #                 grid[self.cur_posn[0], self.cur_posn[1] - 1, 2] += 1
    #                 self.cur_posn[1] -= 1
    #             else:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
    #                 grid[self.cur_posn[0], self.cur_posn[1] - 1, 1] += 1
    #                 self.cur_posn[1] -= 1
    #         elif a_rand < PROB_MOVE_WEST:
    #             if self.is_infected is True:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
    #                 grid[self.cur_posn[0] - 1, self.cur_posn[1], 2] += 1
    #                 self.cur_posn[0] -= 1
    #             else:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
    #                 grid[self.cur_posn[0] - 1, self.cur_posn[1], 1] += 1
    #                 self.cur_posn[0] -= 1
    #         else:
    #             if self.is_infected is True:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
    #                 grid[self.cur_posn[0] + 1, self.cur_posn[1], 2] += 1
    #                 self.cur_posn[0] += 1
    #             else:
    #                 grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
    #                 grid[self.cur_posn[0] + 1, self.cur_posn[1], 1] += 1
    #                 self.cur_posn[0] += 1
    #     '''


    def get_closest_door_posn(self, door_list_x, door_list_y):
        '''Returns a tuple of ints representing the x y position of the door closest to self.cur_posn.'''

        idx_of_closest_door_in_door_list_x = 0
        dis = self.get_distance(self.cur_posn[0], self.cur_posn[1], door_list_x[0], door_list_y[0])
        for indexD in range(1, len(door_list_x)):
            dis_2 = self.get_distance(self.cur_posn[0], self.cur_posn[1], door_list_x[indexD], door_list_y[indexD])
            if dis_2 < dis:
                idx_of_closest_door_in_door_list_x = indexD
                dis = dis_2

        # Get the door position
        door_x = door_list_x[idx_of_closest_door_in_door_list_x]
        door_y = door_list_y[idx_of_closest_door_in_door_list_x]

        return (door_x, door_y)




    def move_one_cell_toward_door(self, grid, door_x, door_y):

        # "north_move" is the distance to closest door of destination instit after moving 1 cell north.
        north_move = self.get_distance(self.cur_posn[0], self.cur_posn[1] - 1, door_x, door_y)
        south_move = self.get_distance(self.cur_posn[0], self.cur_posn[1] + 1, door_x, door_y)
        west_move = self.get_distance(self.cur_posn[0] - 1, self.cur_posn[1], door_x, door_y)
        east_move = self.get_distance(self.cur_posn[0] + 1, self.cur_posn[1], door_x, door_y)


        '''
        if self.last_x == 1 and self.last_y == 0:  # E
            if north_move == min(north_move, south_move, east_move):
                if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 1
                    self.last_y = 0
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = 1
                    return grid
            elif south_move == min(north_move, south_move, east_move):
                if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 1
                    self.last_y = 0
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = -1
                    return grid
            else:  # east_move
                if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                    if north_move == min(north_move, south_move):
                        if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                    else:
                        if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 1
                    self.last_y = 0
                    return grid
        elif self.last_x == -1 and self.last_y == 0:  # W
            if north_move == min(north_move, south_move, west_move):
                if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = -1
                    self.last_y = 0
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = 1
                    return grid
            elif south_move == min(north_move, south_move, west_move):
                if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = -1
                    self.last_y = 0
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = -1
                    return grid
            else:  # West
                if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                    if north_move == min(north_move, south_move):
                        if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                    else:
                        if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = -1
                    self.last_y = 0
                    return grid
        elif self.last_x == 0 and self.last_y == 1:  # N
            if north_move == min(north_move, east_move, west_move):
                if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                    if east_move == min(east_move, west_move):
                        if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                    else:
                        if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                else:  # N
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = 1
                    return grid
            elif east_move == min(north_move, east_move, west_move):
                if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = 1
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 1
                    self.last_y = 0
                    return grid
            else:  # W
                if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = 1
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = -1
                    self.last_y = 0
                    return grid
        elif self.last_x == 0 and self.last_y == -1:  # S
            if south_move == min(south_move, east_move, west_move):
                if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                    if east_move == min(east_move, west_move):
                        if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                    else:
                        if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                else:  # S
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = -1
                    return grid
            elif east_move == min(south_move, east_move, west_move):
                if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = -1
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 1
                    self.last_y = 0
                    return grid
            else:  # W
                if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = -1
                    return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = -1
                    self.last_y = 0
                    return grid
        else:
            if north_move == min(north_move, east_move, west_move):
                if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                    if east_move == min(east_move, west_move):
                        if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                    else:
                        if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                else:  # N
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = 1
                    return grid
            elif south_move == min(north_move, south_move, east_move, west_move):
                if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                    if east_move == min(east_move, west_move):
                        if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                    else:
                        if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 1
                            self.last_y = 0
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[0] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = -1
                            self.last_y = 0
                            return grid
                else:  # S
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 0
                    self.last_y = -1
                    return grid
            elif east_move == min(north_move, south_move, east_move, west_move):
                if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] != 0:
                    if north_move == min(north_move, south_move):
                        if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                    else:
                        if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] += 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = 1
                    self.last_y = 0
                    return grid
            else:
                if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] != 0:
                    if north_move == min(north_move, south_move):
                        if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                    else:
                        if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] != 0:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] += 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = 1
                            return grid
                        else:
                            if self.is_infected is True:
                                grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                            else:
                                grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                                self.cur_posn[1] -= 1
                                grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                            self.last_x = 0
                            self.last_y = -1
                            return grid
                else:
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 2] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        self.cur_posn[0] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1], 1] += 1
                    self.last_x = -1
                    self.last_y = 0
                    return grid
        '''


        if north_move == min(north_move, south_move, west_move, east_move):
            # If cell directly north of cur_posn is a wall, then move either east or west.
            if grid[self.cur_posn[0], self.cur_posn[1] - 1, 0] > 0:
                #if west_move == min(west_move, east_move):

                # Always move west
                if self.is_infected is True:                   # Note: This assumes that if north is a wall, east and west will not be walls.
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                    grid[self.cur_posn[0] - 1, self.cur_posn[1], 2] += 1
                    self.cur_posn[0] -= 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                    grid[self.cur_posn[0] - 1, self.cur_posn[1], 1] += 1
                    self.cur_posn[0] -= 1


                '''
                elif east_move == min(west_move, east_move):
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        grid[self.cur_posn[0] + 1, self.cur_posn[1], 2] += 1
                        self.cur_posn[0] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        grid[self.cur_posn[0] + 1, self.cur_posn[1], 1] += 1
                        self.cur_posn[0] += 1
                '''
            else:                   # cell directly north is not wall. Move north.
                if self.is_infected is True:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1      # decrement num of infected students at current cell
                    grid[self.cur_posn[0], self.cur_posn[1] - 1, 2] += 1  # increment num of infected students at new cell
                    self.cur_posn[1] -= 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1      # decrement num of healthy students at current cell
                    grid[self.cur_posn[0], self.cur_posn[1] - 1, 1] += 1  # increment num of healthy students at new cell
                    self.cur_posn[1] -= 1
        elif south_move == min(north_move, south_move, west_move, east_move):
            # If cell directly south of cur_posn is a wall, then move either east or west.
            if grid[self.cur_posn[0], self.cur_posn[1] + 1, 0] > 0:

                #if west_move == min(west_move, east_move):

                # Always move west
                if self.is_infected is True:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                    grid[self.cur_posn[0] - 1, self.cur_posn[1], 2] += 1
                    self.cur_posn[0] -= 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                    grid[self.cur_posn[0] - 1, self.cur_posn[1], 1] += 1
                    self.cur_posn[0] -= 1
                '''
                elif east_move == min(west_move, east_move):
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        grid[self.cur_posn[0] + 1, self.cur_posn[1], 2] += 1
                        self.cur_posn[0] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        grid[self.cur_posn[0] + 1, self.cur_posn[1], 1] += 1
                        self.cur_posn[0] += 1
                '''
            else:
                if self.is_infected is True:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                    grid[self.cur_posn[0], self.cur_posn[1] + 1, 2] += 1
                    self.cur_posn[1] += 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                    grid[self.cur_posn[0], self.cur_posn[1] + 1, 1] += 1
                    self.cur_posn[1] += 1
        elif west_move == min(north_move, south_move, west_move, east_move):
            if grid[self.cur_posn[0] - 1, self.cur_posn[1], 0] > 0:
                #if north_move == min(north_move, south_move):

                # Always move north
                if self.is_infected is True:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                    grid[self.cur_posn[0], self.cur_posn[1] - 1, 2] += 1
                    self.cur_posn[1] -= 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                    grid[self.cur_posn[0], self.cur_posn[1] - 1, 1] += 1
                    self.cur_posn[1] -= 1

                '''
                elif south_move == min(north_move, south_move):
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1] + 1, 2] += 1
                        self.cur_posn[1] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1] + 1, 1] += 1
                        self.cur_posn[1] += 1
                '''

            else:
                if self.is_infected is True:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                    grid[self.cur_posn[0] - 1, self.cur_posn[1], 2] += 1
                    self.cur_posn[0] -= 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                    grid[self.cur_posn[0] - 1, self.cur_posn[1], 1] += 1
                    self.cur_posn[0] -= 1
        elif east_move == min(north_move, south_move, west_move, east_move):
            if grid[self.cur_posn[0] + 1, self.cur_posn[1], 0] > 0:


                #if north_move == min(north_move, south_move):

                # Always move north
                if self.is_infected is True:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                    grid[self.cur_posn[0], self.cur_posn[1] - 1, 2] += 1
                    self.cur_posn[1] -= 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                    grid[self.cur_posn[0], self.cur_posn[1] - 1, 1] += 1
                    self.cur_posn[1] -= 1

                '''
                elif south_move == min(north_move, south_move):
                    if self.is_infected is True:
                        grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1] + 1, 2] += 1
                        self.cur_posn[1] += 1
                    else:
                        grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                        grid[self.cur_posn[0], self.cur_posn[1] + 1, 1] += 1
                        self.cur_posn[1] += 1
                '''
            else:
                if self.is_infected is True:
                    grid[self.cur_posn[0], self.cur_posn[1], 2] -= 1
                    grid[self.cur_posn[0] + 1, self.cur_posn[1], 2] += 1
                    self.cur_posn[0] += 1
                else:
                    grid[self.cur_posn[0], self.cur_posn[1], 1] -= 1
                    grid[self.cur_posn[0] + 1, self.cur_posn[1], 1] += 1
                    self.cur_posn[0] += 1


    def head_home(self, grid):
        '''Move one cell toward starting_posn.'''

        if (self.starting_posn[0] == self.cur_posn[0] + 1 and self.starting_posn[1] == self.cur_posn[1]) \
                or (self.starting_posn[0] == self.cur_posn[0] - 1 and self.starting_posn[1] == self.cur_posn[1]) \
                or (self.starting_posn[0] == self.cur_posn[0] and self.starting_posn[1] == self.cur_posn[1] + 1) \
                or (self.starting_posn[0] == self.cur_posn[0] and self.starting_posn[1] == self.cur_posn[1] - 1):
            self.cur_posn = self.starting_posn
            self.home_after_completing_schedule = True

        else:
            self.move_one_cell_toward_door(grid, self.starting_posn[0], self.starting_posn[1])




    def update_infec_status_and_cell_infec_probs(self, grid):
        '''May set Student's infection status is_infected to True if it is False, by evaluating grid cell's surface and 
        aerosol infection probabilities. 
        May increase grid cell's infection probabilities (to simulate a sneeze/cough/deposition of virus on surface). '''
       
        myX = self.cur_posn[0]
        myY = self.cur_posn[1]
        total_prob = grid[myX, myY, 3] + grid[myX, myY, 4] #sum of total infectivity
        print("total_prob = grid[myX, myY, 3] + grid[myX, myY, 4]: " + str(total_prob))             #REMOVE
        total_prob = np.minimum(total_prob, 1) #probability cannot exceed 1
        print("total_prob = np.maximum(total_prob, 1): " + str(total_prob))                         #REMOVE
        if np.random.rand() < total_prob: #Does student get infected?
            self.is_infected = True
            print("Student got infected. : " + str(total_prob))  # REMOVE
        else:
            print("Student NOT infected. : " + str(total_prob))  # REMOVE
            
        if (self.is_contagious): #If contagious go through probabilities of incrementing contagion
            if np.random.rand() < SNEEZE_COUGH_PROB:
                grid[myX, myY, 3] += SURFACE_INFEC_PROB_INCREMENT
                
            if np.random.rand() < SURFACE_PROB:
                grid[myX, myY, 4] += SURFACE_INFEC_PROB_INCREMENT

        # TODO: IMPLEMENT THIS METHOD
        # Update is_infected
        # Possibly cough / sneeze
        # Update the cur_posn grid cell's infec probabilities accordingly.


