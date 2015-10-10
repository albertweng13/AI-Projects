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
import copy

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

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
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

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"

    solutionQueue = util.Queue()
    solutionList = []
    visited = set()
    start = problem.getStartState()
    solutionQueue.push((start, solutionList))

    while (not solutionQueue.isEmpty()):
        deQ = solutionQueue.pop()
        position = deQ[0]
        currList = deQ[1]

        if problem.isGoalState(position):
            return currList

        if (position not in visited):
            visited.add(position)
        
            for succ in problem.getSuccessors(position):
                succPos = succ[0]
                succList = succ[1]

                temp_path = list(currList)
                temp_path.append(succList)
                solutionQueue.push((succPos, temp_path))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):

    def DFLimitedS(problem, start, depth, stack, fringe):

        visited = set()
        initialPath = []
        fringe.append(start)
        stack.push((start, depth, initialPath))

        while not stack.isEmpty():

            pop = stack.pop()
            currentPosition = pop[0]
            currentDepth = pop[1]
            currentPath = pop[2]

            fringe.remove(currentPosition)

            if (problem.isGoalState(currentPosition)):
                return currentPath

            #successors =problem.getSuccessors(currentPosition)

            if currentPosition not in visited:

                if currentDepth > 0:

                    for elem in problem.getSuccessors(currentPosition):

                        succPosition = elem[0]
                        succDirection = elem[1]

                        succPath = list(currentPath)
                        succPath.append(succDirection)

                        if succPosition not in fringe:
                            fringe.append(succPosition)
                            stack.push((succPosition, currentDepth - 1, succPath))

                    visited.add(currentPosition)
        
        return []

    solutionList = []
    solutionStack = util.Stack()
    start = problem.getStartState()
    fringe = []
    depth = 0

    while (len(solutionList) == 0):
        solutionList = DFLimitedS(problem, start, depth, solutionStack, fringe)
        depth += 1
    return solutionList


def iterativeDeepeningSearchRecursive(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    #we use a DFS and increase its depth

    from game import Directions
    goalReached = []

    def DFS(state, problem, visited, stack, depth):
        
        if depth <= 0:
            return
        if problem.isGoalState(state):
            goalReached.append(1)
            return
        successors = problem.getSuccessors(state)
        for elem in reversed(successors):
            if elem[0] not in visited:
                visited.add(elem[0])
                DFS(elem[0], problem, visited, stack, depth - 1)
                if len(goalReached) != 0:
                    stack.push(elem[1])
                    return
                visited.remove(elem[0])
        return

    solutionList = []
    solutionStack = util.Stack()
    visited = set()
    
    start = problem.getStartState()
    visited.add(start)

    #trivial case: we start at goal
    if problem.isGoalState(start):
        return solutionList

    depth = 1  
    
    while (len(goalReached) == 0):

        DFS(start, problem, visited, solutionStack, depth)
        depth = depth + 1


    while not solutionStack.isEmpty():
        x = solutionStack.pop()
        solutionList.append(x)
   

    return solutionList


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    def solutionHelper(moves, position):
        #print "call help"
        build = []
        while position in moves.keys():

            move = moves[position]
            direction = move[0]
            parent = move[1]

            build.append(direction)
            position = parent

        for elem in reversed(build):
            solutionList.append(elem)

    
    solutionList = []
    solutionPrQueue = util.PriorityQueue()
    visited = set()
    moves = {}
    stepCost = 0    # stepCost = g(n) + h(n)

    start = problem.getStartState()
    visited.add(start)
    startChildren = problem.getSuccessors(start)
    position = start
    goalReached = False    #current position

    # initialize solutionQueue with start's children
    for elem in startChildren:
        position = elem[0]
        direction = elem[1]
        cost = elem[2]
        
        # heuristic takes state and problem
        stepCost = cost + heuristic(position, problem)
        
        # push ([position, direction, cost, parent], stepCost)   
        solutionPrQueue.push([position, direction, cost, start], stepCost)   

    #while solutionPrQueue.isEmpty() == False:
    while goalReached == False:
        items = solutionPrQueue.pop()
        position = items[0]
        direction = items[1]
        cost = items[2]
        parent = items[3]
        
        #print "parent"

        if position not in visited:
            visited.add(position)
            moves[position] = [direction, parent]
            #print position

            if problem.isGoalState(position):
                solutionHelper(moves, position)
                goalReached = True
                #print "CCCC"

            else:
                for elem in problem.getSuccessors(position):
                    childPosition = elem[0]
                    childDirection = elem[1]
                    childCost = elem[2]
                    accumulatedCost = cost + childCost
                    
                    #print "    " + str(childPosition) 

                    stepCost = accumulatedCost + heuristic(childPosition, problem)

                    # push ([position, direction, cost, parent], stepCost)
                    solutionPrQueue.push([childPosition, childDirection, accumulatedCost, position], stepCost)


    #print "right before return"
    return solutionList


# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
