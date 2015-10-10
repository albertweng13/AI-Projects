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
    start_expr = logic.PropSymbolExpr("P", startX, startY, 0)
    width = problem.getWidth()
    height = problem.getHeight()
    temp_list = []
    
    for i in range(1, width + 1):
        for j in range(1, height + 1):
            if (i, j) == (start[0], start[1]):
                continue
            else:
                temp_list.append(logic.PropSymbolExpr("P", i, j, 0))

    start_expr = start_expr & ~(logic.associate('|', temp_list))
    cnf.append(logic.to_cnf(start_expr))
    # print start_expr

    # Goal State
    (goalX, goalY) = problem.getGoalState() 

    # Sucessor Axioms
    t_max = 50
    all_actions = ['North', 'South', 'East', 'West']
    cnf.append(logic.to_cnf(exactlyOne([logic.PropSymbolExpr("North", 0), logic.PropSymbolExpr("South", 0), logic.PropSymbolExpr("East", 0), logic.PropSymbolExpr("West", 0)])))

    """
    for i in range(1, width+1):
        for j in range(1, height+1):
            for action in problem.actions(i,j):
    """
    # print "We about to enter the loop of hell."

    for t in range(1, t_max+1):
        state_exprs = []
        # print t
        for x in range(1,width+1):
            for y in range(1, height+1):
                curr_state = (x,y)
                curr_state_expr = logic.PropSymbolExpr("P", x, y, t)
                #state_exprs.append(curr_state_expr)
                
                # action axiom = logic.to_cnf(curr_state_expr % successor_ax(curr_state_expr))
                action_logic = []

                legal_actions = problem.actions(curr_state)

                for action in legal_actions:
                    #state_action = curr_state_expr & logic.PropSymbolExpr(action, t)
                    state_action = curr_state_expr
                    if action == game.Directions.EAST:
                        next_state = logic.PropSymbolExpr("P", x+1, y, t-1)
                        take_action = logic.PropSymbolExpr(game.Directions.WEST, t-1)
                    elif action == game.Directions.WEST:
                        next_state = logic.PropSymbolExpr("P", x-1, y, t-1)
                        take_action = logic.PropSymbolExpr(game.Directions.EAST, t-1)
                    elif action == game.Directions.NORTH:
                        next_state = logic.PropSymbolExpr("P", x, y+1, t-1)
                        take_action = logic.PropSymbolExpr(game.Directions.SOUTH, t-1)
                    else:
                        next_state = logic.PropSymbolExpr("P", x, y-1, t-1)
                        take_action = logic.PropSymbolExpr(game.Directions.NORTH, t-1)
                    #print state_action
                    #print (next_state & take_action)
                    state_exprs.append((state_action, (next_state & take_action)))
                    #cnf.append(logic.to_cnf(state_action % (next_state & take_action)))

                #cnf.append(logic.to_cnf(exactlyOne(action_logic)))
        #print state_exprs
        dictionary = {}
        # print dictionary
        for elem in state_exprs:
            if elem[0] not in dictionary.keys():
                dictionary[elem[0]] = [elem[1],]
            if elem[0] in dictionary.keys():
                # dictionary[elem[0]] = dictionary[elem[0]].append(elem[1])
                dictionary[elem[0]].append(elem[1])

            # state_exprs.append((position, new_tuple))
        #print
        #print state_exprs

        # print dictionary
        for key in dictionary.keys():
            val = dictionary[key]
            
            parents = logic.associate('|', val)
            # print key
            # print parents
            cnf.append(logic.to_cnf(key % parents))

                
        #cnf.append(logic.to_cnf(exactlyOne(state_exprs))) # exactly one state is true at one time
        # exactly one action is taken at one time
        cnf.append(logic.to_cnf(exactlyOne([logic.PropSymbolExpr("North", t), logic.PropSymbolExpr("South", t), logic.PropSymbolExpr("East", t), logic.PropSymbolExpr("West", t)])))
        
        cnf.append(logic.to_cnf(logic.PropSymbolExpr("P", goalX, goalY, t))) 
        model = logic.pycoSAT(cnf)
        #print(model)
        if model:
            return extractActionSequence(model, all_actions)
        cnf.remove(logic.PropSymbolExpr("P", goalX, goalY, t))
 
    return extractActionSequence(logic.pycoSAT(cnf), all_actions) 

#def successor_ax(expr):
    

def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    
    cnf = []
    t = 0
    start = problem.getStartState()
    start_pos = start[0]
    # First need initial state. Pacman is at start state and not at any other state.
    pac_initial = logic.PropSymbolExpr("P", start_pos[0], start_pos[1], t)
    initial_expression = pac_initial
    width = problem.getWidth()
    height = problem.getHeight()
    temp_list = []

    for i in range(1, width + 1):
        for j in range(1, height + 1):
            if (i, j) == (start_pos[0], start_pos[1]):
                continue
            else:
                temp_list.append(logic.PropSymbolExpr("P", i, j, t))
    initial_expression = initial_expression & ~(logic.associate('|', temp_list))
    # print initial_expression
    cnf.append(logic.to_cnf(initial_expression))
    t += 1

    #-------------------------------------------------------------------------------
    # TRIVIAL



    fuck_you = []
    final_list = []


    queue = util.Queue()
    queue.push((start, 0, final_list)) # Start is position and foodGrid
    visited = set()

    count = 0
    while count < 51:
        north = logic.PropSymbolExpr("North", count)
        south = logic.PropSymbolExpr("South", count)
        east = logic.PropSymbolExpr("East", count)
        west = logic.PropSymbolExpr("West", count)
        at_one = [north, south, east, west]
        cnf.append(logic.to_cnf(exactlyOne(at_one)))
        count += 1

    final_time = 0

    list_of_lists = {}

    # ELEM[0] - state (x,y) and foodgrid
    # ELEM[1] - time
    # ELEM[2] - parents
    while queue.isEmpty() != True:
        elem = queue.pop()
        if (elem[0] in visited):
            continue
        if (problem.terminalTest(elem[0])):
            # print "We hit the terminal test"
            final_time = elem[1]
            # print final_time
            get_here = logic.PropSymbolExpr("P", elem[0][0][0], elem[0][0][1], final_time)
            # print get_here
            cnf.append(get_here)
            list_of_lists[(elem[0], elem[1])] = temp_path
            #fuck_you = elem[2][:]
            #break
        if (elem[1] == 51):
            break
        actions = problem.actions(elem[0])
        visited.add(elem[0]) #assuming no backtracking
        for action in actions:
            time = elem[1]
            next = problem.result(elem[0], action)
            temp_path = []
            temp_path = elem[2][:]
            temp_path.append((next[0][0], elem[1] + 1, [(elem[0][0], elem[0][1].asList())], [action], next[0][1].asList()))
            # list_of_lists[elem[0]] = temp_path
            #if (next[0] not in visited):
                #fuck_you.append((next[0][0], elem[1] + 1, [(elem[0][0], elem[0][1].asList())], [action], next[0][1].asList()))
                #print (next[0][0], elem[1] + 1, [(elem[0][0], elem[0][1].asList())], [action], next[0][1].asList())
                #print (next[0][0], elem[1] + 1, elem[0][0], action)
            queue.push((next[0], elem[1] + 1, temp_path))



    food_list = start[1].asList()

    for elem in food_list:
        food_symbol = logic.PropSymbolExpr("F", elem[0], elem[1])
        entailment = []
        for i in range(0, final_time + 1):
            pos_symbol = logic.PropSymbolExpr("P", elem[0], elem[1], i)
            entailment.append(pos_symbol)
        all_positions = logic.associate('|', entailment)

        #print food_symbol
        #print all_positions

        cnf.append(logic.to_cnf(food_symbol % all_positions))
        entailment = []

    """food_final = []
    for elem in food_list:
        food_final.append(logic.PropSymbolExpr("F", elem[0], elem[1]))

    final_states = logic.associate('&', food_final)
    #print final_states
    cnf.append(final_states)"""
    temp_cnf = []
    temp_cnf = cnf[:]


    for elem in list_of_lists.keys():
        fuck_you = list_of_lists[elem][:]
        print len(list_of_lists.keys())
        print fuck_you
        print "We should get the length"
        print len(fuck_you)

        for elem in fuck_you:
            print elem
            position = elem[0]
            time = elem[1]
            parent = elem[2]
            direction = elem[3]
            foods = elem[4] # added this.
            fuck_you.remove(elem)
            for elem2 in fuck_you:
                if (position == elem2[0]) & (time == elem2[1]) & (foods == elem2[4]) & (elem != elem2):
                # if (position == elem2[0]) & (time == elem2[1]) & (elem != elem2):
                    fuck_you.remove(elem2)
                    parent = parent + elem2[2]
                    direction = direction + elem2[3]
            fuck_you.append((position, time, parent, direction, foods))


        if_and_only_if = []
        final_append = []



        for elem in fuck_you:
            successor_space = logic.PropSymbolExpr("P", elem[0][0], elem[0][1], elem[1])
            for i in range(len(elem[2])):
                parent = logic.PropSymbolExpr("P", elem[2][i][0][0], elem[2][i][0][1], elem[1] - 1)
                direction = logic.PropSymbolExpr(elem[3][i], elem[1] - 1)
                combine = parent & direction
                if_and_only_if.append(combine)
            parentals = logic.associate('|', if_and_only_if)
            # print successor_space
            # print parentals
            successor_axiom = logic.to_cnf((~successor_space | parentals) & (~parentals | successor_space))
            if_and_only_if = []

            cnf.append(successor_axiom)

        print "How many times do we get here?"
        if logic.pycoSAT(cnf) != False:
            print "We go here."
            break
        else:
            print "Were not screwed"
            cnf = temp_cnf[:]




    """count = 0
    while count < final_time:
        north = logic.PropSymbolExpr("North", count)
        south = logic.PropSymbolExpr("South", count)
        east = logic.PropSymbolExpr("East", count)
        west = logic.PropSymbolExpr("West", count)
        at_one = [north, south, east, west]
        cnf.append(logic.to_cnf(exactlyOne(at_one)))
        count += 1"""

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    model = logic.pycoSAT(cnf)
    #for elem in model.keys():
     #   print elem
      #  print model[elem]
    return extractActionSequence(model, [n, s, e, w])
    # Encode in logic symbol, the x location, the y location, 
    #                           time, number of pellets left

    # Decrement the food when it is hit and delete from the list
    # food.asList() gives a list of the tuples

    # start is of the form ((x, y), food_grid) 
    # Encoding the goal state is tricky. Since we can be wherever.


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



