# Blocks World Implementation Documentation

## Class Documentation

### 1. SearchDomain (ABC)
Abstract base class that defines the interface for search domains.

**Methods:**
- `actions(state)`: Returns list of possible actions in given state
- `result(state, action)`: Returns resulting state after applying action
- `satisfies(state, goal)`: Tests if state satisfies goal conditions
- `cost(state, action)`: Returns cost of applying action in state
- `heuristic(state, goal)`: Returns estimated cost to reach goal

### 2. SearchProblem
Represents a concrete problem to be solved within a domain.

**Attributes:**
- `domain`: The SearchDomain instance
  - this is either the cidades or the a world of blocks
- `initial`: Initial state
- `goal`: Goal state

**Methods:**
- `goal_test(state)`: Tests if state satisfies goal conditions

### 3. MyNode (extends SearchNode)
Represents a node in the search tree.

**Attributes:**
- `state`: Current state
- `parent`: Parent node
- `depth`: Depth in search tree
- `cost`: Cost to reach this node
- `heuristic`: Heuristic value
- `action`: Action that led to this state

**Methods:**
- `in_parent(state)`: Checks if state exists in ancestor nodes

### 4. MyTree (extends SearchTree)
Implements the search tree and algorithms.

**Attributes:**
- `problem`: SearchProblem instance
- `strategy`: Search strategy ('breadth', 'depth', 'A*', 'informeddepth')
- `num_solution`: Number of solution nodes found
- `num_skipped`: Number of skipped nodes
- `num_closed`: Number of closed nodes
- `num_open`: Number of nodes in queue
- `improve`: Whether to continue searching for better solutions
- `plan`: Sequence of actions to reach goal

**Methods:**
  `search2()`: **Main search algorithm**
  1. Initialization:
   - `best_path` is initialized to `None` to store the best solution path found during the search.
   - The method continues as long as there are open nodes (`self.open_nodes`).

2. Processing Nodes:
   - The next node to be explored is taken from `open_nodes`.
   - It checks if the node's cost plus its heuristic is greater than or equal to the best solution found so far (if any), and if the `improve` flag is set. If so, it skips this node to avoid exploring suboptimal paths.

3. Goal Check:
   - If the current node's state satisfies the goal, it increments the count of solutions found (`self.num_solution`).
   - If the solution is better than the previously found solutions (lower cost), it updates the solution and constructs the path of states leading to this node.
   - If `improve` is `False`, it returns the `best_path` immediately upon finding a solution; otherwise, it continues to explore for better solutions.

4. Generating New Nodes:
   - For each action applicable in the current node's state, it computes the resulting state.
   - It checks for cycles by ensuring the new state does not exist in the path of the parent nodes.
   - If the new state's cost is less than the current best solution (when `improve` is `True`), it creates a new `MyNode` with the updated state, cost, and heuristic.
   - These new nodes are then added to the list of open nodes based on the search strategy (e.g., breadth-first, A*, etc.).

5. Return Value:
   - The method returns the `best_path` once all nodes have been processed or a suitable solution is found.


- `add_to_open(lnewnodes)`: Adds new nodes based on strategy
- `astar_add_to_open(lnewnodes)`: A* specific node addition
- `informeddepth_add_to_open(lnewnodes)`: Informed depth-first specific
- `check_admissible(node)`: Verifies heuristic admissibility
- `get_plan(node)`: Extracts action sequence from solution

### 5. Blocks World Classes

#### Predicates:
- `Floor(block)`: Block is on floor
- `On(b1, b2)`: Block b1 is on block b2
- `Free(block)`: Block has nothing on top
- `Holds(block)`: Robot holds block
- `HandFree()`: Robot hand is empty

#### Operators:
- `Stack(X,Y)`: Stack block X on Y
- `Unstack(X,Y)`: Remove block X from Y
- `Putdown(X)`: Put block X on floor
- `Pickup(X)`: Pick up block X from floor

## Search Process Flow

1. **Initialization:**
   ```
   # Create domain, initial state, and goal state
   bw = MyBlocksWorld()
   inThe implementation tracks several metrics:
- `num_open`: Nodes in queue
- `num_solution`: Solutions found
- `num_skipped`: Nodes skipped
- `num_closed`: Nodes explored

These metrics help evaluate search efficiency and strategy effectiveness.
2. **Search Execution:**
   - Tree performs search using `search2()`
   - Nodes are expanded based on strategy
   - Solution path is built when goal is reached

3. **Solution Generation:**
   ```
   t.search2()  # Performs search
   print(t.plan)  # Shows sequence of actions
   ```

## Search Strategies

### 1. Breadth-First Search
- Explores all nodes at current depth before moving deeper
- Guarantees optimal solution for uniform costs
- Implementation: Adds new nodes to end of queue

### 2. Depth-First Search
- Explores deepest node in current path first
- Memory efficient but not optimal
- Implementation: Adds new nodes to front of queue

### 3. A* Search
- Uses heuristic to guide search
- Optimal when heuristic is admissible
- Implementation: Orders nodes by f(n) = g(n) + h(n)
  - g(n): Cost to reach node
  - h(n): Estimated cost to goal

### 4. Informed Depth-First Search
- Depth-first variant using heuristic
- More informed than basic depth-first
- Implementation: Orders children by heuristic before adding to front

## Heuristic Function

### Explanation of the Heuristic Function

This heuristic function estimates the cost of reaching a goal state from a given state in a Blocks World problem. It calculates the heuristic based on how many blocks need to be moved to achieve the desired configuration. The function distinguishes between blocks that require different numbers of moves, assigning higher costs to blocks that need to be moved more times.

#### Overview
- **One-Move Blocks**: These are blocks that need to be moved once to reach their correct position.
- **Two-Move Blocks**: These are blocks that need to be moved twice due to dependencies on other blocks below them that are misplaced.
- The heuristic value is calculated as:
  - Twice the number of blocks that need to be moved once.
  - Four times the number of blocks that need to be moved twice.

#### Step-by-Step Breakdown

1. **Initialize Sets and State Mappings**:
   - `one_move_blocks`: Holds blocks that need a single move to be correctly positioned.
   - `two_move_blocks`: Holds blocks that will need two moves.
   - `current_pos`: A dictionary mapping each block to what it is currently resting on (e.g., another block or the floor).
   - `goal_pos`: A dictionary mapping each block to its desired resting place as per the goal state.

2. **Convert State Representations**:
   - Loop through each predicate in `state` and `goal`:
     - If a block is `On` another block, add it to `current_pos` or `goal_pos` with the respective block it is on.
     - If a block is on the `Floor`, set its value as `'floor'`.

3. **Identify Blocks That Need to Be Moved**:
   - Loop through each block in `current_pos`:
     - If the block is not present in `goal_pos`, skip it (the goal does not care about its position).
     - Otherwise, determine if it needs to be moved:
       - **One Move**: If the block's current support (the block or floor it is on) is different from its goal support, add it to `one_move_blocks`.
       - **Two Moves**: If the block is on the correct support, check if the support itself is misplaced. This can create a dependency:
         - If the block it rests on is a one-move block, this block becomes a two-move block.
         - Traverse further down the stack using `while` to ensure that if any block below is misplaced, this block is correctly categorized as needing two moves.

4. **Calculate the Heuristic Value**:
   - Compute the total estimated cost using the formula:
     - `len(one_move_blocks) * 2`: Each block that needs one move adds 2 to the heuristic.
     - `len(two_move_blocks) * 4`: Each block that needs two moves adds 4 to the heuristic.
   - Return this value as the estimated cost to reach the goal state.
