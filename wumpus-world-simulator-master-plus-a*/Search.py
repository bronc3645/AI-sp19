# Search.py
#
# A* search for wumpus world navigation in Python.

import sys
import Action
import Orientation

class SearchState:
	
	def __init__(self, location, orientation, depth, parent, action):
		self.location = location
		self.orientation = orientation
		self.depth = depth
		self.parent = parent
		self.action = action
		self.heuristic = 0
		self.cost = 0
		
	def __eq__(self, other):
		if ((self.location == other.location) and (self.orientation == other.orientation)):
			return True
		else:
			return False

class SearchEngine:
	
	def __init__(self):
		self.frontier = []
		self.explored = []
		self.safeLocations = []
		self.nodeCount = 0
		
	# These are the main methods:
	# - AddSafeLocation: Tell the search about locations you think are safe; the search only considers safe locations to move through.
	# - RemoveSafeLocation: If you determine a safe location is in fact not safe, then you can remove it from consideration.
	# - FindPath: The main method to call to use search to find a sequence of actions leading from start to goal only through safe locations.
	
	def AddSafeLocation (self, x, y):
		if (not self.SafeLocation(x,y)):
			self.safeLocations.append([x,y])
	
	def RemoveSafeLocation(self, x, y):
		if (self.SafeLocation(x,y)):
			self.safeLocations.remove([x,y])

	# Use search to find sequence of actions from start location/orientation to goal location/orientation.
	# Returns empty action list if not path found (or already at the goal).
	def FindPath (self, startLocation, startOrientation, goalLocation, goalOrientation):
		initialState = SearchState (startLocation, startOrientation, 0, None, Action.CLIMB)
		goalState = SearchState (goalLocation, goalOrientation, 0, None, Action.CLIMB)
		finalState = self.Search (initialState, goalState)
		actionList = []
		# If solution found, retain actions
		if (finalState):
			tmpState = finalState
			while (tmpState.parent):
				actionList.insert(0, tmpState.action)
				tmpState = tmpState.parent
		self.Clear() # deletes entire search tree, including initialState and finalState
		return actionList

	# Main search algorithm. Returns goal state from which you can follow the parent pointers
	# to get the actions in the solution path.
	def Search (self,initialState, goalState):
		self.Clear()
		self.nodeCount = 0
		print("Calling search...")
		finalState = self.AStarSearch (initialState, goalState)
		if (finalState):
			print("Solution found.")
		else:
			print("No solution found.")
		print(str(self.nodeCount) + " nodes generated.\n")
		sys.stdout.flush()
		return finalState

	# Clear the explored and frontier lists
	def Clear (self):
		self.frontier = []
		self.explored = []

	# A* search = uniform cost search using cost = (depth + heuristic)
	def AStarSearch (self, initialState, goalState):
		initialState.heuristic = self.CityBlockDistance(initialState.location, goalState.location)
		initialState.cost = initialState.depth + initialState.heuristic
		self.frontier.append(initialState)
		while (self.frontier):
			state = self.frontier.pop(0)
			if (self.GoalTest (state, goalState)):
				return state
			self.explored.append (state)
			# Try each action: GOFORWARD, TURNLEFT, TURNRIGHT
			for action in [Action.GOFORWARD, Action.TURNLEFT, Action.TURNRIGHT]:
				childState = self.GetChildState (state, action)
				if (childState):
					self.nodeCount += 1
					childState.heuristic = self.CityBlockDistance (childState.location, goalState.location)
					childState.cost = childState.depth + childState.heuristic
					if (not self.Visited(childState)):
						self.AddToFrontierInOrder(childState)
					else:
						# Check if childState on frontier, but has lower cost
						# Could do this more efficiently by remembering it from Visited call, but good enough
						for index,tmpState in enumerate(self.frontier):
							if (tmpState == childState):
								if (tmpState.cost > childState.cost):
									# Child state is better, so replace frontier state with child state
									self.frontier[index] = childState
								
		return None # failure

	# True if state location same as goal location, ignoring orientation.
	def GoalTest (self, state, goalState):
		if (state == goalState):
			return True
		else:
			return False

	# Returns new state after applying action to given state. For GOFORWARD, only
	# works if adjacent location exists and is safe. If not, return None.
	def GetChildState (self, state, action):
		childState = None
		if (action == Action.TURNLEFT):
			childState = SearchState (state.location, state.orientation, state.depth + 1, state, Action.TURNLEFT)
			if (state.orientation == Orientation.UP):
				childState.orientation = Orientation.LEFT
			if (state.orientation == Orientation.DOWN):
				childState.orientation = Orientation.RIGHT
			if (state.orientation == Orientation.LEFT):
				childState.orientation = Orientation.DOWN
			if (state.orientation == Orientation.RIGHT):
				childState.orientation = Orientation.UP
		if (action == Action.TURNRIGHT):
			childState = SearchState (state.location, state.orientation, state.depth + 1, state, Action.TURNRIGHT)
			if (state.orientation == Orientation.UP):
				childState.orientation = Orientation.RIGHT
			if (state.orientation == Orientation.DOWN):
				childState.orientation = Orientation.LEFT
			if (state.orientation == Orientation.LEFT):
				childState.orientation = Orientation.UP
			if (state.orientation == Orientation.RIGHT):
				childState.orientation = Orientation.DOWN
		if (action == Action.GOFORWARD):
			x = state.location[0]
			y = state.location[1]
			if (state.orientation == Orientation.UP):
				y += 1
			if (state.orientation == Orientation.DOWN):
				y -= 1
			if (state.orientation == Orientation.LEFT):
				x -= 1
			if (state.orientation == Orientation.RIGHT):
				x += 1
			if (self.SafeLocation(x,y)):
				childState = SearchState ([x,y], state.orientation, state.depth + 1, state, Action.GOFORWARD)
		return childState

	def CityBlockDistance (self, location1, location2):
		return (abs (location1[0] - location2[0]) + abs (location1[1] - location2[1]))

	def SafeLocation (self, x, y):
		if ([x,y] in self.safeLocations):
			return True
		else:
			return False
		
	# Return true if state on explored or frontier lists
	def Visited (self, state):
		if (state in self.explored):
			return True
		if (state in self.frontier):
			return True
		return False

	# Insert state into frontier, keeping it in order by state->cost
	# Among equal-cost states, the new state is put first so that A* performs
	# a DFS (more efficient than BFS) among states with equal costs.
	def AddToFrontierInOrder (self, state):
		inserted = False
		for index,tmpState in enumerate(self.frontier):
			if (tmpState.cost >= state.cost):
				self.frontier.insert(index, state)
				inserted = True
				break
		if (not inserted):
			self.frontier.append(state)

