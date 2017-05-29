
import numpy.random as rand
import math


class Student:
    def __init__(self, x, y, schedule):
        self.x = x
        self.y = y
        self.schedule = schedule
        '''State of the student'''
        self.start_random_walk = True   # Flag for random walking
        self.go_class = False           # Flag for heading to class
        self.take_seats = False         # Flag for sitting in class already
        self.leave_class = False        # Flag for leaving class

        self.infected = False           # Flag of if infected

        '''Possibility for each kind of moving option'''
        self.stayRandom = 0.2
        self.move_north = 0.4
        self.move_south = 0.6
        self.move_west = 0.8
        self.move_east = 1.0

        self.cur_sched_activity_idx = 0 # Current scheduled activity index
        return

    ''' Function to calculate the distance of two point'''
    def two_point(self, x1, y1, x2, y2):
        return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

    ''' Function to check the schedule of the student itself and change the state of the student based on schedule'''
    def check_schedule(self, current_time):
        # If current time is lower than start time, random walking, and reset the take_seats flag
        if current_time < self.schedule[self.cur_sched_activity_idx].start_time:
            self.start_random_walk = True
            self.take_seats = False
        # If current time is between ending time and starting time, go to class, and set the random walk false
        elif self.schedule[self.cur_sched_activity_idx].start_time <= current_time <\
                self.schedule[self.cur_sched_activity_idx].end_time:
            self.start_random_walk = False
            self.go_class = True
        # If current time is bigger than end time, set the flag of leaving to true
        elif current_time == self.schedule[self.cur_sched_activity_idx].end_time:
            self.go_class = False
            self.leave_class = True

    def move(self, grid, current_time, door_list_x, door_list_y,INSTITUTION_INT_MAP):
        """Temporarily set the wall's type to 5, so if the front direction is wall, student will not keep moving"""
        self.check_schedule(current_time)       # Call the function to check schedule and change state

        # Access the door list through the int map by the index given by the schedule
        door_list_x = INSTITUTION_INT_MAP[self.schedule[self.cur_sched_activity_idx].dest_institution_int].door_list_x
        door_list_y = INSTITUTION_INT_MAP[self.schedule[self.cur_sched_activity_idx].dest_institution_int].door_list_y

        # Access the seat given through the schedule
        seat_given_x = self.schedule[self.cur_sched_activity_idx].seat_posn[0]
        seat_given_y = self.schedule[self.cur_sched_activity_idx].seat_posn[1]

        # Function for leaving classroom
        if self.leave_class is True:
            # Figure out the closest door
            closest = 0
            dis = self.two_point(self.x, self.y, door_list_x[0], door_list_y[0])
            for indexD in range(1, len(door_list_x)):
                dis_2 = self.two_point(self.x, self.y, door_list_x[indexD], door_list_y[indexD])
                if dis_2 < dis:
                    closest = indexD
                    dis = dis_2
            # Get the door position
            door_x = door_list_x[closest]
            door_y = door_list_y[closest]

            # Four if statements to check which direction is outdoors
            # I assume the outdoor path's type is 0
            # If it's outdoor, assign the student to the correct position.
            if grid[door_x - 1, door_y, 0] == 0:
                if self.infected is True:
                    grid[seat_given_x, seat_given_y, 2] -= 1
                    grid[door_x - 1, door_y, 2] += 1
                    self.x = door_x - 1
                    self.y = door_y
                else:
                    grid[seat_given_x, seat_given_y, 1] -= 1
                    grid[door_x - 1, door_y, 1] += 1
                    self.x = door_x - 1
                    self.y = door_y
            elif grid[door_x + 1, door_y, 0] == 0:
                if self.infected is True:
                    grid[seat_given_x, seat_given_y, 2] -= 1
                    grid[door_x + 1, door_y, 2] += 1
                    self.x = door_x + 1
                    self.y = door_y
                else:
                    grid[seat_given_x, seat_given_y, 1] -= 1
                    grid[door_x + 1, door_y, 1] += 1
                    self.x = door_x + 1
                    self.y = door_y
            elif grid[door_x, door_y - 1, 0] == 0:
                if self.infected is True:
                    grid[seat_given_x, seat_given_y, 2] -= 1
                    grid[door_x, door_y - 1, 2] += 1
                    self.x = door_x
                    self.y = door_y - 1
                else:
                    grid[seat_given_x, seat_given_y, 1] -= 1
                    grid[door_x, door_y - 1, 1] += 1
                    self.x = door_x
                    self.y = door_y - 1
            elif grid[door_x, door_y + 1, 0] == 0:
                if self.infected is True:
                    grid[seat_given_x, seat_given_y, 2] -= 1
                    grid[door_x, door_y + 1, 2] += 1
                    self.x = door_x
                    self.y = door_y + 1
                else:
                    grid[seat_given_x, seat_given_y, 1] -= 1
                    grid[door_x, door_y + 1, 1] += 1
                    self.x = door_x
                    self.y = door_y + 1

            # When finish the leaving classroom, move to next schedule
            self.cur_sched_activity_idx += 1
            return grid

        # If it's time to go to class and not taken seats yet
        if self.go_class is True and self.take_seats is False:
            # The same to check the closest door
            closest = 0
            dis = self.two_point(self.x, self.y, door_list_x[0], door_list_y[0])
            for indexD in range(1, len(door_list_x)):
                dis_2 = self.two_point(self.x, self.y, door_list_x[indexD], door_list_y[indexD])
                if dis_2 < dis:
                    closest = indexD
                    dis = dis_2

            door_x = door_list_x[closest]
            door_y = door_list_y[closest]

            # Check if the door is next to the student, if so, move them into the seat directly
            if (door_x == self.x + 1 and door_y == self.y) or (door_x == self.x - 1 and door_y == self.y) or \
                    (door_x == self.x and door_y == self.y + 1) or (door_x == self.x and door_y == self.y - 1):
                if self.infected is True:
                    grid[self.x, self.y, 2] -= 1
                    grid[seat_given_x, seat_given_y, 2] += 1
                    self.x = seat_given_x
                    self.y = seat_given_y
                    self.take_seats = True
                    self.go_class = False
                    return grid
                else:
                    grid[self.x, self.y, 1] -= 1
                    grid[seat_given_x, seat_given_y, 1] += 1
                    self.x = seat_given_x
                    self.y = seat_given_y
                    self.take_seats = True
                    self.go_class = False
                    return grid

            # If not taken seat yet, move them towards the door
            if self.take_seats is False and self.start_random_walk is False:
                north_move = self.two_point(self.x, self.y + 1, door_x, door_y)
                south_move = self.two_point(self.x, self.y - 1, door_x, door_y)
                west_move = self.two_point(self.x - 1, self.y, door_x, door_y)
                east_move = self.two_point(self.x + 1, self.y, door_x, door_y)
                if north_move == min(north_move, south_move, west_move, east_move):
                    if grid[self.x, self.y + 1, 0] == 5:
                        if west_move == min(west_move, east_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x - 1, self.y, 2] += 1
                                self.x -= 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x - 1, self.y, 1] += 1
                                self.x -= 1
                                return grid
                        elif east_move == min(west_move, east_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x + 1, self.y, 2] += 1
                                self.x += 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x + 1, self.y, 1] += 1
                                self.x += 1
                                return grid
                    else:
                        if self.infected is True:
                            grid[self.x, self.y, 2] -= 1
                            grid[self.x, self.y + 1, 2] += 1
                            self.y += 1
                            return grid
                        else:
                            grid[self.x, self.y, 1] -= 1
                            grid[self.x, self.y + 1, 1] += 1
                            self.y += 1
                            return grid
                elif south_move == min(north_move, south_move, west_move, east_move):
                    if grid[self.x, self.y - 1, 0] == 5:
                        if west_move == min(west_move, east_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x - 1, self.y, 2] += 1
                                self.x -= 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x - 1, self.y, 1] += 1
                                self.x -= 1
                                return grid
                        elif east_move == min(west_move, east_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x + 1, self.y, 2] += 1
                                self.x += 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x + 1, self.y, 1] += 1
                                self.x += 1
                                return grid
                    else:
                        if self.infected is True:
                            grid[self.x, self.y, 2] -= 1
                            grid[self.x, self.y - 1, 2] += 1
                            self.y -= 1
                            return grid
                        else:
                            grid[self.x, self.y, 1] -= 1
                            grid[self.x, self.y - 1, 1] += 1
                            self.y -= 1
                            return grid
                elif west_move == min(north_move, south_move, west_move, east_move):
                    if grid[self.x, self.y + 1, 0] == 5:
                        if north_move == min(north_move, south_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x, self.y + 1, 2] += 1
                                self.y += 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x, self.y + 1, 1] += 1
                                self.y += 1
                                return grid
                        elif south_move == min(north_move, south_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x, self.y - 1, 2] += 1
                                self.y -= 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x, self.y - 1, 1] += 1
                                self.y -= 1
                                return grid
                    else:
                        if self.infected is True:
                            grid[self.x, self.y, 2] -= 1
                            grid[self.x - 1, self.y, 2] += 1
                            self.x -= 1
                            return grid
                        else:
                            grid[self.x, self.y, 1] -= 1
                            grid[self.x - 1, self.y, 1] += 1
                            self.x -= 1
                            return grid
                elif east_move == min(north_move, south_move, west_move, east_move):
                    if grid[self.x, self.y + 1, 0] == 5:
                        if north_move == min(north_move, south_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x, self.y + 1, 2] += 1
                                self.y += 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x, self.y + 1, 1] += 1
                                self.y += 1
                                return grid
                        elif south_move == min(north_move, south_move):
                            if self.infected is True:
                                grid[self.x, self.y, 2] -= 1
                                grid[self.x, self.y - 1, 2] += 1
                                self.y -= 1
                                return grid
                            else:
                                grid[self.x, self.y, 1] -= 1
                                grid[self.x, self.y - 1, 1] += 1
                                self.y -= 1
                                return grid
                    else:
                        if self.infected is True:
                            grid[self.x, self.y, 2] -= 1
                            grid[self.x + 1, self.y, 2] += 1
                            self.x += 1
                            return grid
                        else:
                            grid[self.x, self.y, 1] -= 1
                            grid[self.x + 1, self.y, 1] += 1
                            self.x += 1
                            return grid

        if self.start_random_walk is True:
            a_rand = rand.random()
            if a_rand < self.stayRandom:
                return grid
            elif a_rand < self.move_north:
                if self.infected is True:
                    grid[self.x, self.y, 2] -= 1
                    grid[self.x, self.y + 1, 2] += 1
                    self.y += 1
                    return grid
                else:
                    grid[self.x, self.y, 1] -= 1
                    grid[self.x, self.y + 1, 1] += 1
                    self.y += 1
                    return grid
            elif a_rand < self.move_south:
                if self.infected is True:
                    grid[self.x, self.y, 2] -= 1
                    grid[self.x, self.y - 1, 2] += 1
                    self.y -= 1
                    return grid
                else:
                    grid[self.x, self.y, 1] -= 1
                    grid[self.x, self.y - 1, 1] += 1
                    self.y -= 1
                    return grid
            elif a_rand < self.move_west:
                if self.infected is True:
                    grid[self.x, self.y, 2] -= 1
                    grid[self.x - 1, self.y, 2] += 1
                    self.x -= 1
                    return grid
                else:
                    grid[self.x, self.y, 1] -= 1
                    grid[self.x - 1, self.y, 1] += 1
                    self.x -= 1
                    return grid
            else:
                if self.infected is True:
                    grid[self.x, self.y, 2] -= 1
                    grid[self.x + 1, self.y, 2] += 1
                    self.x += 1
                    return grid
                else:
                    grid[self.x, self.y, 1] -= 1
                    grid[self.x + 1, self.y, 1] += 1
                    self.x += 1
                    return grid
        return grid