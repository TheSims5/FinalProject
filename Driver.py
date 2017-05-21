import numpy as na
import numpy.random as rand
import matplotlib.pyplot as plt


class Student:

    def __init__(self):
        self.x = 0
        self.y = 0
        return

    def move(self, grid):
        return grid

''' Function to initialize the grid and create 3 as the border
    and in the third dimension, first number means how many infected students are overlapping
    second number means how many healthy students are overlapping on the same grid
    third number temporarily set to 0 with no meanings'''


def create_grid(x, y):
    grid = na.zeros(shape=(x, y, 3))
    grid[0, :, :] = 3
    grid[-1, :, :] = 3
    grid[:, -1, :] = 3
    grid[:, 0, :] = 3
    return grid


''' Function to locate the buildings on the map, in the third dimension, -1 on both number means those
    grids occupied by this building, and -2 on both number means the entrance of the building'''


def locate_building(x_min, x_max, y_min, y_max, door_x, door_y, grid):
    for i in range(x_min, x_max+1):
        for j in range(y_min, y_max+1):
            grid[i, j, :] = -1

    grid[door_x, door_y, :] = -2
    return grid

''' Temporary student initialization function to help'''


def init_students(x):
    students = []
    for i in range(x):
        students.append(Student())

    return students


''' One time period simulator'''


def simulate_one_step(grid, students, total_students, current_time_period):
    for i in range(total_students):
        grid = students[i].move(grid)

    current_time_period += 1
    return grid, current_time_period


''' Main program to start here'''

students_num = 5000
steps = 100
time_now = 0
size_x = 100
size_y = 100
campus = create_grid(size_x, size_y)
all_students = init_students(students_num)


''' Start to locate all the buildings and the entrance of them'''

''' End to locate all the buildings'''


''' Below is the visualization part to show the animation by calling simulate_one_step many times'''


plt.ion()
fig = plt.figure(figsize=(8, 5))
ax = fig.add_axes((0, 0, 1, 1), frameon=False)

visualizer = na.zeros((size_x, size_y, 3), 'f')
result = ax.imshow(visualizer, interpolation='none', extent=[0, 100, 0, 100], aspect='auto', zorder=0)
ax.axis('off')

campus, time_now = simulate_one_step(campus, all_students, students_num, time_now)

for h in range(steps):
    campus, time_now = simulate_one_step(campus, all_students, students_num, time_now)
    visualizer = na.zeros((size_x, size_y, 3), 'f')
    for i in na.arange(1, size_x - 1):
        for j in na.arange(1, size_y - 1):
            visualizer[j, i, 0:1] = 1 - campus[i, j, 1]
            if campus[i, j, 1] < 1:
                visualizer[j, i, :] -= campus[i, j, 0] * 5
    for i in range(len(all_students)):
        visualizer[all_students[i].y, all_students[i].x, :] = na.array([0, 1, 0])

    result.set_data(visualizer)
    plt.draw()
    plt.pause(0.01)

