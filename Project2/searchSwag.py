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
    cnf = expressions[0]
    for expr in expressions:
        cnf = cnf | expr
    return cnf
    util.raiseNotDefined()


def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    cnf = expressions[0] | ~expressions[0]
    for expr_a in expressions:
        for expr_b in expressions:
            if expr_a != expr_b:
                cnf = cnf & (~expr_a | ~expr_b)
    return cnf
    util.raiseNotDefined()


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
    i = 0
    path = []
    while True:
        for key in model.keys():
            keyStr = str(key)
            string = "[" + str(i) + "]"
            if string in keyStr and model[key] is True:
                path.append(keyStr[:keyStr.index('[')])
        i+=1
        if(len(path) != i):
            break
    return path

def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    que = util.Queue()
    visited = []
    cnfList = []
    startState = problem.getStartState()
    goalState = problem.getGoalState()
    Directions = ['North', 'South', 'East', 'West']
    count=0

    que.push((startState,0))
    while not que.isEmpty():
        pop = que.pop()
        currentState = pop[0]
        currentTime = pop[1]
        count += 1
        if goalState == currentState:
            visited.append(currentState)
            count = currentTime
            break
        if currentState not in visited:
            actions = problem.actions(currentState)
            for action in actions:
                nextState = problem.result(currentState, action)[0]
                que.push((nextState, currentTime+1))
                expression = (logic.PropSymbolExpr('P',currentState[0],currentState[1], currentTime) & logic.PropSymbolExpr(action,currentTime)) >> logic.PropSymbolExpr('P',nextState[0],nextState[1], currentTime+1)
                # state + action > new state
                cnfList.append(logic.to_cnf(expression))
            visited.append(currentState)

    # not in two places at once
    for time in xrange(count+1):
        cnfList.append(exactlyOne([logic.PropSymbolExpr('P',state[0],state[1], time) for state in visited]))
    
    # must make one move each turn
    for time in xrange(count):
        cnfList.append(exactlyOne([logic.PropSymbolExpr(action,time) for action in Directions]))

    # no going back on path
    for state in visited:
        cnfList.append(atMostOne([logic.PropSymbolExpr('P',state[0],state[1],time) for time in xrange(count+1)]))

    # start at startState
    cnfList.append(logic.PropSymbolExpr('P',startState[0],startState[1], 0))

    # goal state
    cnfList.append(logic.PropSymbolExpr('P',goalState[0],goalState[1], count))
    if(count > 10):
        cnfList.append(~logic.PropSymbolExpr('West',0))

    # no illegal moves
    for state in visited:
        for action in list(set(Directions)-set(problem.actions(state))):
            for time in xrange(count+1):
                # state > not action
                cnfList.append(logic.to_cnf(logic.PropSymbolExpr('P',state[0],state[1], time) >> ~logic.PropSymbolExpr(action,time)))

    model = logic.pycoSAT(cnfList)

    path = extractActionSequence(model, Directions)
    return path


def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    Directions = ['North', 'South', 'East', 'West']
    width = problem.getWidth()
    height = problem.getHeight()
    foodGrid = startState[1]

    allStates = []
    exploredSet = []
    foodSpots = []
    que = util.Queue()
    que.push(startState)
    while not que.isEmpty():
        currentState = que.pop()
        if currentState[0] not in exploredSet:
            allStates.append(currentState)
            exploredSet.append(currentState[0])
            actions = problem.actions(currentState)
            for action in actions:
                nextState = problem.result(currentState, action)[0]
                que.push(nextState)
            if foodGrid[currentState[0][0]][currentState[0][1]]:
                foodSpots.append(currentState[0])

    max_time = 51

    for time_limit in xrange(len(foodSpots),max_time):
        cnfList = []
        for currentState in allStates:
            actions = problem.actions(currentState)
            for action in actions:
                for time in xrange(time_limit):
                    nextState = problem.result(currentState, action)[0]
                    expression = (logic.PropSymbolExpr('P',currentState[0][0],currentState[0][1], time) & logic.PropSymbolExpr(action,time)) >> logic.PropSymbolExpr('P',nextState[0][0],nextState[0][1], time+1)
                    # state + action > new state
                    cnfList.append(logic.to_cnf(expression))
            for action in list(set(Directions)-set(problem.actions(currentState))):
                for time in xrange(time_limit):
                    # state > not action
                    cnfList.append(logic.to_cnf(logic.PropSymbolExpr('P',currentState[0][0],currentState[0][1], time) >> ~logic.PropSymbolExpr(action,time)))

        # start at startState
        cnfList.append(logic.PropSymbolExpr('P',startState[0][0],startState[0][1], 0))

        # must make one move each turn
        for time in xrange(time_limit):
            cnfList.append(exactlyOne([logic.PropSymbolExpr(action,time) for action in Directions]))

        # not in two places at once
        for time in xrange(time_limit):
            cnfList.append(exactlyOne([logic.PropSymbolExpr('P',state[0][0],state[0][1], time) for state in allStates]))

        # hit at least each pellet once
        for food in foodSpots:
            cnfList.append(atLeastOne([logic.PropSymbolExpr('P',food[0],food[1],time) for time in xrange(time_limit)]))

        model = logic.pycoSAT(cnfList)

        if model:
            path = extractActionSequence(model, Directions)
            return path


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
    startState = problem.getStartState()
    Directions = ['North', 'South', 'East', 'West']
    width = problem.getWidth()
    height = problem.getHeight()
    foodGrid = startState[1]

    allStates = []
    exploredSet = []
    foodSpots = []
    que = util.Queue()
    que.push(startState)
    while not que.isEmpty():
        currentState = que.pop()
        if currentState[0] not in exploredSet:
            allStates.append(currentState)
            exploredSet.append(currentState[0])
            actions = problem.actions(currentState)
            for action in actions:
                nextState = problem.result(currentState, action)[0]
                que.push(nextState)
            if foodGrid[currentState[0][0]][currentState[0][1]]:
                foodSpots.append(currentState[0])

    max_time = 51

    for time_limit in xrange(len(foodSpots),max_time):
        cnfList = []
        for currentState in allStates:
            actions = problem.actions(currentState)
            for action in actions:
                for time in xrange(time_limit):
                    nextState = problem.result(currentState, action)[0]
                    expression = (logic.PropSymbolExpr('P',currentState[0][0],currentState[0][1], time) & logic.PropSymbolExpr(action,time)) >> logic.PropSymbolExpr('P',nextState[0][0],nextState[0][1], time+1)
                    # state + action > new state
                    cnfList.append(logic.to_cnf(expression))
            for action in list(set(Directions)-set(problem.actions(currentState))):
                for time in xrange(time_limit):
                    # state > not action
                    cnfList.append(logic.to_cnf(logic.PropSymbolExpr('P',currentState[0][0],currentState[0][1], time) >> ~logic.PropSymbolExpr(action,time)))

        # pacman start at startState
        cnfList.append(logic.PropSymbolExpr('P',startState[0][0],startState[0][1], 0))
        
        # must make one move each turn
        for time in xrange(time_limit):
            cnfList.append(exactlyOne([logic.PropSymbolExpr(action,time) for action in Directions]))

        # not in two places at once
        for time in xrange(time_limit):
            cnfList.append(exactlyOne([logic.PropSymbolExpr('P',state[0][0],state[0][1], time) for state in allStates]))

        # hit at least each pellet once
        for food in foodSpots:
            cnfList.append(atLeastOne([logic.PropSymbolExpr('P',food[0],food[1],time) for time in xrange(time_limit)]))



        for index in xrange(len(problem.getGhostStartStates())):
            #ghost start state
            ghostStartState = problem.getGhostStartStates()[index]
            ghostPos = ghostStartState.getPosition()
            cnfList.append(logic.PropSymbolExpr('G' + str(index),ghostPos[0],ghostPos[1],0))


            # if no wall east, go east
            if not problem.isWall((ghostPos[0]+1, ghostPos[1])):
                cnfList.append(logic.PropSymbolExpr('G' + str(index),ghostPos[0]+1,ghostPos[1], 1))
                # print "East"
            else:
                cnfList.append(logic.PropSymbolExpr('G' + str(index),ghostPos[0]-1,ghostPos[1], 1))
                # print "West"


            # get all ghost positions
            allGhostPos = []
            ghostPosY = ghostPos[1]
            for w in xrange(width+1):
                pos = (w,ghostPosY)
                if not problem.isWall((w,ghostPosY)):
                    allGhostPos.append(pos)


            # ghost actions
            for time in xrange(1, time_limit):
                for pos in allGhostPos:
                    toEast = (pos[0]+1, pos[1])
                    toWest = (pos[0]-1, pos[1])
                    if problem.isWall(toWest):
                        cnfList.append(logic.to_cnf(logic.PropSymbolExpr('G' + str(index),pos[0],pos[1], time) >> logic.PropSymbolExpr('G' + str(index),pos[0]+1,pos[1], time+1)))
                    # cant go east
                    if problem.isWall(toEast):
                        cnfList.append(logic.to_cnf(logic.PropSymbolExpr('G' + str(index),pos[0],pos[1], time) >> logic.PropSymbolExpr('G' + str(index),pos[0]-1,pos[1], time+1)))
                    # can go either
                    elif not problem.isWall(toWest) and not problem.isWall(toEast):
                        expr_and = logic.PropSymbolExpr('G' + str(index),pos[0]-1,pos[1], time-1) & logic.PropSymbolExpr('G' + str(index),pos[0],pos[1], time)
                        expr_implies = expr_and >> logic.PropSymbolExpr('G' + str(index),pos[0]+1,pos[1], time+1)
                        cnfList.append(logic.to_cnf(expr_implies))
                        expr_and = logic.PropSymbolExpr('G' + str(index),pos[0]+1,pos[1], time-1) & logic.PropSymbolExpr('G' + str(index),pos[0],pos[1], time)
                        expr_implies = expr_and >> logic.PropSymbolExpr('G' + str(index),pos[0]-1,pos[1], time+1)
                        cnfList.append(logic.to_cnf(expr_implies))


            # pacman and ghost cant be in same state
            # print allGhostPos
            for time in xrange(time_limit):
                for pos in allGhostPos:
                    # temp = [logic.PropSymbolExpr('P',pos[0],pos[1],time)]
                    # temp += [logic.PropSymbolExpr('G' + str(index),pos[0],pos[1],time+1)]
                    # cnfList.append(atMostOne(temp))

                    temp = [logic.PropSymbolExpr('P',pos[0],pos[1],time+1)]
                    temp += [logic.PropSymbolExpr('G' + str(index),pos[0],pos[1],time)]
                    cnfList.append(atMostOne(temp))

                    temp = [logic.PropSymbolExpr('P',pos[0],pos[1],time)]
                    temp += [logic.PropSymbolExpr('G' + str(index),pos[0],pos[1],time)]
                    cnfList.append(atMostOne(temp))

        # ghost not in two places at once
        # for time in xrange(time_limit):
            # cnfList.append(exactlyOne([logic.PropSymbolExpr('G' + str(index),pos[0],pos[1], time) for pos in allGhostPos]))


        model = logic.pycoSAT(cnfList)

        if model:
            # for i in cnfList:
                # print i
            path = extractActionSequence(model, Directions)
            return path



# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)