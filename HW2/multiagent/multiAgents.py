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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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

        # get number of agents 
        numAgents = gameState.getNumAgents()

        # What do we care about? We want to know which pac-man action returned 
        # the move with the best scores. Let's go ahead and get all of 
        # the actions pac-man can make ('legalMoves')
        legalMoves = gameState.getLegalActions(self.index)

        # update what will be teh agentIndex parameter for the cal to our 'value' function
        newIndex = (self.index + 1) % numAgents

        def value(state, agentIndex, itera):
            # update agentIndex 
            agentIndex = agentIndex % numAgents
            
            # check if we can ~make moves~ 
            if itera == self.depth * numAgents or not state.getLegalActions(agentIndex):
              return self.evaluationFunction(state)
            if agentIndex == self.index:
              return maxValue(state, agentIndex, itera)
            else:
              return minValue(state, agentIndex, itera)

        def minValue(state, agentIndex, itera):
            v = float('inf')
            itera += 1 
            for action in state.getLegalActions(agentIndex):
              v = min(v, value(state.generateSuccessor(agentIndex, action), agentIndex + 1, itera))
            return v

        def maxValue(state, agentIndex, itera):
            v = float('-inf')
            itera += 1
            for action in state.getLegalActions(agentIndex):
              v = max(v, value(state.generateSuccessor(agentIndex, action), agentIndex + 1, itera))
            return v

        # assosciate each of the legal actions with their score, and then pick the max of the scores 
        # and returning the action 
        scores = [(action, value(gameState.generateSuccessor(self.index, action), newIndex, 1)) for action in legalMoves]
        bestMove = max(scores, key = lambda t: t[1])[0]
        return bestMove

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # get number of agents 
        numAgents = gameState.getNumAgents()

        # What do we care about? We want to know which pac-man action returned 
        # the move with the best scores. Let's go ahead and get all of 
        # the actions pac-man can make ('legalMoves')
        legalMoves = gameState.getLegalActions(self.index)

        # update what will be teh agentIndex parameter for the cal to our 'value' function
        newIndex = (self.index + 1) % numAgents

        def value(state, agentIndex, alpha, beta, itera):
            # update agentIndex 
            agentIndex = agentIndex % numAgents
            
            # check if we can ~make moves~ 
            if itera == self.depth * numAgents or not state.getLegalActions(agentIndex):
              return self.evaluationFunction(state)
            if agentIndex == self.index:
              return maxValue(state, agentIndex, alpha, beta, itera)
            else:
              return minValue(state, agentIndex, alpha, beta, itera)

        def minValue(state, agentIndex, alpha, beta, itera):
            v = float('inf')
            itera += 1 
            for action in state.getLegalActions(agentIndex):
              v = min(v, value(state.generateSuccessor(agentIndex, action), agentIndex + 1, alpha, beta, itera))
              if v < alpha:
                return v
              beta = min(beta, v)
            return v

        def maxValue(state, agentIndex, alpha, beta, itera):
            v = float('-inf')
            itera += 1
            for action in state.getLegalActions(agentIndex):
              v = max(v, value(state.generateSuccessor(agentIndex, action), agentIndex + 1, alpha, beta, itera))
              if v > beta:
                return v
              alpha = max(alpha, v)
            return v

        # assosciate each of the legal actions with their score, and then pick the max of the scores 
        # and returning the action 
        scores = [(action, value(gameState.generateSuccessor(self.index, action), newIndex, float('-inf'), float('inf'), 1)) for action in legalMoves]
        bestMove = max(scores, key = lambda t: t[1])[0]
        return bestMove

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
        util.raiseNotDefined()

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

