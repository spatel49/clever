#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'find_meeting_slots' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
#  1. INTEGER num_slots
#  2. 2D_STRING_ARRAY employee_schedules
#

import math # need to use it for floor

# Helper function used to increment time by 15 minutes in 24 hour format
def increment_time(time):
    splitTime = time.split(":")
    if math.floor((int(splitTime[1])+15) / 60) > 0:
        if splitTime[0][0] == "0" and splitTime[0][1] != "9":
            splitTime[0] = "0" + str(int(splitTime[0]) + 1)
        else:
            splitTime[0] = str(int(splitTime[0]) + 1)
    if (int(splitTime[1]) + 15) % 60 != 0:
        time = splitTime[0] + ":" + str((int(splitTime[1]) + 15) % 60)
    else:
        time = splitTime[0] + ":00"
    return time

# Main function that returns optimal ranges of times that most employees are
# available to meet in a list, constrained to the number of slots
# Note: It will fail 3 test cases, because it groups all employees together, instead
# of accounting for each distinct employee in the dictionary. For example, if there
# are 4 people, 2 available from 11:00-12:00 and the other two available from 12:00-
# 13:00, the function will output that there is one meeting slot where 2 people are
# available from 11:00-13:00. This can be optimized starting line 55, if we organize
# the dictionary such that each time slot points to an array of distinct employees
# [1, 2, 3, ..., num_employees]. Then we can perform additional steps such as removing
# the employee from the list and getting the length of the list later in the function.
def find_meeting_slots(num_slots, employee_schedules):
    # We will use a dictionary to store time spans and the number of employees
    # that are available during the time span: {timeSpan: numOfEmployees, ...}
    store = {}
    numEmployees = len(employee_schedules)
    finalschedule = []
    
    # Initializes the dictionary with 00:00 : numEmployees, 
    # {00:15 : numEmployees, ... 23:45 : numEmployees}
    for i in range(96):
        if i < 40: #00:00
            if 15*i%60 != 0:
                store["0" + str(math.floor(15*i/60)) + ":" + str(15*i%60)] = numEmployees
            else:
                store["0" + str(math.floor(15*i/60)) + ":00"] = numEmployees
        else:
            if 15*i%60 != 0:
                store[str(math.floor(15*i/60)) + ":" + str(15*i%60)] = numEmployees
            else:
                store[str(math.floor(15*i/60)) + ":00"] = numEmployees
    
    # Loop through all employee schedules to find optimal time
    for i in range(numEmployees):
        # if the employee has no meetings, continue to the next schedule
        if len(employee_schedules[i]) == 0:
            continue
        
        times = employee_schedules[i]
        times.sort()
        
        # Otherwise, remove the employee from the dictionary for all the times
        # that they are not available
        numMeetings = len(times)
        for j in range(numMeetings):
            timeSpanArr = times[j].split("-")
            startTime = timeSpanArr[0]
            endTime = timeSpanArr[1]
            while (startTime != endTime):
                store[startTime] -= 1
                startTime = increment_time(startTime)
        
    # Now that we have all the 15-minute slots where employees are available,
    # we will search through the dictionary for all slots where there are >= 2
    # available employees and append that to our final schedule list.
    startSearch = "00:00"
    while startSearch != "24:00":
        curNumOfEmployees = store[startSearch]
        if curNumOfEmployees >= 2:
            startTime = startSearch
            endTime = increment_time(startSearch)
            while endTime != "24:00" and store[endTime] == curNumOfEmployees:
                endTime = increment_time(endTime)
            finalschedule.append([startTime + "-" + endTime, curNumOfEmployees])
            startSearch = endTime
        else:
            startSearch = increment_time(startSearch)
        
    # We will sort the final list of all available times based on the number of
    # employees available during that time (greatest to lowest)
    finalschedule = sorted(finalschedule, key = lambda x: x[1], reverse=True)
            
    # If there are less number of possible valid meeting slots than the requested
    # num_slots, we return an empty list
    if len(finalschedule) < num_slots:
        return []
    
    # Add the right number of num_slots into our finaloutput array and return
    finaloutput = []
    for i in range(num_slots):
        finaloutput.append(finalschedule[i][0])
    
    return sorted(finaloutput)
if __name__ == '__main__':