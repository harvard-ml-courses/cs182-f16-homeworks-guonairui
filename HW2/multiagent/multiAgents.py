# multiAgents.py
# --------------
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

# Larry Guo and Gabbi Merz

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

alpha = float('-inf')
beta = float('inf')

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        
        "*** YOUR CODE HERE ***"

        # Get number of agents
        numAgents = gameState.getNumAgents()


        # Implement the Dispatch variation of minimax algorithm
        # so we can have multiple min levels
        def value(state, itera):
            agentIndex = itera % numAgents
            
            if itera == self.depth * numAgents or not state.getLegalActions(agentIndex):
              # Use tuples to represent actions towards states
              return ('Stop', self.evaluationFunction(state))
            if agentIndex == self.index:
              return maxValue(state, itera)
            else:
              return minValue(state, itera)

        def minValue(state, itera):
            agentIndex = itera % numAgents

            v = ('Stop', float('inf'))
            for action in state.getLegalActions(agentIndex):
              successor = state.generateSuccessor(agentIndex, action)
              nextAction, nextValue = value(successor, itera + 1)
              if nextValue < v[1]:
                v = (action, nextValue)
            return v

        def maxValue(state, itera):
            agentIndex = itera % numAgents
            v = ('Stop', float('-inf'))
            for action in state.getLegalActions(agentIndex):
              successor = state.generateSuccessor(agentIndex, action)
              nextAction, nextValue = value(successor, itera + 1)
              if nextValue > v[1]:
                v = (action, nextValue)
            return v

        bestMove = value(gameState, 0)
        return bestMove[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Get the number of agents
        numAgents = gameState.getNumAgents()

        # Using the dispatch implementation of minimax to deal with multiple ghosts
        def value(state, alpha, beta, itera):
            # Update agentIndex based on number of iteration loops
            agentIndex = itera % numAgents

            # If at max depth or no legal moves, return evaluation function
            if itera == self.depth * numAgents or not state.getLegalActions(agentIndex):
              return ('Stop', self.evaluationFunction(state))

            # If we are pacman, do max, if not do min
            if agentIndex == self.index:
              return maxValue(state, alpha, beta, itera)
            else:
              return minValue(state, alpha, beta, itera)

        def minValue(state, alpha, beta, itera):
            # Update agentIndex based on number of iteration loops
            agentIndex = itera % numAgents

            # Initialize minimum as infinity
            v = ('Stop', float('inf'))

            # For all legal actions, loop through and update min, alpha, and beta accordingly
            for action in state.getLegalActions(agentIndex):
              nextAction, nextValue = value(state.generateSuccessor(agentIndex, action), alpha, beta, itera + 1)
              if nextValue < v[1]:
                v = (action, nextValue)
              if v[1] < alpha:
                return v
              beta = min(beta, v[1])
            return v

        def maxValue(state, alpha, beta, itera):
            # Update agentIndex based on number of iteration loops
            agentIndex = itera % numAgents

            # Initialize minimum as negative infinity
            v = ('Stop', float('-inf'))

            # For all legal actions, loop through and update min, alpha, and beta accordingly
            for action in state.getLegalActions(agentIndex):
              nextAction, nextValue = value(state.generateSuccessor(agentIndex, action), alpha, beta, itera + 1)
              if nextValue > v[1]:
                v = (action, nextValue)
              if v[1] > beta:
                return v
              alpha = max(alpha, v[1])
            return v

        # Use the value function to find best move
        bestMove = value(gameState, float('-inf'), float('inf'), 0)
        return bestMove[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # get number of agents 
        numAgents = gameState.getNumAgents()

        def value(state, itera):
            # update agentIndex 
            agentIndex = itera % numAgents
            
            # check if we can ~make moves~ 
            if itera == self.depth * numAgents or not state.getLegalActions(agentIndex):
              return ('Stop', self.evaluationFunction(state))
            if agentIndex == self.index:
              return maxValue(state, itera)
            else:
              return expValue(state, itera)

        def expValue(state, itera):
            agentIndex = itera % numAgents
            v = ('Stop', 0)
            actions = state.getLegalActions(agentIndex)
            for action in actions:
              p = 1 / float(len(actions))
              successor = value(state.generateSuccessor(agentIndex, action), itera + 1)
              v = (action, (v[1] + (p * successor[1])))
            return v

        def maxValue(state, itera):
            agentIndex = itera % numAgents
            v = ('Stop', float('-inf'))
            for action in state.getLegalActions(agentIndex):
              successor = state.generateSuccessor(agentIndex, action)
              nextAction, nextValue = value(successor, itera + 1)
              if nextValue > v[1]:
                v = (action, nextValue)
            return v

        bestMove = value(gameState, 0)
        return bestMove[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

