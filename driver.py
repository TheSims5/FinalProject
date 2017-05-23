#==============================================================================
# Driver for the uEpidemic simulation.
#
# Authors: Shijie Xiong, Zhiming Zhong
# May 2017
#==============================================================================

import numpy as na
import numpy.random as rand
import matplotlib.pyplot as plt
import math
from building import Building
from bus_stop import BusStop
from parking_area import ParkingArea
from student_housing import StudentHousing
from campus_outdoors import CampusOutdoors

#TODO Uncomment to integrate actual Student class:
# from student import Student


#TODO: REMOVE Student class stub: -------
class Student:

    def __init__(self):
        self.x = 0
        self.y = 0
        return

    def move(self, grid):
        return grid


def create_grid(size_x, size_y):
    ''' Initializes the 3-dimensional grid. Sets border value to 3. In the 3rd dimension:
        1st # is how many infected students occupy the cell, 
        2nd # is how many healthy students occopy the cell, 
        3rd # is temporarily set to 0 with no meaning.'''
    grid = na.zeros(shape=(size_x, size_y, 3)) # [x_pos, y_pos, [institution number, # healthy, # infected]]
    #grid[0, :, :] = 3
    #grid[-1, :, :] = 3
    #grid[:, -1, :] = 3
    #grid[:, 0, :] = 3

    return grid



def add_institution_to_grid(institution_int, grid):
    ''' Adds institution to the grid.
    In the 3rd dimension of grid, a value of -1 on the 1st and 2nd values indicates an institution occupies the cell. 
    In the 3rd dimension of grid, a value of -2 on the 1st and 2nd values indicates an institution door occupies the cell. '''

    print(INSTITUTION_INT_MAP)
    institution = INSTITUTION_INT_MAP[institution_int]
    x_min = institution.posn[0]
    x_max = institution.posn[1]
    y_min = institution.posn[2]
    y_max = institution.posn[3]

    for i in range(x_min, x_max+1):
        for j in range(y_min, y_max+1):
            grid[i, j, 0] = institution_int             # institutions

    if institution.__class__.__name__ in ['Building', 'StudentHousing', 'ParkingArea']:
        for door_posn in institution.door_posns:
            grid[door_posn[0], door_posn[1], 0] = -1    # Institution doors.

    return grid


def create_students(num_of_students):
    ''' Temporary student initialization function.'''
    students = []
    for i in range(num_of_students):
        students.append(Student())

    return students


def simulate_one_step(grid, students, total_students, current_time_period):
    ''' One time period simulator'''
    for i in range(total_students):
        grid = students[i].move(grid)

    current_time_period += 1
    return grid, current_time_period


def create_institutions():
    '''Creates all institutions in the simulation, setting institution names, infection probabilities, positions, 
    and door positions. Adds all institutions to INSTITUTION_INT_MAP.'''

    campus_outdoors = CampusOutdoors(name= 'campus_outdoors',infec_prob=0.0, posn=[0, 0, 0, 0])
    disc =          Building(name= 'disc',infec_prob=0.0, posn=[528, 574, 256, 393], door_posns=[[574, 296], [528,345], [574,345], [565, 393]])
    uw1 =           Building(name= 'uw1',infec_prob=0.0, posn=[364, 575, 478, 515], door_posns=[[364,496], [495, 478], [575, 493], [494, 515],[480, 515]])
    uw2 =           Building(name= 'uw2',infec_prob=0.0, posn=[400, 527, 355, 396], door_posns=[[400, 390], [429, 396], [433, 395]])
    lb1 =           Building(name= 'lb1',infec_prob=0.0, posn=[621, 752, 421, 470], door_posns=[[664,470]])
    lb2 =           Building(name= 'lb2',infec_prob=0.0, posn=[725, 780, 486, 570], door_posns=[[725, 486]])
    uwbb =          Building(name= 'uwbb',infec_prob=0.0, posn=[1590, 1686, 330, 400], door_posns=[[1630, 400]])
    arc =           Building(name= 'arc',infec_prob=0.0, posn=[665, 711, 569, 633], door_posns=[[711,585]])
    subway =        Building(name= '',infec_prob=0.0, posn=[604, 620, 432, 468], door_posns=[[611, 470]])
    bus_stop =      BusStop(name= 'bus_stop',infec_prob=0.0, posn=[1070, 1144, 340, 447])
    husky_village = StudentHousing(name= 'husky_village',infec_prob=0.0, posn=[1290, 1390, 160, 300], door_posns=[[1290, 160], [1390, 160], [1390, 300]])
    parking_area_1 =ParkingArea(name= 'parking_area_1',infec_prob=0.0, posn=[467, 674, 155, 215], door_posns=[[590, 215]])
    parking_area_2 =ParkingArea(name= 'parking_area_2',infec_prob=0.0, posn=[100, 300, 32, 525], door_posns=[[300,395]])
    parking_area_3 =ParkingArea(name= 'parking_area_3',infec_prob=0.0, posn=[996, 1154, 563, 616], door_posns=[[1150, 563]])
    ccc_1_2 =       Building(name= 'ccc_1_2',infec_prob=0.0, posn=[818, 1020, 484, 525])
    ccc_3 =         Building(name= 'ccc_3',infec_prob=0.0, posn=[892, 1030, 343, 408])

    global INSTITUTION_INT_MAP
    INSTITUTION_INT_MAP = {0: campus_outdoors, \
                           1: disc, \
                           2: uw1, \
                           3: uw2, \
                           4: lb1, \
                           5: lb2, \
                           6: uwbb, \
                           7: arc, \
                           8: subway, \
                           9: bus_stop, \
                           10: husky_village, \
                           11: parking_area_1, \
                           12: parking_area_2, \
                           13: parking_area_3, \
                           14: ccc_1_2, \
                           15: ccc_3}

    # Adjust x and y, mins and maxes, and door positions, according to selected size_x and size_y
    for instit_int in INSTITUTION_INT_MAP.keys():
        instit = INSTITUTION_INT_MAP[instit_int]

        for i in range(len(instit.posn)):
            instit.posn[i] /= (float(orig_img_size_y)/size_y)
            instit.posn[i] = int(math.floor(INSTITUTION_INT_MAP[instit_int].posn[i]))

        if INSTITUTION_INT_MAP[instit_int].__class__.__name__ in ['Building', 'StudentHousing', 'ParkingArea']:
            for i in range(len(instit.door_posns)):
                instit.door_posns[i][0] /= (float(orig_img_size_y) / size_y)
                instit.door_posns[i][1] /= (float(orig_img_size_y) / size_y)
                instit.door_posns[i][0] = int(math.floor(instit.door_posns[i][0]))
                instit.door_posns[i][1] = int(math.floor(instit.door_posns[i][1]))

        add_institution_to_grid(instit_int, campus)



def run_simulation(campus, cur_time, all_students):
    '''Runs simulation 'total_steps' number of time steps. Displays visualization (animation).'''

    #TODO: increment day after the appropriate # of time steps.

    plt.ion()
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_axes((0, 0, 1, 1), frameon=False)

    visualizer = na.zeros((size_x, size_y, 3), 'f')
    result = ax.imshow(visualizer, interpolation='none', extent=[0, 100, 0, 100], aspect='auto', zorder=0)
    ax.axis('off')

    campus, cur_time = simulate_one_step(campus, all_students, TOTAL_STUDENTS, cur_time)

    for h in range(TOTAL_STEPS):
        campus, cur_time = simulate_one_step(campus, all_students, TOTAL_STUDENTS, cur_time)
        visualizer = na.zeros((size_y, size_x, 3), 'f')
        for i in na.arange(1, size_x - 1):      # go through each cell except boundaries
            for j in na.arange(1, size_y - 1):
                if campus[i, j, 0] == 0:    # CampusOutdoors
                    visualizer[j, i, 0] = 0
                    visualizer[j, i, 1] = 1 # green
                    visualizer[j, i, 2] = 0
                elif campus[i, j, 0] == -1: # doors
                    visualizer[j, i, 0] = 0
                    visualizer[j, i, 1] = 0
                    visualizer[j, i, 2] = 1 # blue
                else:                       # institutions that are not CampusOutdoors
                    visualizer[j, i, 0] = 1
                    visualizer[j, i, 1] = 1 # green
                    visualizer[j, i, 2] = 1
        for i in range(len(all_students)):  # Note: can use 1 - ratio to make redder
            if campus[all_students[i].x, all_students[i].y, 0] == 0: # If outdoors, we are going to color student grid
                if campus[all_students[i].x, all_students[i].y, 1] != 0 \
                        and campus[all_students[i].x, all_students[i].y, 2] != 0:
                    ratio = campus[all_students[i].x, all_students[i].y, 1] / \
                            campus[all_students[i].x, all_students[i].y, 2]
                    visualizer[all_students[i].y, all_students[i].x, :] = na.array([1, ratio, ratio])
                elif campus[all_students[i].x, all_students[i].y, 1] == 0 and \
                        campus[all_students[i].x, all_students[i].y, 2] != 0:
                    visualizer[all_students[i].y, all_students[i].x, :] = na.array([1, 0, 0])
                elif campus[all_students[i].x, all_students[i].y, 1] != 0 and \
                        campus[all_students[i].x, all_students[i].y, 2] == 0:
                    visualizer[all_students[i].y, all_students[i].x, :] = na.array([1, 1, 1])

        result.set_data(visualizer)
        plt.draw()
        plt.pause(0.01)


#======================================================= Main ==========================================================


DT = 5                  # adjustable. Unit: minutes.
MINS_PER_DAY = 60.0 * 24
TOTAL_STUDENTS = 5000   # adjustable
TOTAL_STEPS = int(MINS_PER_DAY / DT * 5)   # simulate 5 days. Each day has MINUTES_PER_DAY / DT time steps.
cur_time = 0            # current time, in minutes. (e.g. 601 == 10:01 a.m.)
cur_step = 0
cur_day = 0             # 1st day == day 0.

orig_img_size_y = 800   # height of image (in pixels) used to determine all institution coordinates
size_x = 330            # width of grid
size_y = int(size_x/2.2)     # height of grid

campus = create_grid(size_x, size_y)
all_students = create_students(TOTAL_STUDENTS)

INSTITUTION_INT_MAP = {}
create_institutions()

run_simulation(campus, cur_time, all_students)
