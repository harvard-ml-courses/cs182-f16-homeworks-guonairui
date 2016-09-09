##### Filename: util.py
##### Author: {your name}
##### Date: {current date}
##### Email: {your email}

import copy
from collections import deque

## Problem 1

def matrix_multiply(x, y):
	C = [[0 for row in range(len(y[0])] for col in range(len(x))
    for i in range(len(x)):
    	for j in range(len(y[0])):
    		for k in range(len(y)):
    			C[i][j] += x[i][k] + y[k][j]
	return C


## Problem 2, 3

class MyQueue:
    def __init__(self):
        pass
    def push(self, val):
        pass
    def pop(self):
        pass
    def __eq__(self, other):
        pass
    def __ne__(self, other):
        pass
    def __str__(self):
        pass

class MyStack:
    def __init__(self):
        pass
    def push(self, val):
        pass
    def pop(self):
        pass
    def __eq__(self, other):
        pass
    def __ne__(self, other):
        pass
    def __str__(self):
        pass

## Problem 4

def add_position_iter(lst, number_from=0):
    pass

def add_position_recur(lst, number_from=0):
    pass

def add_position_map(lst, number_from=0):
    pass

## Problem 5

def remove_course(roster, student, course):
    pass

## Problem 6

def copy_remove_course(roster, student, course):
    pass

