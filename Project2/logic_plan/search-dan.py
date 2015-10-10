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
    expr = expressions[0]
    for i in range(1, len(expressions)):
        expr = expr | expressions[i]
    return expr


def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    expr = ~expressions[0] | ~ expressions[1]
    for i in range(0, len(expressions)):
        for j in range(i+1, len(expressions)):
            if i != 0 and j != 1:
                temp = ~expressions[i] | ~expressions[j]
                expr = expr & temp  
    return expr



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
    positives = []
    solution = []
    for action in model:
        if model[action]:
            positives.append(action)
    for i in range(len(positives)):
        for value in positives:
            value = logic.PropSymbolExpr.parseExpr(value)
            if value[1] == str(i):
                solution.append(value[0])
    return solution


def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    
    start = problem.getStartState()
    goal = problem.getGoalState()
    allActions = ['North', 'South', 'East', 'West']
    expr = []
    states = []
    for i in range(1, problem.getWidth() + 1):
        for j in range(1, problem.getHeight() + 1):
            if not problem.isWall((i,j)):
                states.append((i,j))
    
    startingConstraint = logic.PropSymbolExpr("P", start[0], start[1], 0)
    for state in states:
        if state != start:
            startingConstraint = startingConstraint & ~logic.PropSymbolExpr("P", state[0], state[1], 0)
    expr.append(startingConstraint)


    for t in range(1, 50):
        allStateSymbols = []
        sentences = []
        allActionSymbols = []
        goalConstraint = logic.PropSymbolExpr("P", goal[0], goal[1], t)
        
        for action in allActions:
            actionSymbol = logic.PropSymbolExpr(action, t)
            allStateSymbols.append(actionSymbol)
        oneAction = exactlyOne(allStateSymbols)
        sentences.append(logic.to_cnf(oneAction))

        for state in states:
            stateSymbol = logic.PropSymbolExpr("P", state[0], state[1], t)
            allStateSymbols.append(stateSymbol)
            actions = problem.actions(state)
            for action in allActions:
                if action in actions:
                    actionSymbol = logic.PropSymbolExpr(action, t)
                    result = problem.result(state, action)
                    resultSymbol = logic.PropSymbolExpr("P", result[0][0], result[0][1], t + 1)
                    constraint = (stateSymbol & actionSymbol) >> resultSymbol
                    sentences.append(logic.to_cnf(constraint))
                else:
                    actionSymbol = logic.PropSymbolExpr(action, t)
                    constraint = stateSymbol >> ~actionSymbol
                    sentences.append(logic.to_cnf(constraint))
            if state != goal:
                goalConstraint = goalConstraint & ~stateSymbol


        oneState = exactlyOne(allStateSymbols)
        sentences.append(logic.to_cnf(oneState))
        sentences.append(logic.to_cnf(goalConstraint))
        expr += sentences

        model = logic.pycoSAT(expr)
        if model != False:
            print model
            return extractActionSequence(model, allActions)
        else:
            expr.remove(logic.to_cnf(goalConstraint))














    # actions = problem.actions(start)
    # firstActions = []
    # firstSuccessors = []
    # secondActions = []
    # secondSuccessors = []
    # for action in actions:
    #     logicAction = logic.PropSymbolExpr(action, 1)
    #     firstActions.append(logicAction)
    #     successor = problem.result(start, action)
    #     resultConstraint = logic.Expr('<=>', logicAction, logic.PropSymbolExpr("P", successor[0][0], successor[0][1], 1))
    #     firstSuccessors.append(logic.to_cnf(resultConstraint))

    #     for action in problem.actions(successor[0]):
    #         logicalAction = logic.PropSymbolExpr(action, 2)
    #         secondActions.append(logicalAction)
    #         result = problem.result(successor[0], action)
    #         resultingConstraint = logic.Expr('<=>', logicalAction, logic.PropSymbolExpr("P", result[0][0], result[0][1], 2))
    #         secondSuccessors.append(logic.to_cnf(resultingConstraint))


    # expr.append(logic.to_cnf(exactlyOne(firstActions)) & logic.to_cnf(exactlyOne(firstSuccessors)))
    # expr.append(logic.to_cnf(exactlyOne(secondActions)) & logic.to_cnf(exactlyOne(secondSuccessors)))

    # #use xor somewhere

    # goalConstraint = logic.PropSymbolExpr("P", goal[0], goal[1], 2)
    # for state in states:
    #     if state != start:
    #         goalConstraint = goalConstraint & ~logic.PropSymbolExpr("P", state[0], state[1], 2)
    # expr.append(goalConstraint)
    # for t in range(1, 50):
    #     actions = [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]
    #     temp = []
    #     for action in actions:
    #         temp.append(logic.PropSymbolExpr(action, t))
    #     expr.append(exactlyOne(temp))
    #     propStates = []
    #     for state in states:
    #         propStates.append(logic.PropSymbolExpr("P", state[0],state[1], t))
    #         prevStates = []
    #         actions = problem.actions(state)
    #         for action in actions:
    #             resultingState = problem.result(state, action)
    #             resultingExpr = logic.PropSymbolExpr("P", resultingState[0][0], resultingState[0][1], t+1)
    #             expr.append(logic.to_cnf((logic.PropSymbolExpr("P", state[0], state[1], t) & logic.PropSymbolExpr(action, t)) >> resultingExpr))
    #             prevExpr = logic.PropSymbolExpr("P", resultingState[0][0], resultingState[0][1], t)
    #             prevStates.append(prevExpr & logic.PropSymbolExpr(game.Directions.REVERSE[action], t))
    #         expr.append(logic.to_cnf(logic.PropSymbolExpr("P", state[0], state[1], t+1) >> atLeastOne(prevStates)))
    #     expr.append(logic.PropSymbolExpr("P", goal[0], goal[1], t))
    #     expr.append(logic.to_cnf(exactlyOne(propStates)))
    #     model = logic.pycoSAT(expr)

    #     if model != False:
    #         print model
    #         return extractActionSequence(model, actions)
    #     else:
    #         expr.remove(logic.PropSymbolExpr("P", goal[0], goal[1], t))


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



