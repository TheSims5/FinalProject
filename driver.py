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
from classroom import Classroom
from activity import Activity
from schedule import Schedule
from course import Course
from student import Student



def create_grid(size_x, size_y):
    ''' Initializes the 3-dimensional grid. Sets border value to 3. In the 3rd dimension:
        1st # is how many infected students occupy the cell, 
        2nd # is how many healthy students occopy the cell, 
        3rd # is temporarily set to 0 with no meaning.'''

    grid = na.zeros(shape=(size_x, size_y, 5))
    # grid structure:
    # [int xpos, int ypos,
    #                      [int instit,
    #                       # of healthy stud at cell,
    #                       # of infected stud at cell,
    #                       aerosol_infec_prob,
    #                       surface_infec_prob]]


    #grid[0, :, :] = 3
    #grid[-1, :, :] = 3
    #grid[:, -1, :] = 3
    #grid[:, 0, :] = 3

    return grid



def add_institution_to_grid(institution_int, grid):
    ''' Adds institution to the grid.
    In the 3rd dimension of grid, a value of -1 on the 1st and 2nd values indicates an institution occupies the cell. 
    In the 3rd dimension of grid, a value of -2 on the 1st and 2nd values indicates an institution door occupies the cell. '''

    institution = INSTITUTION_INT_MAP[institution_int]
    x_min = institution.posn[0]
    x_max = institution.posn[1]
    y_min = institution.posn[2]
    y_max = institution.posn[3]

    for i in range(x_min, x_max+1):
        for j in range(y_min, y_max+1):
            grid[i, j, 0] = institution_int             # institutions
            #print(grid)   #REMOVE.

    if institution.__class__.__name__ in ['Building', 'ParkingArea', 'BusStop']:
        #for door_posn in institution.door_posns:
        #    grid[door_posn[0], door_posn[1], 0] = 0    # Institution doors.

        if institution.name in ['uw1', 'uw2', 'disc']:
            # Add classrooms to grid.
            for i in range(len(institution.classrooms)):
                classroom_x_min = institution.classrooms[i].posn[0]
                classroom_x_max = institution.classrooms[i].posn[1]
                classroom_y_min = institution.classrooms[i].posn[2]
                classroom_y_max = institution.classrooms[i].posn[3]

                # Set grid values at Classroom borders
                for m in [classroom_x_min, classroom_x_max + 1]:
                    for n in range(classroom_y_min, classroom_y_max + 1):
                        grid[m, n, 0] = -2
                for m in [classroom_y_min, classroom_y_max + 1]:
                    for n in range(classroom_x_min, classroom_x_max + 1):
                        grid[n, m, 0] = -2

    return grid


#def create_students(num_of_students):
#    ''' Temporary student initialization function.'''
#    students = []
#    for i in range(num_of_students):
#        students.append(Student())
#
#    return students


def simulate_one_step(grid, students, total_students, cur_time):
    
    ''' One time period simulator'''
    for i in range(total_students):
        grid = students[i].move(grid, cur_time, INSTITUTION_INT_MAP)

    return grid


def create_institutions():
    '''Creates all institutions in the simulation, setting institution names, infection probabilities, positions, 
    and door positions. Adds all institutions to INSTITUTION_INT_MAP.'''

    campus_outdoors = CampusOutdoors(name= 'campus_outdoors',infec_prob=0.0, posn=[0, 0, 0, 0])


    # With old door posns. (flush w/ rest of building)
    #disc =          Building(name= 'disc',infec_prob=0.0, posn=[528, 574, 256, 393], door_posns=[[574, 296], [574,345], [565, 393]])   # , [528,345]
    #uw1 =           Building(name= 'uw1',infec_prob=0.0, posn=[364, 575, 478, 515], door_posns=[[364,496], [495, 478], [575, 493], [494, 515],[480, 515]])
    #uw2 =           Building(name= 'uw2',infec_prob=0.0, posn=[400, 527, 355, 393], door_posns=[[400, 390], [429, 393], [433, 393]])


    # With new door posns. protruding from building walls.
    disc = Building(name='disc', infec_prob=0.0, posn=[528, 574, 256, 393],
                    door_posns=[[575, 296], [576, 296], [575, 345], [576, 345],[565, 394], [565, 395],[527,345], [526,345], \
                                [555, 255 ], [555, 254 ] ] )  # , [528,345]
    uw1 = Building(name='uw1', infec_prob=0.0, posn=[364, 575, 478, 515],
                   door_posns=[[363, 496], [495, 477], [576, 493], [494, 516], [480, 516], \
                               [362, 496], [495, 476], [577, 493], [494, 517], [480, 517]])
    uw2 = Building(name='uw2', infec_prob=0.0, posn=[400, 527, 355, 393],
                   door_posns=[[399, 390], [429, 394], [433, 394], \
                               [398, 390], [429, 395], [433, 395], [520, 354], [520, 353], [410, 354], [410, 353],])


    lb1 =           Building(name= 'lb1',infec_prob=0.0, posn=[621, 752, 421, 470], door_posns=[[664,470]])
    lb2 =           Building(name= 'lb2',infec_prob=0.0, posn=[725, 780, 486, 570], door_posns=[[725, 486]])
    #uwbb =          Building(name= 'uwbb',infec_prob=0.0, posn=[1590, 1686, 330, 400], door_posns=[[1630, 400]])
    #arc =           Building(name= 'arc',infec_prob=0.0, posn=[665, 711, 569, 633], door_posns=[[711,585]])
    #subway =        Building(name= '',infec_prob=0.0, posn=[604, 620, 432, 468], door_posns=[[611, 470]])
    #bus_stop =      BusStop(name= 'bus_stop',infec_prob=0.0, posn=[1070, 1144, 340, 447], door_posns=[[1144, 340]])
    #bus_stop =      BusStop(name= 'bus_stop',infec_prob=0.0, posn=[ - 15, size_x - 10, float(size_y) * 2/3, float(size_y) * 3/4], door_posns=[[840, 480]])
    bus_stop = BusStop(name='bus_stop', infec_prob=0.0,
                       posn=[840, 880, 460, 500], door_posns=[[840, 480]])

    #husky_village = StudentHousing(name= 'husky_village',infec_prob=0.0, posn=[1290, 1390, 160, 300], door_posns=[[1290, 160], [1390, 160], [1390, 300]])

    # With old door posns. flush with institution boundaries.
    #parking_area_1 =ParkingArea(name= 'parking_area_1',infec_prob=0.0, posn=[467, 674, y_offset + 1, 215], door_posns=[[590, 215]])
    #parking_area_2 =ParkingArea(name= 'parking_area_2',infec_prob=0.0, posn=[x_offset + 1, 300, y_offset + 1, 525], door_posns=[[300,395]])


    # With new door posns. protruding from institution boundaries.
    parking_area_1 = ParkingArea(name='parking_area_1', infec_prob=0.0, posn=[467, 674, y_offset + 1, 215],
                                 door_posns=[[590, 216], [590, 217]])
    parking_area_2 = ParkingArea(name='parking_area_2', infec_prob=0.0, posn=[x_offset + 1, 300, y_offset + 1, 525],
                                 door_posns=[[301, 395], [302, 395]])

    #parking_area_3 =ParkingArea(name= 'parking_area_3',infec_prob=0.0, posn=[996, 1154, 563, 616], door_posns=[[1150, 563]])
    #ccc_1_2 =       Building(name= 'ccc_1_2',infec_prob=0.0, posn=[818, 1020, 484, 525])
    #ccc_3 =         Building(name= 'ccc_3',infec_prob=0.0, posn=[892, 1030, 343, 408])

    global INSTITUTION_INT_MAP
    INSTITUTION_INT_MAP = {0: campus_outdoors, \
                           1: disc, \
                           2: uw1, \
                           3: uw2, \
                           4: lb1, \
                           5: lb2, \
                           #6: uwbb, \
                           #7: arc, \
                           #8: subway, \
                           9: bus_stop, \
                           #10: husky_village, \
                           11: parking_area_1, \
                           12: parking_area_2, \
                           #13: parking_area_3, \
                           #14: ccc_1_2, \
                           #15: ccc_3
                            }


    # Adjust x and y, mins and maxes, and door positions, according to selected size_x and size_y
    for instit_int in INSTITUTION_INT_MAP.keys():
        instit = INSTITUTION_INT_MAP[instit_int]

        for i in range(len(instit.posn)):
            if i in [0, 1]:     # If it's either x_min or x_max
                instit.posn[i] -= x_offset
            else:
                instit.posn[i] -= y_offset
            instit.posn[i] *= (float(size_y)/ orig_img_size_y)
            instit.posn[i] = int(math.floor(INSTITUTION_INT_MAP[instit_int].posn[i]))


        if INSTITUTION_INT_MAP[instit_int].__class__.__name__ in ['Building', 'ParkingArea', 'BusStop']:

            for i in range(len(instit.door_posns)):
                instit.door_posns[i][0] -= x_offset
                instit.door_posns[i][1] -= y_offset
                instit.door_posns[i][0] *= (float(size_y)/ orig_img_size_y)
                instit.door_posns[i][1] *= (float(size_y)/ orig_img_size_y)
                instit.door_posns[i][0] = int(math.floor(instit.door_posns[i][0]))
                instit.door_posns[i][1] = int(math.floor(instit.door_posns[i][1]))


        if instit.name in ['uw1', 'uw2', 'disc']:
            cols = 5
            rows = 2
            if instit.name == 'disc':
                cols = 2
                rows = 5
            x_min = instit.posn[0]
            x_max = instit.posn[1]
            y_min = instit.posn[2]
            y_max = instit.posn[3]
            width = x_max - x_min
            height = y_max - y_min
            width_of_one_classroom = (float(width - 2) / cols) - 2 # 2 rows between each classroom and between classrooms and building boundaries
            width_of_one_classroom = int(width_of_one_classroom)
            height_of_one_classroom = (float(height - 2) / rows) - 2
            height_of_one_classroom = int(height_of_one_classroom)

            for col in range(cols):
                for row in range(rows):
                    instit.classrooms.append(Classroom(posn=[x_min + 2 + col*(2 + width_of_one_classroom),
                                                          x_min + 2 + col*(2 + width_of_one_classroom) + width_of_one_classroom,
                                                          y_min + 2 + row * (2 + height_of_one_classroom),
                                                          y_min + 2 + row * (2 + height_of_one_classroom) + height_of_one_classroom]))


        add_institution_to_grid(instit_int, campus)




def run_simulation(campus, cur_time, all_students):
    '''Runs simulation 'total_steps' number of time steps. Displays visualization (animation).'''

    plt.ion()
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_axes((0, 0, 1, 1), frameon=False)

    visualizer = na.zeros((size_x, size_y, 3), 'f')
    result = ax.imshow(visualizer, interpolation='none', extent=[0, 100, 0, 100], aspect='auto', zorder=0)
    ax.axis('off')

    campus = simulate_one_step(campus, all_students, TOTAL_STUDENTS, cur_time)

    for h in range(TOTAL_STEPS):

        #Testing:
        #if (h % 100 == 0):
        #    print("cur_time in minutes: " + str(cur_time))
        #    print("student cur_posn: " + str(all_students[0].cur_posn))


        campus = simulate_one_step(campus, all_students, TOTAL_STUDENTS, cur_time)
        visualizer = na.zeros((size_y, size_x, 3), 'f')



        for i in na.arange(1, size_x - 1):      # go through each cell except boundaries
            for j in na.arange(1, size_y - 1):


                if campus[i, j, 0] == 0:    # CampusOutdoors: white. For easy visualization of students.
                    visualizer[j, i, 0] = 1
                    visualizer[j, i, 1] = 1
                    visualizer[j, i, 2] = 1
                # elif campus[i, j, 0] == -1: # doors: cyan
                #     visualizer[j, i, 0] = 0
                #     visualizer[j, i, 1] = 0
                #     visualizer[j, i, 2] = 1

                elif campus[i, j, 0] == -2: # classroom borders: cyan
                    visualizer[j, i, 0] = 0
                    visualizer[j, i, 1] = 0
                    visualizer[j, i, 2] = 1
                else:                       # institutions that are not CampusOutdoors: white
                    visualizer[j, i, 0] = 1
                    visualizer[j, i, 1] = 1
                    visualizer[j, i, 2] = 1



                    cur_instit_int = campus[i, j, 0]
                    cur_instit = INSTITUTION_INT_MAP[cur_instit_int]
                    x_min = cur_instit.posn[0]
                    x_max = cur_instit.posn[1]
                    y_min = cur_instit.posn[2]
                    y_max = cur_instit.posn[3]

                    if cur_instit_int > 0 and \
                            (i in [x_min, x_max] or j in [y_min, y_max]):    # If it's a insitution border: color it black
                        visualizer[j, i, 0] = 0
                        visualizer[j, i, 1] = 0
                        visualizer[j, i, 2] = 0
                temp_a = campus[i, j, 3] + campus[i, j, 4]
                #if temp_a != 0:
                #    visualizer[j, i, 0] = temp_a / 1
                #    visualizer[j, i, 1] = 0
                #    visualizer[j, i, 2] = 1

        a = [1, 2, 3, 9, 11, 12]
        for i in a:
            temp_door_list = INSTITUTION_INT_MAP[i].door_posns
            for j in range(len(temp_door_list)):
                temp_door_x = temp_door_list[j][0]
                temp_door_y = temp_door_list[j][1]
                visualizer[temp_door_y, temp_door_x,:] = na.array([0, 0, 1])

        for i in range(len(all_students) - 1, -1, -1):  # Note: can use 1 - ratio to make redder

            # CampusOutdoors is colored white. (1, 1, 1)
            # Other Institutions are colored yellow. (Any institution with int > 0)  (1, 1, 0)
            # Doors & classroom borders are colored cyan (0, 1, 1)
            # If a cell has at least 1 infected student, the cell is colored black.  (0, 0, 0)
            # If a cell has at least 1 student, but 0 infected students, it's colored red. (1, 0 0)

            # if campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 0] == 0: # If outdoors, we are going to color student grid




            # [int xpos, int ypos, [int instit#,
            #                        int # of healthy stud at cell,
            #                        int # of infected stud at cell,
            #                        float aerosol_infec_prob,
            #                        float surface_infec_prob] ]



            #if all_students[i].doing_random_walk:  # REMOVE



            cur_stud = all_students[i]

            #if there's at least 1 infected student at this cell, color cell black.
            if campus[cur_stud.cur_posn[0], cur_stud. cur_posn[1], 2] > 0:
                visualizer[all_students[i].cur_posn[1], all_students[i].cur_posn[0], :] = na.array([0,1, 0])
            else:
                visualizer[all_students[i].cur_posn[1], all_students[i].cur_posn[0], :] = na.array([1,0 , 0])

            if cur_stud.is_contagious:
                visualizer[all_students[i].cur_posn[1], all_students[i].cur_posn[0], :] = na.array([0, 0, 0])

            '''
            if all_students[i].doing_random_walk:   #REMOVE

                # If this cell the student is on is not outdoors, and
                if campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 1] != 0 \
                        and campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 2] != 0:
                    ratio = campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 1] / \
                            campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 2]
                    visualizer[all_students[i].cur_posn[1], all_students[i].cur_posn[0], :] = na.array([1, ratio, ratio])
                elif campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 1] == 0 and \
                                campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 2] != 0:
                    visualizer[all_students[i].cur_posn[1], all_students[i].cur_posn[0], :] = na.array([1, 0, 0])
                elif campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 1] != 0 and \
                                campus[all_students[i].cur_posn[0], all_students[i].cur_posn[1], 2] == 0:
                    visualizer[all_students[i].cur_posn[1], all_students[i].cur_posn[0], :] = na.array(
                        [1, 0, 1])                                  # ([1, 0, 1] is pink.) # TODO: set back to  [1, 1, 1]

            '''


        cur_time += DT


        result.set_data(visualizer)
        plt.draw()
        plt.pause(0.00001)



def create_students():
    create_Courses(525, 645, 1, 15)
    create_Courses(660, 780, 2, 30)
    create_Courses(795, 915, 3, 30)
    create_Courses(930, 1050, 4, 30)
    create_Courses(1065, 1185, 5, 30)
    create_Courses(1200, 1320, 6, 15)

    students = []
    for i in range(TOTAL_STUDENTS):

        s1 = Student()
        s1.time_of_infection = -1
        if i < CONTAGIOUS_STUDENTS:
            s1.is_contagious = True
            s1.is_infected = True
            s1.time_of_infection = 0
            print("*******************************time_of_infection  : 0")
            
        students.append(s1)
        rand_number = rand.randint(1,4)
        student_pick_Courses(s1, rand_number)

        s1.starting_posn[0] -= x_offset
        s1.starting_posn[0] *= (float(size_y) / orig_img_size_y)
        s1.starting_posn[1] -= y_offset
        s1.starting_posn[1] *= (float(size_y) / orig_img_size_y)

        s1.starting_posn[0] = int(s1.starting_posn[0])
        s1.starting_posn[1] = int(s1.starting_posn[1])    
        

    
    return students



def create_Courses(starting_time, ending_time, time_slot_index, number_of_class_to_be_created):
    for i in range(number_of_class_to_be_created):
        #     starting_time = 8.75*60
        #     ending_time = 10.75*60
        #

        # institution_is_availiable = {1:False,2:False,3:False}

        array_of_institution_index = na.array((1, 2, 3))

        #UNCOMMENT
        rand.shuffle(array_of_institution_index)
        for i in array_of_institution_index:
            done = False
            selected_institution_number = i
            classroom_list = INSTITUTION_INT_MAP[i].classrooms

            classroom_index = na.array(range(len(classroom_list)))

            #UC
            rand.shuffle(classroom_index)

            for j in classroom_index:
                if classroom_list[j].open[time_slot_index - 1] == True:
                    INSTITUTION_INT_MAP[i].classrooms[j].open[time_slot_index - 1] = False
                    selected_classroom_number = j
                    classroom = classroom_list[selected_classroom_number]
                    course = Course(starting_time, ending_time, selected_institution_number, classroom)
                    all_courses[time_slot_index].append(course)
                    done = True
                    break
            if done:
                break



def student_pick_Courses(stud, num_of_class):

    #TODO: change back to 1, 2, 3, 4, 5, 6
    array_of_time_slot = na.array((4, 1, 3, 2, 5, 6))

    #UNCOMMENT.
    rand.shuffle(array_of_time_slot)

    num_of_selected = 0
    temp_activity_list = []

    for time in array_of_time_slot:
        if num_of_selected == num_of_class:
            break

        list_of_courses = all_courses.get(time)
        course_indices = na.arange(len(list_of_courses))
        #UNCOMMENT
        rand.shuffle(course_indices)
        for course in range(len(course_indices)):

            selected_course_index = course_indices[course]
            course = list_of_courses[selected_course_index]

            if course.cur_num_of_students < course.capacity:
                activity = Activity(course)
                temp_activity_list.append(activity)
                course.cur_num_of_students += 1
                column = course.x_size_of_classroom
                seat_posn_x = course.cur_num_of_students % column
                seat_posn_y = course.cur_num_of_students / column
                course.open_seats[seat_posn_y, seat_posn_x] = False

                seat_posn_x = seat_posn_x + course.classroom_x_min + 1
                seat_posn_y = seat_posn_y + course.classroom_y_min + 1
                activity.seat_posn = (seat_posn_x, seat_posn_y)
                num_of_selected += 1
                break

    if len(temp_activity_list) == 2:
        if (temp_activity_list[0].start_time > temp_activity_list[1].start_time):
            temp = temp_activity_list[1]
            temp_activity_list[1] = temp_activity_list[0]
            temp_activity_list[0] = temp

    if len(temp_activity_list) == 3:
        if (temp_activity_list[0].start_time > temp_activity_list[1].start_time):
            temp = temp_activity_list[1]
            temp_activity_list[1] = temp_activity_list[0]
            temp_activity_list[0] = temp

        if (temp_activity_list[1].start_time > temp_activity_list[2].start_time):
            temp = temp_activity_list[2]
            temp_activity_list[2] = temp_activity_list[1]
            temp_activity_list[1] = temp

        if (temp_activity_list[0].start_time > temp_activity_list[1].start_time):
            temp = temp_activity_list[1]
            temp_activity_list[1] = temp_activity_list[0]
            temp_activity_list[0] = temp


    stud.schedule = Schedule()
    stud.schedule.activities = temp_activity_list

# END FROM HOI YAN'S DRIVER============================================================================================



#======================================================= Main ==========================================================

# Adjustable-----------------------------------------------------------------
x_offset = 290
y_offset = 205
DT = 0.5           # Unit: minutes.
TOTAL_STUDENTS = 1000
CONTAGIOUS_STUDENTS = 10 #Number of contagious students
cur_time = 510          # current time, in minutes. (e.g. 601 == 10:01 a.m.)
#----------------------------------------------------------------------------


MINS_PER_DAY = 60.0 * 24

TOTAL_STEPS = int(float(MINS_PER_DAY) / DT)   # simulate 5 days. Each day has MINUTES_PER_DAY / DT time steps.

cur_step = 0
cur_day = 1


orig_img_size_y = 600 - y_offset  # height of image (in pixels) used to determine all institution coordinates
orig_img_size_x = orig_img_size_y * float(16) / 10
#size_x = 330            # width of grid
#size_y = int(size_x/2.2)     # height of grid


size_y = 250
#size_y -= float(y_offset) * (float(size_y)/orig_img_size_y)
size_y = int(size_y)
size_x = size_y * float(16) / 10 # (Optimized for screen with aspect ratio 16:10)
size_x = int(size_x)


campus = create_grid(size_x, size_y)

INSTITUTION_INT_MAP = {}

create_institutions()

# Course_list
# 1: has the list of Courses at time slot one 08:45-10:45
# 2: has the list of Courses at time slot two 11:00-13:00
# 3: has the list of Courses at time slot three 13:15-15:15
# 4: has the list of Courses at time slot four 15:30-17:30
# 5: has the list of Courses at time slot five 17:45-19:45
# 6: has the list of Courses at time slot six 20:00-22:00
all_courses = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

all_students = create_students()

run_simulation(campus, cur_time, all_students)

for i in all_students:
    print( str(i.time_of_infection))