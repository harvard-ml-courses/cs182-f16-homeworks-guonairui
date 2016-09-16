	# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).

LARRY GUO + AUGUST HOLM
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    """

    "*** YOUR CODE HERE ***"
    # HERE IS THE NON OPTIMIZED VERSION THAT GETS ALL THE POINTS ON THE AUTOGRADER
    # Using a stack for the fringe
    fringe = util.Stack()

    # Using a set for visited nodes because it handles duplicate values better
    visited = set()
    # Pushes the start state
    fringe.push((problem.getStartState(), [], 0))

    # While the fringe isn't empty
    while not fringe.isEmpty():
        state, moves, total = fringe.pop()

        # If we've visited the state, move on to next iteration
        if state in visited:
            continue

        # If the problem is a GoalState, return the moves to get there
        if problem.isGoalState(state):
            return moves

        # Add the state to visited
        visited.add(state)

        # Add each successor to the fringe
        for new, nextt, cost in problem.getSuccessors(state):
            fringe.push((new, moves + [nextt], total + cost))

    # Return no moves if no goal was met
    return []

    """
    # HERE IS THE "OPTIMIZED" VERSION THAT KEEPS TRACK OF THE FRONTIER

    fringe = util.Stack()

    visited = set()
    frontier = set()
    fringe.push((problem.getStartState(), [], 0))

    while not fringe.isEmpty():
        state, moves, total = fringe.pop()

        if state in visited:
            continue

        if problem.isGoalState(state):
            return moves

        visited.add(state)

        for new, nextt, cost in problem.getSuccessors(state):
            if new not in frontier:
                fringe.push((new, moves + [nextt], total + cost))
                frontier.add(new)

    return []
    """



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    "*** YOUR CODE HERE ***"

    # HERE IS THE NON OPTIMIZED VERSION THAT GETS ALL THE POINTS ON THE AUTOGRADER
    
    fringe = util.Queue()
    visited = set()
    fringe.push((problem.getStartState(), [], 0))

    while not fringe.isEmpty():
        state, moves, total = fringe.pop()

        if state in visited:
            continue

        if problem.isGoalState(state):
            return moves

        visited.add(state)

        for new, nextt, cost in problem.getSuccessors(state):
            fringe.push((new, moves + [nextt], total + cost))

    return []

    """
    # HERE IS THE OPTIMIZED VERSION THAT KEEPS TRACK OF THE FRONTIER
    # Using a queue for the fringe
    fringe = util.Queue()
    visited = set()
    frontier = set()
    fringe.push((problem.getStartState(), [], 0))

    # Continues to push new successor states onto the fringe while ignoring visited
    # states and also returning moves if the state is a goal
    while not fringe.isEmpty():
        state, moves, total = fringe.pop()

        if state in visited:
            continue

        visited.add(state)

        # Optimization for BFS where it checks for goal on push not pop
        for new, nextt, cost in problem.getSuccessors(state):
            if problem.isGoalState(new):
                return moves + [nextt]
            if new not in frontier:
                fringe.push((new, moves + [nextt], total + cost))
                frontier.add(new)

    return []
    """
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    "*** YOUR CODE HERE ***"

    # Using a priority queue for the fringe
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push((problem.getStartState(), [], 0), 0)

    # Continues to push new successor states onto the fringe while ignoring visited
    # states and also returning moves if the state is a goal.
    # Calculates priority solely on the cost of the actions it takes to get to that state
    while not fringe.isEmpty():
    	state, moves, total = fringe.pop()

    	if state in visited:
    		continue

    	if problem.isGoalState(state):
    		return moves

    	visited.add(state)

    	for new, nextt, cost in problem.getSuccessors(state):
    		fringe.push((new, moves + [nextt], total + cost), total + cost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    "*** YOUR CODE HERE ***"

    # Using a priority queue for the fringe
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem))

    # Continues to push new successor states onto the fringe while ignoring visited
    # states and also returning moves if the state is a goal.
    # Pushes priority based on a heuristic as well as cost from the start state
    while not fringe.isEmpty():
    	state, moves, total = fringe.pop()

    	if state in visited:
    		continue

    	if problem.isGoalState(state):
    		return moves

    	visited.add(state)

    	for new, nextt, cost in problem.getSuccessors(state):
    		fringe.push((new, moves + [nextt], total + cost), total + cost + heuristic(new, problem))

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
