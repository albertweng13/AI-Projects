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
from util import *
from game import Directions
import time

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
    result = expressions[0]
    for expr in expressions:
        if result is None:
            result = None
        else:
            result = result | expr
    return result


def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    
    result = expressions[0] | ~expressions[0]
    for expr1 in expressions:
        for expr2 in expressions:
            if expr1 == expr2:
                continue
            else:
                result = result & (~expr1 | ~expr2)
    return result


def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    
    return atLeastOne(expressions) & atMostOne(expressions)


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

def generate_initial_statements(problem, time):
    nonStartStates = []
    startState = problem.getStartState()
    pacmanStart = logic.PropSymbolExpr("P", startState[0], startState[1], time)
    index_x = 1
    for x in range(1, problem.getWidth()+1):
        for y in range(1, problem.getHeight()+1):
            if (x,y) == (startState[0], startState[1]):
                continue
            else:
                nonStartStates.append(logic.PropSymbolExpr("P", x, y, time))
    return pacmanStart & ~(logic.associate('|', nonStartStates))

def transition_expression(problem, current, successor):
    previous_position_expr = logic.PropSymbolExpr("P",current[0][0], current[0][1], current[2])
    current_position_expr = logic.PropSymbolExpr("P",successor[0][0],successor[0][1],current[2]+1)
    move_expr = logic.PropSymbolExpr(successor[1], int(current[2]))
    combine = (current_position_expr % (previous_position_expr & move_expr))
    return combine

def goal_expression(problem, current, successor):
    current_position_expr = logic.PropSymbolExpr("P",successor[0][0],successor[0][1],current[2]+1)   
    return current_position_expr


def generateFromDirections(current, elem):
    if elem == Directions.NORTH:
        return ((current[0][0],current[0][1]+1), "North")
    if elem == Directions.SOUTH:
        return ((current[0][0],current[0][1]-1), "South")
    if elem == Directions.EAST:
        return ((current[0][0]+1,current[0][1]), "East")
    if elem == Directions.WEST:
        return ((current[0][0]-1,current[0][1]), "West")

def findPreviousDirection(current):
    previous = current[1]
    current = current[0]
    x_coord = current[0] - previous[0]
    if x_coord == 0:
        y_coord = current[1] - previous[1]
        if y_coord == 0:
            return "NONE!"
        if y_coord > 0:
            return Directions.SOUTH
        else:
            return Directions.NORTH
    if x_coord > 0:
        return Directions.WEST
    else: 
        return Directions.EAST

def generateOneMove(count):
    north = logic.PropSymbolExpr("North", count)
    south = logic.PropSymbolExpr("South", count)
    east = logic.PropSymbolExpr("East", count)
    west = logic.PropSymbolExpr("West", count)
    returned = [north, south, east, west]
    return returned

def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"

    cnf = []
    time = 0
    cnf.append(logic.to_cnf(generate_initial_statements(problem, time)))

    current = problem.getStartState()
    queue = Queue()
    queue.push(((current[0],current[1]), (current[0],current[1]), time))

    """ ((current_position), (previous_position), time) """

    goal_state = None
    goal_states = []
    end_time = 0
    goal_time_found = (False,0)

    while not queue.isEmpty():
        current = queue.pop()
        actions = problem.actions(current[0])
        previous_action = findPreviousDirection(current)
        if goal_time_found[0] == True:
            if current[2] > goal_time_found[1]:
                break
        for elem in actions:   
            if elem != previous_action:
                successor = generateFromDirections(current, elem)
                x = transition_expression(problem, current, successor)
                if not problem.terminalTest(successor[0]):
                    cnf.append(logic.to_cnf(x))
                    queue.push((successor[0], current[0], current[2]+1))
                else:
                    goal_state = successor
                    goal_time_found = (True,current[2])
                    goal_states.append(x)
                end_time = current[2]

    cnf.append(logic.to_cnf(logic.associate('|', goal_states)))

    """ solve cnf """

    end_time += 1
    cnf.append(logic.to_cnf(logic.PropSymbolExpr("P", goal_state[0][0], goal_state[0][1], end_time)))

    for elem in range(0, end_time):
        cnf.append(logic.to_cnf(exactlyOne(generateOneMove(elem))))

    n = Directions.NORTH
    s = Directions.SOUTH
    e = Directions.EAST
    w = Directions.WEST

    return extractActionSequence(logic.pycoSAT(cnf), [n,s,e,w])

    util.raiseNotDefined()


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



