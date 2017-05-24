import numpy as n
from activity import Activity


class ScheduleList(object):


    all_activities = []             # list of all Actvities
    activities_community_map = {}   # map from int community to a list of activites that community can participate in.


    def __init__(self, community):
        self.schedules = [[],[],[],[],[]]
        self.community = community

        # Class in discovery hall, 1:15 - 3:15pm (start walking at 12:40)
        class1 = Activity(start_time=13 * 60 - 20, end_time=15.25 * 60, dest_institution_int=1)

        # Class in uwbb, 3:30 - 5:30 (start walking at 3:15)
        class2 = Activity(start_time=15.25 * 60, end_time= 17.5 * 60, dest_institution_int=6)

        # Go to the parking area 1. (from 5:30pm to 11:59pm)
        going_home = Activity(start_time=17.5 * 60, end_time= 23 * 60 + 59, dest_institution_int=11)


        self.schedules[0].append(class1)
        self.schedules[0].append(class2)
        self.schedules[0].append(going_home)


s = ScheduleList(1)

#for activ in s.schedules[0]:
#    activ.display()
