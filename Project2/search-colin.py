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


    return logic.associate('|', expressions)

def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"

    final_expression = ~atLeastOne(expressions)

    temp_list = []
    for elem in expressions:
        for elem2 in expressions:
            if elem == elem2:
                temp_list.append(elem2)
            else:
                temp_list.append(~elem2)
        final_expression = final_expression | logic.associate('&', temp_list)
        temp_list = []
    return final_expression



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
    final_sequence = []

    t = 0
    count = 0
    while count < len(model):
        for elem in actions:
            move = logic.PropSymbolExpr(elem, t)
            if (move not in model.keys()):
                continue
            if (model[move]):
                final_sequence.append(elem)
                t += 1
                break
        count += 1


    return final_sequence


def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"

    cnf = []
    t = 0
    start = problem.getStartState()

    # First need initial state. Pacman is at start state and not at any other state.

    pac_initial = logic.PropSymbolExpr("P", start[0], start[1], t)
    initial_expression = pac_initial

    width = problem.getWidth()
    height = problem.getHeight()
    temp_list = []

    for i in range(0, width):
        for j in range(0, height):
            if (i, j) == (start[0], start[1]):
                continue
            else:
                temp_list.append(logic.PropSymbolExpr("P", i, j, t))

    initial_expression = initial_expression & ~(logic.associate('|', temp_list))
    cnf.append(logic.to_cnf(initial_expression))

    t += 1

    # Finds T where T is the minimum time required to find a solution. 

    queue = util.Queue()
    queue.push((start, 0))
    visited = set()

    fuck_you = []

    final_time = 0

    while queue.isEmpty() != True:
        elem = queue.pop()
        if (elem[0] in visited):
            continue
        if (problem.terminalTest(elem[0])):
            final_time = elem[1]
            break
        actions = problem.actions(elem[0])
        visited.add(elem[0])
        for action in actions:
            time = elem[1]
            next = problem.result(elem[0], action)
            next_state = next[0]
            if (next[0] not in visited):
                fuck_you.append((next[0], elem[1] + 1, [elem[0]], [action]))
            queue.push((next[0], elem[1] + 1))

    # We need valid successor axioms.

    goal = problem.getGoalState()
    pac_final = logic.PropSymbolExpr("P", goal[0], goal[1], final_time)
    cnf.append(pac_final)

    for elem in fuck_you:
        position = elem[0]
        time = elem[1]
        parent = elem[2]
        direction = elem[3]
        fuck_you.remove(elem)
        new_list = []
        for elem2 in fuck_you:
            if (position == elem2[0]) & (time == elem2[1]) & (elem != elem2):
                fuck_you.remove(elem2)
                parent = parent + elem2[2]
                direction = direction + elem2[3]
        fuck_you.append((position, time, parent, direction))
        
    # Generate our successor axioms

    if_and_only_if = []

    for elem in fuck_you:
        successor_space = logic.PropSymbolExpr("P", elem[0][0], elem[0][1], elem[1])
        for i in range(len(elem[2])):
            parent = logic.PropSymbolExpr("P", elem[2][i][0], elem[2][i][1], elem[1] - 1)
            direction = logic.PropSymbolExpr(elem[3][i], elem[1] - 1)
            combine = parent & direction
            if_and_only_if.append(combine)
        parentals = logic.associate('|', if_and_only_if)
        successor_axiom = logic.to_cnf((~successor_space | parentals) & (~parentals | successor_space))
        if_and_only_if = []

        cnf.append(successor_axiom)
        
    # Ensure we make only one action at at time.

    count = 0
    while count < final_time:
        north = logic.PropSymbolExpr("North", count)
        south = logic.PropSymbolExpr("South", count)
        east = logic.PropSymbolExpr("East", count)
        west = logic.PropSymbolExpr("West", count)
        at_one = [north, south, east, west]
        cnf.append(logic.to_cnf(exactlyOne(at_one)))
        count += 1

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    model = logic.pycoSAT(cnf)
    return extractActionSequence(model, [n, s, e, w])


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



