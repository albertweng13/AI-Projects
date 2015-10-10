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
    visited = set()
    queue = util.Queue()
    pathtracker = []
    start = (problem.getStartState(), pathtracker)
    queue.push(start)
    while not queue.isEmpty():
        curr = queue.pop()
        if problem.isGoalState(curr[0]):
            return curr[1]
        if curr[0] not in visited:
            visited.add(curr[0])
            for successor in problem.getSuccessors(curr[0]):
                pathtracker = []
                pathtracker = pathtracker + curr[1]
                pathtracker.append(successor[1])
                queue.push((successor[0], pathtracker))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    def DFS(problem, depth, stack, visited):
        start = problem.getStartState()
        pathtracker = []
        frontier = set()
        frontier.add(start)
        stack.push((start, depth, pathtracker))
        while not stack.isEmpty():
            curr = stack.pop()
            frontier.remove(curr[0])
            if (problem.isGoalState(curr[0])):
                return curr[2]
            if curr[0] not in visited:
                if curr[1] > 0:
                    visited.add(curr[0])
                    for successor in problem.getSuccessors(curr[0]):
                        depthcounter = curr[1]-1
                        pathtracknode = []
                        pathtracknode = pathtracknode + curr[2]
                        pathtracknode.append(successor[1])
                        if successor[0] not in frontier:
                            frontier.add(successor[0])
                            stack.push((successor[0], depthcounter, pathtracknode))

    depth = 0
    finalpath = None
    while finalpath == None :
        visited = set()
        stack = util.Stack()
        finalpath = DFS(problem, depth, stack, visited)
        depth += 1
    return finalpath

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = set()
    queue = util.PriorityQueue()
    start = problem.getStartState()
    visited.add(start)
    finalpath = []

    for successor in problem.getSuccessors(start):
        fn = successor[2] + heuristic(successor[0], problem)
        pathtracknode = []
        pathtracknode.append(successor[1])
        queue.push((successor, pathtracknode), fn)

    while not queue.isEmpty():
        current = queue.pop()
        node = current[0]
        if node[0] not in visited:
            visited.add(node[0])
            if problem.isGoalState(node[0]):
                return current[1]
            for successor in problem.getSuccessors(node[0]):
                cumulative = node[2] + successor[2]
                fn = cumulative + heuristic(successor[0], problem)
                successorA = (successor[0], successor[1], cumulative)
                pathtracknode = []
                pathtracknode = pathtracknode + current[1]
                pathtracknode.append(successor[1])
                queue.push((successorA, pathtracknode), fn)

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
