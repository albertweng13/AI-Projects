# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import sys
from util import manhattanDistance
from game import Directions
import random, util
from searchAgents import mazeDistance
import math

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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostpositions = successorGameState.getGhostPositions()
        "*** YOUR CODE HERE ***"
        foodpositions = currentGameState.getFood().asList()
        pelletpositions = successorGameState.getCapsules()

        ghost = 0.0
        food = 0.0
        for scary in ghostpositions:
            scary = (int(scary[0]),int(scary[1]))
            newPos = (int(newPos[0]), int(newPos[1]))
            mazeDist = manhattanDistance(scary, newPos)
            if mazeDist <= 1:
                ghost = -sys.maxint -1            
        for yummy in foodpositions:
            maxfood = 0.0   
            foodmazeDist = manhattanDistance(yummy, newPos)
            #pelletmazeDist = mazeDistance(pellet, newPos, successorGameState)
            if foodmazeDist > 0:
                maxfood = ((float(1) / foodmazeDist))
            else:
                maxfood = sys.maxint
            food = max(food, maxfood)
        return food + ghost
        

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
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

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
      Your minimax agent (question 7)
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
        def choice(state, depth):
            def maxValue(state, agent, depth):
                actions = state.getLegalActions(agent)
                result = (None, None)
                maxVal = -sys.maxint - 1
                if (depth <= 0 or state.isWin() or state.isLose()):
                    leafValue = self.evaluationFunction(state)
                    result = (leafValue, None)
                    return result
                for elem in actions:
                    successor = state.generateSuccessor(agent, elem)
                    value = minValue(successor, agent + 1, depth)
                    if (value[0] > maxVal):
                        maxVal = value[0]
                        result = (value[0], elem)
                return result
            def minValue(state, agent, depth):
                actions = state.getLegalActions(agent)
                result = (None, None)
                minVal = sys.maxint
                if (depth <= 0 or state.isWin() or state.isLose()):
                    leafValue = self.evaluationFunction(state)
                    result = (leafValue, None)
                    return result
                for elem in actions:
                    successor = state.generateSuccessor(agent, elem)
                    if (agent + 1 >= state.getNumAgents()):
                        value = maxValue(successor, 0, depth - 1)
                    else:
                        value = minValue(successor, agent + 1, depth)
                    if (value[0] < minVal):
                        minVal = value[0]
                        result = (value[0], elem)
                return result
            return maxValue(state, 0, depth)
        depth = self.depth
        decision = choice(gameState, depth)
        return decision[1]



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def choice(state, depth):
            def maxValue(state, agent, depth):
                actions = state.getLegalActions(agent)
                result = (None, None)
                maxVal = -sys.maxint - 1
                if (depth <= 0 or state.isWin() or state.isLose()):
                    leafValue = self.evaluationFunction(state)
                    result = (leafValue, None)
                    return result
                for elem in actions:
                    successor = state.generateSuccessor(agent, elem)
                    value = expValue(successor, agent + 1, depth)
                    if (value[0] > maxVal):
                        maxVal = value[0]
                        result = (value[0], elem)
                return result
            def expValue(state, agent, depth):
                actions = state.getLegalActions(agent)
                result = (None, None)
                valueList = []
                moveList = []
                average = 0.0
                amount = 0.0
                if (depth <= 0 or state.isWin() or state.isLose()):
                    leafValue = self.evaluationFunction(state)
                    result = (leafValue, None)
                    return result
                for elem in actions:
                    successor = state.generateSuccessor(agent, elem)
                    if (agent + 1 >= state.getNumAgents()):
                        value = maxValue(successor, 0, depth - 1)
                    else:
                        value = expValue(successor, agent + 1, depth)
                    amount = amount + 1
                    valueList.append(value[0])
                    moveList.append(elem)
                for num in valueList:
                    if (num is not None):
                        average = average + num
                average = average / amount
                move = moveList[random.randint(0, len(moveList) - 1)]
                result = (average, move)
                return result
            return maxValue(state, 0, depth)
        depth = self.depth
        decision = choice(gameState, depth)
        return decision[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
      Sometimes our Pacman must become Super Pacman.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodpositions = currentGameState.getFood().asList()
    pelletpositions = currentGameState.getCapsules()
    result = 0.0
    
    foodDist = 1.0
    for yummy in foodpositions:
        foodDist = foodDist + manhattanDistance(newPos, yummy)
    result = result + (1.0 / foodDist)

    foodAmount = len(foodpositions)
    if (foodAmount > 0):
        result = result + (1.0 / foodAmount)

    result = result + (-1337 * len(pelletpositions))
    result = result + currentGameState.getScore()

    for scary in newGhostStates:
        ghostPos = scary.getPosition()
        ghostPos = (int(ghostPos[0]), int(ghostPos[1]))
        ghostDist = manhattanDistance(newPos, ghostPos)
        scared = scary.scaredTimer
        if (scared > 0 and ghostDist >= scared and ghostDist > 0):
            result = result + sys.maxint
        elif (ghostDist < 2):
            result = result - sys.maxint

    return result   

# Abbreviation
better = betterEvaluationFunction

