import numpy as n

'''
   This Schedule class will contain information of many schedule for the agent to behave
   Each schedule recorded in this class has a certain chance to be behaved
   There are variables to determine the starting time or ending time of each schedule
'''


class Schedule:

    # In second dimension, first variable means the number of the building
    # second variable means the starting time
    # third variable means the ending time
    # forth variable means the probability
    def __init__(self):
        self.activities = []
        # self.size = 0
        # self.list = n.zeros((length, 4))

#     def display(self):
#         print("activities: " + str(self.activities))
#         
#     # The time will stored in decimal with floating number. For example, 17:38 means 17.38 in this function
#     def increase_schedule(self, objective_building, starting_time, ending_time, probability):
#         self.list[self.size, 0] = objective_building
#         self.list[self.size, 1] = starting_time
#         self.list[self.size, 2] = ending_time
#         self.list[self.size, 3] = probability
#         self.size += 1
# 
#     # You will be able to read any schedule by its index
#     def get_activity(self, index):
#         return self.list[index, 0], self.list[index, 1], self.list[index, 2], self.list[index, 3]



