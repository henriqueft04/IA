#STUDENT NAME: Henrique Ferreira Teixeira
#STUDENT NUMBER: 114588

#DISCUSSED TPI-1 WITH: (names and numbers):
#There was some minor discussion with Gilherme Rosa 113968
#Saw a lot of documentaion on stack overflow 
#Also investigated some githubs as https://github.com/CoGian | https://github.com/apostolistselios
#Also saw some discussions about the topic on reddit

from tree_search import *
from strips import *
from blocksworld import *

class MyNode(SearchNode):

    def __init__(self,state,parent,cost, heuristic=0,action=None):
        super().__init__(state,parent)
        #ADD HERE ANY CODE YOU NEED

        self.depth = parent.depth + 1 if parent != None else 0
        self.cost = cost
        self.heuristic = heuristic

        #the action that led from the parent state to the current state
        self.action = action

    def in_parent(self,state):
         
        if self.parent == None:
            return False
        if self.parent.state == state:
            return True
        
        return self.parent.in_parent(state)

class MyTree(SearchTree):
    def __init__(self, problem, strategy='breadth', improve=False):
        super().__init__(problem, strategy)
        self.problem = problem
        self.num_solution = 0  # number of solution nodes found
        self.num_skipped = 0   # number of skipped nodes
        self.num_closed = 0    # number of closed nodes
        self.num_open = 1      # number of nodes in the queue
        self.improve = improve
        
        # Create root node
        root = MyNode(
            problem.initial,
            None,
            0,
            problem.domain.heuristic(problem.initial, problem.goal),
            None
        )
        self.open_nodes = [root]
        self.solution = None
        self.plan = []

    def search2(self):
        best_path = None
        
        while self.open_nodes:
            node = self.open_nodes.pop(0)
            self.num_open = len(self.open_nodes)

            # Check if the cost of the node is greater than the cost of the best solution
            if self.improve and self.solution and node.cost + node.heuristic >= self.solution.cost:
                self.num_skipped += 1
                continue
            
            # Check if i finally found a solution
            if self.problem.goal_test(node.state):
                self.num_solution += 1

                # Update the solution if it's better
                if self.solution is None or node.cost < self.solution.cost:
                    self.solution = node
                    # Build the plan of actions
                    actions = []
                    current = node
                    while current and current.parent:
                        if current.action:  # Make sure action exists
                            for op in self.problem.domain.actions(current.parent.state):
                                if self.problem.domain.result(current.parent.state, op) == current.state:
                                    actions.insert(0, op)
                                    break
                        current = current.parent
                    self.plan = actions  # Update the plan with the actions
                    
                    # Build the path of states

                    best_path = self.get_plan(node)

                if not self.improve:
                    return best_path
                
                continue
            
            self.num_closed += 1
            
            lnewnodes = []

            for action in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, action)
                
                if node.in_parent(newstate):
                    continue
                    
                newcost = node.cost + self.problem.domain.cost(node.state, action)

                # skip if best solution is already better
                if self.improve and self.solution and newcost >= self.solution.cost:
                    self.num_skipped += 1
                    continue
                
                # Update the heuristic for the new state
                newheuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                newnode = MyNode(
                    newstate,
                    node,
                    newcost,
                    newheuristic,
                    action  # Store the actual action object
                )
                lnewnodes.append(newnode)
            
            if self.strategy == 'depth':
                self.open_nodes = lnewnodes + self.open_nodes
            elif self.strategy == 'informeddepth':
                self.informeddepth_add_to_open(lnewnodes)
            else:
                self.add_to_open(lnewnodes)

        return best_path

    def add_to_open(self, lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes = lnewnodes + self.open_nodes
        elif self.strategy == 'A*':
            self.astar_add_to_open(lnewnodes)
        elif self.strategy == 'informeddepth':
            self.informeddepth_add_to_open(lnewnodes)
        else:
            print('Strat not implemented by me yet :)')
            
    def astar_add_to_open(self, lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda x: (x.cost + x.heuristic, x.depth, str(x.state)))

    def informeddepth_add_to_open(self, lnewnodes):
        lnewnodes.sort(key=lambda x: (x.cost + x.heuristic, str(x.state)))
        self.open_nodes = lnewnodes + self.open_nodes

    def check_admissible(self, node):
        actual_cost = node.cost
        
        current = node
        while current:
            # The heuristic at any node should not exceed
            # the actual remaining cost to the goal
            remaining_cost = actual_cost - current.cost
            if current.heuristic > remaining_cost:
                return False
            current = current.parent
        return True

    def get_plan(self, node):
        if node.parent is None:
            return []
        return self.get_plan(node.parent) + [node.action] 

class MyBlocksWorld(STRIPS):

    # h1:
    def heuristic(self, state, goal):
        """
        Heuristic function that estimates the cost to reach the goal.
        - Twice the number of blocks that must be moved once.
        - Four times the number of blocks that must be moved twice.
        """
        one_move_blocks = set()
        two_move_blocks = set()
        
        # Convert state and goal to be easier to read cause im dumb :)
        current_pos = {}  # Current position of each block
        goal_pos = {}     # Desired position of each block
        
        # Process current state
        for pred in state:
            if isinstance(pred, On):
                current_pos[pred.args[0]] = pred.args[1]
            elif isinstance(pred, Floor):
                current_pos[pred.args[0]] = 'floor'
        
        # Process goal state
        for pred in goal:
            if isinstance(pred, On):
                goal_pos[pred.args[0]] = pred.args[1]
            elif isinstance(pred, Floor):
                goal_pos[pred.args[0]] = 'floor'
        
        # Identify blocks that need to be moved once and twice
        for block in current_pos:
            if block not in goal_pos:
                continue

            current_support = current_pos[block]
            goal_support = goal_pos[block]

            # Check if this block is on the wrong support (must be moved once)
            if current_support != goal_support:
                one_move_blocks.add(block)

            # Check if the block is on the correct support but the support itself must be moved
            elif current_support == goal_support:
                # If the block below in the goal is misplaced, this block must be moved twice
                support_below = current_support
                if support_below in one_move_blocks:
                    two_move_blocks.add(block)
                    one_move_blocks.discard(block)  # A block cannot be both one-move and two-move

                # Check if there are misplaced blocks further down in the stack
                while support_below != 'floor':
                    if support_below in one_move_blocks or support_below in two_move_blocks:
                        two_move_blocks.add(block)
                        one_move_blocks.discard(block)
                        break

                    # Move to the block below in the current stack
                    support_below = current_pos.get(support_below, 'floor')

        # Calculate the heuristic value
        return len(one_move_blocks) * 2 + len(two_move_blocks) * 4