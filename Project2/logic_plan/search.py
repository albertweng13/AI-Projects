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
    cnf = []
    maxTime = 51
    n = Directions.NORTH
    s = Directions.SOUTH
    e = Directions.EAST
    w = Directions.WEST
    DirectionsList = [n, s, e , w]
    width = problem.getWidth()+1
    height = problem.getHeight()+1
    #Starting State
    startState = problem.getStartState()
    pacmanStart = logic.PropSymbolExpr("P", startState[0], startState[1], 0)
    nonStartStates = []
    for x in range(1, width):
        for y in range(1, height):
            if (x,y) == (startState[0], startState[1]):
                continue
            else:
                nonStartStates.append(logic.PropSymbolExpr("P", x, y, 0))
            startLogic = logic.to_cnf(pacmanStart & ~(logic.associate('|', nonStartStates)))
    cnf.append(startLogic)

    goalState = problem.getGoalState()

    stateList = []
    for x in range(width+1):
        for y in range(height+1):
            if problem.isWall((x,y)):
                continue
            else:
                stateList.append((x,y))

    for time in range(maxTime):
        oneStateList = []
        for state in stateList:
            oneStateList.append(logic.PropSymbolExpr("P",state[0],state[1], time))
            legalActionList = problem.actions(state)
            illegalList = []
            for action in DirectionsList:
                if action in legalActionList:
                    nextState = problem.result(state, action)[0]
                    # state & action >> new state
                    nextLogic = (logic.PropSymbolExpr("P",state[0],state[1], time) & logic.PropSymbolExpr(action,time)) >> logic.PropSymbolExpr('P',nextState[0],nextState[1], time+1)
                    cnf.append(logic.to_cnf(nextLogic))
                else:
                    illegalList.append(action)
            for action in illegalList:
                # state >> not illegal action
                cnf.append(logic.to_cnf(logic.PropSymbolExpr('P',state[0],state[1], time) >> ~logic.PropSymbolExpr(action,time)))

        # uses oneStateList, makes sure we are not in two places at once
        oneState = exactlyOne(oneStateList)
        cnf.append((oneState))
        
        # Exactly 1 move per turn
        Dir = []
        for direction in DirectionsList:
            Dir.append(logic.PropSymbolExpr(direction, time))
        oneMove = exactlyOne(Dir)
        cnf.append(logic.to_cnf(oneMove))

        # goal state
        cnf.append(logic.PropSymbolExpr("P",goalState[0],goalState[1], time))

        #print time

        model = logic.pycoSAT(cnf)
        if model:
            path = extractActionSequence(model, DirectionsList)
            return path

        cnf.remove(logic.PropSymbolExpr("P",goalState[0],goalState[1], time))



def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    cnf = []
    maxTime = 51
    n = Directions.NORTH
    s = Directions.SOUTH
    e = Directions.EAST
    w = Directions.WEST
    DirectionsList = [n, s, e , w]
    width = problem.getWidth()+1
    height = problem.getHeight()+1
    #Starting State
    swag = problem.getStartState()
    startState = swag[0]
    #Get positions of food
    foodGrid = swag[1]
    foodPosList = []
    for x in range(width+1):
        for y in range(height+1):
            if foodGrid[x][y]:
                foodPosList.append((x,y))

    pacmanStart = logic.PropSymbolExpr("P", startState[0], startState[1], 0)
    nonStartStates = []
    for x in range(1, width):
        for y in range(1, height):
            if (x,y) == (startState[0], startState[1]):
                continue
            else:
                nonStartStates.append(logic.PropSymbolExpr("P", x, y, 0))
            startLogic = logic.to_cnf(pacmanStart & ~(logic.associate('|', nonStartStates)))
    cnf.append(startLogic)

    stateList = []
    for x in range(width+1):
        for y in range(height+1):
            if problem.isWall((x,y)):
                continue
            else:
                stateList.append((x,y))

    for time in range(maxTime):
        #print time
        oneStateList = []
        for state in stateList:
            oneStateList.append(logic.PropSymbolExpr("P",state[0],state[1], time))
            legalActionList = problem.actions((state, foodGrid))
            illegalList = []
            for action in DirectionsList:
                if action in legalActionList:
                    nextState = problem.result((state, foodGrid), action)[0][0]
                    # state & action >> new state
                    nextLogic = (logic.PropSymbolExpr("P",state[0],state[1], time) & logic.PropSymbolExpr(action,time)) >> logic.PropSymbolExpr('P',nextState[0],nextState[1], time+1)
                    cnf.append(logic.to_cnf(nextLogic))
                else:
                    illegalList.append(action)
            for action in illegalList:
                # state >> not illegal action
                cnf.append(logic.to_cnf(logic.PropSymbolExpr("P",state[0],state[1], time) >> ~logic.PropSymbolExpr(action,time)))

        # uses oneStateList, makes sure we are not in two places at once
        oneState = exactlyOne(oneStateList)
        cnf.append((oneState))
        
        # Exactly 1 move per turn
        Dir = []
        for direction in DirectionsList:
            Dir.append(logic.PropSymbolExpr(direction, time))
        oneMove = exactlyOne(Dir)
        cnf.append(logic.to_cnf(oneMove))

        # goal state (must hit each pellet once)
        foodAllEaten = []
        for food in foodPosList:
            foodOnce = []
            for alltime in range(time+1):
                foodOnce.append(logic.PropSymbolExpr('P',food[0],food[1],alltime))
            atLeastOnce = logic.associate('|', foodOnce)
            foodAllEaten.append(atLeastOnce)
        goalLogic = logic.associate('&', foodAllEaten)
        cnf.append(goalLogic)
        model = logic.pycoSAT(cnf)
        if model:
            path = extractActionSequence(model, DirectionsList)
            return path
        cnf.remove(goalLogic)
    print("you suck")
    
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
    cnf = []
    maxTime = 51
    n = Directions.NORTH
    s = Directions.SOUTH
    e = Directions.EAST
    w = Directions.WEST
    DirectionsList = [n, s, e , w]
    width = problem.getWidth()+1
    height = problem.getHeight()+1
    #Starting State
    swag = problem.getStartState()
    startState = swag[0]
    ghostStartStateList = problem.getGhostStartStates()
    #Get positions of food
    foodGrid = swag[1]
    foodPosList = []
    for x in range(width+1):
        for y in range(height+1):
            if foodGrid[x][y]:
                foodPosList.append((x,y))

    pacmanStart = logic.PropSymbolExpr("P", startState[0], startState[1], 0)
    nonStartStates = []
    for x in range(1, width):
        for y in range(1, height):
            if (x,y) == (startState[0], startState[1]):
                continue
            else:
                nonStartStates.append(logic.PropSymbolExpr("P", x, y, 0))
            startLogic = logic.to_cnf(pacmanStart & ~(logic.associate('|', nonStartStates)))
    cnf.append(startLogic)

    stateList = []
    for x in range(width+1):
        for y in range(height+1):
            if problem.isWall((x,y)):
                continue
            else:
                stateList.append((x,y))

    for time in range(maxTime):
        oneStateList = []
        for state in stateList:
            oneStateList.append(logic.PropSymbolExpr("P",state[0],state[1], time))
            legalActionList = problem.actions((state, foodGrid))
            illegalList = []
            for action in DirectionsList:
                if action in legalActionList:
                    nextState = problem.result((state, foodGrid), action)[0][0]
                    # state & action >> new state
                    nextLogic = (logic.PropSymbolExpr("P",state[0],state[1], time) & logic.PropSymbolExpr(action,time)) >> logic.PropSymbolExpr('P',nextState[0],nextState[1], time+1)
                    cnf.append(logic.to_cnf(nextLogic))
                else:
                    illegalList.append(action)
            for action in illegalList:
                # state >> not illegal action
                cnf.append(logic.to_cnf(logic.PropSymbolExpr("P",state[0],state[1], time) >> ~logic.PropSymbolExpr(action,time)))

        # uses oneStateList, makes sure we are not in two places at once
        oneState = exactlyOne(oneStateList)
        cnf.append((oneState))
        
        # Exactly 1 move per turn
        Dir = []
        for direction in DirectionsList:
            Dir.append(logic.PropSymbolExpr(direction, time))
        oneMove = exactlyOne(Dir)
        cnf.append(logic.to_cnf(oneMove))

        # goal state (must hit each pellet once)
        foodAllEaten = []
        for food in foodPosList:
            foodOnce = []
            for alltime in range(time+1):
                foodOnce.append(logic.PropSymbolExpr('P',food[0],food[1],alltime))
            atLeastOnce = logic.associate('|', foodOnce)
            foodAllEaten.append(atLeastOnce)
        goalLogic = logic.associate('&', foodAllEaten)
        cnf.append(goalLogic)

        #Pacman and Ghost not in same place
        def ghostPositionfinder(ghoststart, time):
            ghostposition = ghoststart
            x = ghoststart[0]
            y = ghoststart[1]
            East = True
            for t in range(time):
                if East == True:
                    x += 1
                    if problem.isWall((x,y)):
                        x -= 2
                        East = False
                elif East == False:
                    x -= 1
                    if problem.isWall((x,y)):
                        x += 2
                        East = True
            return (x,y)
            #logic.PropSymbolExpr("G", ghostPos[0], ghostPos[1], 0)

        for ghostStartState in ghostStartStateList:
            ghostPos = ghostStartState.getPosition()
            ghostCurrentPos = ghostPositionfinder(ghostPos, time)
            cnf.append(logic.PropSymbolExpr("G", ghostCurrentPos[0], ghostCurrentPos[1], time))

        for pos in stateList:
            plsnodie = [logic.PropSymbolExpr("P",pos[0],pos[1],time)] + [logic.PropSymbolExpr("G",pos[0],pos[1],time)]
            cnf.append(atMostOne(plsnodie))
            plsnodie = [logic.PropSymbolExpr("P",pos[0],pos[1],time)] + [logic.PropSymbolExpr("G",pos[0],pos[1],time-1)]
            cnf.append(atMostOne(plsnodie))

        model = logic.pycoSAT(cnf)
        if model:
            path = extractActionSequence(model, DirectionsList)
            return path
        cnf.remove(goalLogic)

    print("you suck")
    


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



