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
    Directions = ['North', 'South', 'East', 'West']
    cnf = []
    finalTime=0
    startState = problem.getStartState()

    # Start at startState
    cnf.append(logic.PropSymbolExpr('P', startState[0], startState[1], finalTime))
    #I have no idea why you can't go west initially but it doesnt work without it

    #successor axioms, use BFS
    q = util.Queue()
    q.push((startState,0))
    visited = []
    while not q.isEmpty():
        current = q.pop()
        if problem.terminalTest(current[0]):
            visited.append(current[0])
            finalTime = current[1]
            break
        if current[0] in visited:
            continue
        else:
            visited.append(current[0])
            actionList = []
            actionList = problem.actions(current[0])
            successorList = []
            for action in actionList:
                nextState = problem.result(current[0], action)[0]
                successorList.append((nextState, action))
            for successor in successorList:
                q.push((successor[0], current[1]+1))
                successorlogic = (logic.PropSymbolExpr("P", current[0][0], current[0][1], current[1]) & logic.PropSymbolExpr(successor[1],current[1])) >> logic.PropSymbolExpr('P',successor[0][0],successor[0][1], current[1]+1)
                # current state + current action >> next state
                cnf.append(logic.to_cnf(successorlogic))

    # Goal at Goal state
    goalState = problem.getGoalState()
    cnf.append(logic.PropSymbolExpr('P',goalState[0],goalState[1], finalTime))

    # One Place per time, One move per time
    for time in range(finalTime+1):
        oneplaceList = []
        oneturnList = []

        for state in visited:
            oneplaceList.append(logic.PropSymbolExpr('P', state[0], state[1], time))
        for action in Directions:
            oneturnList.append(logic.PropSymbolExpr(action,time))

        oneplaceLogic = exactlyOne(oneplaceList)
        oneturnLogic = exactlyOne(oneturnList)

        cnf.append(oneplaceLogic)
        cnf.append(oneturnLogic)

    # No backtracking
    for state in visited:
        backtrackingList = []
        for time in range(finalTime+1):
            backtrackingList.append(logic.PropSymbolExpr('P', state[0], state[1], time))
        backtrackingLogic = atMostOne(backtrackingList)
        cnf.append(backtrackingLogic)

    # No Illegal moves (each state >> no illegal actions)
    for state in visited:
        illegalList = []
        for illegalmove in Directions:
            if illegalmove in problem.actions(state):
                continue
            else:
                illegalList.append(illegalmove)

        for time in range(finalTime+1):
            for action in illegalList:
                # state > not action
                cnf.append(logic.to_cnf(logic.PropSymbolExpr('P',state[0],state[1], time) >> ~logic.PropSymbolExpr(action,time)))

    model = logic.pycoSAT(cnf)

    if model:
        return extractActionSequence(model, Directions)


    """time = 0
    cnf = []
    startState = problem.getStartState()
    pacmanStart = logic.PropSymbolExpr("P", startState[0], startState[1], 0)
    nonStartStates = []
    index_x = 1
    while (index_x <= problem.getWidth()):
        index_y = 1
        while (index_y <= problem.getHeight()):
            if index_x == startState[0] & index_y == startState[1]:
                index_y += 1
                continue
            else:
                nonStartStates.append(logic.PropSymbolExpr("P", index_x, index_y, 0))
                index_y += 1
        index_x += 1
    start = pacmanStart & ~(logic.associate('|', nonStartStates))
    cnf.append(logic.to_cnf(start))

    goaltime = paths[0][1]
    #cnf.append(logic.to_cnf(pathlogic))
    goalState = problem.getGoalState()
    goal = logic.PropSymbolExpr("P", goalState[0], goalState[1], goaltime)
    cnf.append(goal)

    finalTime = 0
    while finalTime < goaltime:
        north = logic.PropSymbolExpr("North", finalTime)
        south = logic.PropSymbolExpr("South", finalTime)
        east = logic.PropSymbolExpr("East", finalTime)
        west = logic.PropSymbolExpr("West", finalTime)
        at_one = [north, south, east, west]
        cnf.append(logic.to_cnf(exactlyOne(at_one)))
        finalTime += 1

    
    def find_pathlogic(problem, start, paths, pacmanStart):
        visited = set()
        queue = util.Queue()
        time = 0
        startlogic = [pacmanStart]
        queue.push((start, startlogic, time))
        while not queue.isEmpty():
            current = queue.pop()
            if current[0] in visited:
                continue
            if problem.terminalTest(current[0]):
                paths.append(((current[1]), current[2]))
                break
            visited.add(current[0])
            actionList = problem.actions(current[0])
            successorList = []
            for action in actionList:
                successor = problem.result(current[0], action)
                successorList.append((successor[0], action))
            for successor in successorList:
                nexttime = current[2] + 1
                action = successor[1]
                nextState = successor[0]
                pushlogic = current[1]
                pushlogic.append(logic.PropSymbolExpr("P", nextState[0], nextState[1], nexttime) & logic.PropSymbolExpr(action, current[2]))
                #listofactions = ["North", "South", "East", "West"]
                #if action in listofactions:
                #    listofactions.remove(action)
                #for elem in listofactions:
                #    pushlogic = pushlogic & ~logic.PropSymbolExpr(elem, current[2])
                queue.push((nextState, pushlogic, nexttime))

    paths = []
    find_pathlogic(problem, startState, paths, pacmanStart)
    pathlogic = paths[0][0]

    goaltime = paths[0][1]
    #cnf.append(logic.to_cnf(pathlogic))
    goalState = problem.getGoalState()
    goal = logic.PropSymbolExpr("P", goalState[0], goalState[1], goaltime)
    cnf.append(goal)

    #if and only if
    print (pathlogic)
    swag = goal
    while len(pathlogic) != 0:
        temp = pathlogic[-1]
        pathlogic.remove(pathlogic[-1])
        #print (temp)
        swag = logic.to_cnf((~swag | temp) & (~temp | swag))

    print (swag)

    #1moveperturn
    model = logic.pycoSAT(cnf)
    return extractActionSequence(model, [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST])
    """



def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    """

    Directions = ['North', 'South', 'East', 'West']
    cnf = []
    finalTime=0
    startState = problem.getStartState()
    foodGrid = startStateandGrid[1]
    maxtime = 50

    # Start at startState
    cnf.append(logic.PropSymbolExpr('P', startState[0], startState[1], finalTime))
    #I have no idea why you can't go west initially but it doesnt work without it
    cnf.append(~logic.PropSymbolExpr('West',0))

    #successor axioms, use BFS
    q = util.Queue()
    q.push((startState, 0))
    visited = []
    timer = 0
    while not q.isEmpty() and timer <= maxtime:
        current = q.pop()
        timer += 1
        if current[0] in visited:
            continue
        else:
            visited.append(current[0])
            actionList = []
            actionList = problem.actions(current[0])
            successorList = []
            for action in actionList:
                nextState = problem.result(current[0], action)[0]
                successorList.append((nextState, action))
            for successor in successorList:
                q.push((successor[0], current[1]+1))
                successorlogic = (logic.PropSymbolExpr("P", current[0][0], current[0][1], current[1]) & logic.PropSymbolExpr(successor[1],current[1])) >> logic.PropSymbolExpr('P',successor[0][0],successor[0][1], current[1]+1)
                # current state + current action >> next state
                cnf.append(logic.to_cnf(successorlogic))

    # Goal at Goal state
    goalState = problem.getGoalState()
    cnf.append(logic.PropSymbolExpr('P',goalState[0],goalState[1], finalTime))

    # One Place per time, One move per time
    for time in range(finalTime+1):
        oneplaceList = []
        oneturnList = []

        for state in visited:
            oneplaceList.append(logic.PropSymbolExpr('P', state[0], state[1], time))
        for action in Directions:
            oneturnList.append(logic.PropSymbolExpr(action,time))

        oneplaceLogic = exactlyOne(oneplaceList)
        oneturnLogic = exactlyOne(oneturnList)

        cnf.append(oneplaceLogic)
        cnf.append(oneturnLogic)

    # No backtracking
    for state in visited:
        backtrackingList = []
        for time in range(finalTime+1):
            backtrackingList.append(logic.PropSymbolExpr('P', state[0], state[1], time))
        backtrackingLogic = atMostOne(backtrackingList)
        cnf.append(backtrackingLogic)

    # No Illegal moves (each state >> no illegal actions)
    for state in visited:
        illegalList = []
        for illegalmove in Directions:
            if illegalmove in problem.actions(state):
                continue
            else:
                illegalList.append(illegalmove)

        for time in range(finalTime+1):
            for action in illegalList:
                # state > not action
                cnf.append(logic.to_cnf(logic.PropSymbolExpr('P',state[0],state[1], time) >> ~logic.PropSymbolExpr(action,time)))

    # hit at least each pellet once
    foodSpots = foodGrid.asList
    for food in foodSpots:
        cnfList.append(atLeastOne([logic.PropSymbolExpr('P',food[0],food[1],time) for time in xrange(time_limit)]))

    model = logic.pycoSAT(cnf)

    if model:
        return extractActionSequence(model, Directions)
    """


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



