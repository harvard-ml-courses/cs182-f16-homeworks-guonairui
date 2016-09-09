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

