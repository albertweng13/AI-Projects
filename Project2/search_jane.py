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
import game

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
    return ~logic.associate('&', [~expr for expr in expressions])

def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    temp = []
    tempList = [~atLeastOne(expressions)]
    for a in expressions: 
        for b in expressions:
            if a == b:
                temp.append(b)
            else:
                temp.append(~b)
        temp = logic.associate('&', temp)
        tempList.append(temp)
        temp = []

    tempList = logic.associate('|', tempList)
    return tempList

def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return atMostOne(expressions) & atLeastOne(expressions)

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
    plan = []
    i, count = 0, 0
    while count < len(model):
        for action in actions:
            if logic.PropSymbolExpr(action, i) not in model.keys():
                continue
            if (model[logic.PropSymbolExpr(action, i)]):
                plan.append(action)
                i += 1
                break
        count += 1
    return plan   

def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    cnf = []

    # Initial State
    start = problem.getStartState()
    startX = start[0]
    startY = start[1]
    cnf.append(logic.to_cnf(logic.PropSymbolExpr("P", startX, startY, 0)))
    width = problem.getWidth()
    height = problem.getHeight()

    # Goal State
    (goalX, goalY) = problem.getGoalState() 

    # Sucessor Axioms
    t_max = 50
    all_actions = ['North', 'South', 'East', 'West']

    for t in range(t_max+1):
        state_exprs = []
        for x in range(1,width+1):
            for y in range(1, height+1):
                curr_state = (x,y)
                curr_state_expr = logic.PropSymbolExpr("P", x, y, t)
                state_exprs.append(curr_state_expr)
                
                action_logic = []
                
                """
                if x-1 >=0 and game.Directions.EAST in problem.actions((x-1, y)):
                    action_logic.append(logic.PropSymbolExpr("P", x-1, y, t-1) & logic.PropSymbolExpr("East", t-1))
                if x+1 <= width and game.Directions.WEST in problem.actions((x+1, y)):
                    action_logic.append(logic.PropSymbolExpr("P", x+1, y, t-1) & logic.PropSymbolExpr("West", t-1))
                if y-1 >= 0 and game.Directions.NORTH in problem.actions((x, y-1)):
                    action_logic.append(logic.PropSymbolExpr("P", x, y-1, t-1) & logic.PropSymbolExpr("North", t-1))
                if y+1 <= height and game.Directions.SOUTH in problem.actions((x, y+1)):
                    action_logic.append(logic.PropSymbolExpr("P", x, y+1, t-1) & logic.PropSymbolExpr("South", t-1))
                """
                legal_actions = problem.actions(curr_state)

                for action in legal_actions:
                    state_action = curr_state_expr & logic.PropSymbolExpr(action, t)
                    if action == game.Directions.EAST:
                        next_state = logic.PropSymbolExpr("P", x+1, y, t+1)
                    elif action == game.Directions.WEST:
                        next_state = logic.PropSymbolExpr("P", x-1, y, t+1)
                    elif action == game.Directions.NORTH:
                        next_state = logic.PropSymbolExpr("P", x, y+1, t+1)
                    else:
                        next_state = logic.PropSymbolExpr("P", x, y-1, t+1)
                    cnf.append(logic.to_cnf(state_action % next_state))

                #cnf.append(logic.to_cnf(exactlyOne(action_logic)))
        
                
        cnf.append(logic.to_cnf(exactlyOne(state_exprs))) # exactly one state is true at one time
        # exactly one action is taken at one time
        cnf.append(logic.to_cnf(exactlyOne([logic.PropSymbolExpr("North", t), logic.PropSymbolExpr("South", t), logic.PropSymbolExpr("East", t), logic.PropSymbolExpr("West", t)])))
        
        cnf.append(logic.to_cnf(logic.PropSymbolExpr("P", goalX, goalY, t))) 
        model = logic.pycoSAT(cnf)
        print(model)
        if model:
            return extractActionSequence(model, all_actions)
        cnf.remove(logic.PropSymbolExpr("P", goalX, goalY, t))
 
    return extractActionSequence(logic.pycoSAT(cnf), all_actions) 

def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    cnf = []

    # Initial State
    start_pos, foodGrid = problem.getStartState()

    tempList = []
    for i in xrange(0, problem.getWidth()):
        for j in xrange(0, problem.getHeight()):
            if i != startX:
                if j != startY:
                    tempList.append(logic.PropSymbolExpr("P", i, j, 0))
    cnf.append(logic.to_cnf(logic.PropSymbolExpr("P", startX, startY, 0) & ~(logic.associate('|', tempList))))

    # A* to find path to eat all food
    start = problem.getStartState()
    fringe = util.PriorityQueue()
    fringe.push(start_pos, 0)

    visited = set()
    tempList = []
    path = []
    totalTime = 0 

    while not fringe.isEmpty():
        coord, t = fringe.pop()
        if coord not in visited:
            if problem.terminalTest(coord):
                totalTime = t
                break
            visited.add(coord)
            for action in problem.actions(coord):
                nextCoord, cost = problem.result(coord, action)
                if nextCoord not in visited:
                    tempList.append((nextCoord, t + 1, [coord], [action]))
                fringe.push((nextCoord, t + 1))


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



