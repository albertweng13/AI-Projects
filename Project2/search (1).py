# search.py
# ---------
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


# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import logic
from game import Directions

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

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostSearchProblem)
        """
        util.raiseNotDefined()

    def terminalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionSearchProblem
        """
        util.raiseNotDefined()

    def result(self, state, action):
        """
        Given a state and an action, returns resulting state and step cost, which is
        the incremental cost of moving to that successor.
        Returns (next_state, cost)
        """
        util.raiseNotDefined()

    def actions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        util.raiseNotDefined()

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        util.raiseNotDefined()

    def isWall(self, position):
        """
        Return true if position (x,y) is a wall. Returns false otherwise.
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


def atLeastOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at least one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    result = None
    for expr in expressions:
        if result is None:
            result = expr
        else:
            result = result | expr
    return result


def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    result = None
    exprList = expressions
    while (len(exprList) > 0):
        expr = exprList.pop(0)
        if result is None:
            first = exprList[0]
            result = (~expr | ~first)
            for comp in exprList:
                if (comp != first):
                    result = result & (~expr | ~comp)
        else:
            for comp in exprList:
                result = result & (~expr | ~comp)
    return result


def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    result = None
    exprList = expressions
    while (len(exprList) > 0):
        expr = exprList.pop(0)
        if result is None:
            first = exprList[0]
            result = (~expr | ~first) & (expr | first)
            for comp in exprList:
                if (comp != first):
                    result = result & (~expr | ~comp) & (expr | first)
        else:
            for comp in exprList:
                result = result & (~expr | ~comp) & (expr | first)
    return result


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    dictList = model.keys()
    actionList = []
    plan = []
    for item in dictList:
        symbol = logic.PropSymbolExpr.parseExpr(item)
        if (symbol[0] in actions):
            if (model[item] is True):
                actionList.append(symbol)
    actionList.sort(key=lambda action: int(action[1]))
    for direction in actionList:
        plan.append(direction[0])
    return plan


def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    time = 0
    cnf = []
    startState = problem.getStartState()
    pacmanStart = logic.PropSymbolExpr("P", startState[0], startState[1], 0)
    nonStartStates = []
    paths = []
    
    index_x = 0
    index_y = 0
    while (index_x < problem.getWidth()):
        while (index_y < problem.getHeight()):
            if index_x == startState[0] & index_y == startState[1]:
                continue
            else:
                nonStartStates.append(logic.PropSymbolExpr("P", index_x, index_y, 0))
                index_x += 1
                index_y += 1
    start = pacmanStart & ~(logic.associate('|', nonStartStates))
    cnf.append(logic.to_cnf(start))

    def find_T(problem, start):
        visited = set()
        queue = util.Queue()
        queue.push((start, 0))
        while not queue.isEmpty():
            current = queue.pop()
            if problem.terminalTest(current[0]):
                return current[1]
            if current[0] not in visited:
                visited.add(current[0])
                actionList = problem.actions(current[0])
                successorList = []
                for action in actionList:
                    successorList.append(problem.result(current[0], action))
                for successor in successorList:
                    queue.push((successor[0], current[1] + 1))

    time = find_T(problem, startState)

    def build_Path(problem, state, result, time, T, paths):
        if (time >= T):
            if (problem.terminalTest(state)):
                paths.append(logic.to_cnf(result))
            else:
                result = ~result
                paths.append(logic.to_cnf(result))
        else:
            actionList = problem.actions(state)
            for action in actionList:
                nextState = problem.result(state, action)[0]
                build_Path(problem, nextState, result & logic.PropSymbolExpr("P", nextState[0], nextState[1], time + 1) & logic.PropSymbolExpr(action, time), time + 1, T, paths)

    build_Path(problem, startState, pacmanStart, 0, time, paths)
    cnf = cnf + paths
    print(cnf)
    model = logic.pycoSAT(cnf)
    return extractActionSequence(model, [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST])




def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostSearchProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



