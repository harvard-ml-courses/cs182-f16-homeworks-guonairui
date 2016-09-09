##### Filename: util.py
##### Author: {your name}
##### Date: {current date}
##### Email: {your email}

import copy
from collections import deque

## Problem 1
def matrix_multiply(x, y):
	rows = len(x)
	cols = len(y[0])
	z = [[0 for row in range(rows)] for col in range(cols)]
	for i in range(rows):
		for j in range(cols):
			for k in range(len(x[0])):
				z[i][j] += x[i][k] * y[k][j]
	return z

## Problem 2, 3

class MyQueue:
    def __init__(self):
        self.items = deque()
    def push(self, val):
        self.items.append(val)
    def pop(self):
    	if len(self.items) == 0:
    		return None
        else:
        	return self.items.popleft()
    def __eq__(self, other):
        while len(self.items) > 0:
        	if self.pop() != other.pop():
        		return False
		return True
    def __ne__(self, other):
        while len(self.items) > 0:
        	if self.pop() != other.pop():
        		return True
		return False
    def __str__(self):
    	a = ""
        for i in self.items:
        	a = a + str(i)
    	return a

class MyStack:
    def __init__(self):
        self.items = deque()
    def push(self, val):
        self.items.append(val)
    def pop(self):
        if len(self.items) == 0:
        	return None
    	else:
    		return self.items.pop()
    def __eq__(self, other):
        while len(self.items) > 0:
        	if self.pop() != other.pop():
        		return False
		return True
    def __ne__(self, other):
        while len(self.items) > 0:
        	if self.pop() != other.pop():
        		return True
		return False
    def __str__(self):
        a = ""
        for i in self.items:
        	a = a + str(i)
    	return a

## Problem 4

def add_position_iter(lst, number_from=0):
	temp = []
	for i in range(len(lst)):
		temp.append(lst[i] + i + number_from)
	return temp

def add_position_recur(lst, number_from=0):
	a = list(enumerate(lst, start = number_from))
	if len(lst) == 0:
		return lst
	return add_position_recur(lst[:-1], number_from) + [a[-1][0] + a[-1][1]]

def add_position_map(lst, number_from=0):
	a = list(enumerate(lst, start = number_from))
	return list(map(lambda (x): x[0] + x[1], a))
	pass

## Problem 5

def remove_course(roster, student, course):
    if student in roster and course in roster.get(student):
    	roster.get(student).remove(course)
	return roster

## Problem 6

def copy_remove_course(roster, student, course):
    temp = copy.deepcopy(roster)
    remove_course(temp, student, course)
    return temp

