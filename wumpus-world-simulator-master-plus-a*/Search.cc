// Search.cc
//
// A* search for wumpus world navigation.

#include <iostream>
#include <list>
#include <stdlib.h>
#include "Search.h"

using namespace std;


// ----- SearchState methods

bool SearchState::operator== (const SearchState& state)
{
	if ((location.X == state.location.X) && (location.Y == state.location.Y) &&
		(orientation == state.orientation))
	{
		return true;
	}
	return false;
}


// ----- SearchEngine methods

// Use search to find sequence of actions from start location/orientation to goal location/orientation.
// Returns empty action list if not path found (or already at the goal).
list<Action> SearchEngine::FindPath (Location startLocation, Orientation startOrientation, Location goalLocation, Orientation goalOrientation)
{
	SearchState* initialState = new SearchState (startLocation, startOrientation, 0, NULL, CLIMB);
	SearchState* goalState = new SearchState (goalLocation, goalOrientation, 0, NULL, CLIMB);
	SearchState* finalState = Search (initialState, goalState);
	list<Action> actionList;
	// If solution found, retain actions
	if (finalState != NULL)
	{
		SearchState* tmpState = finalState;
		while (tmpState->parent != NULL)
		{
			actionList.push_front(tmpState->action);
			tmpState = tmpState->parent;
		}
	}
	Clear(); // deletes entire search tree, including initialState and finalState
	delete goalState;
	return actionList;
}

// Add given location to safeLocations list, if new
void SearchEngine::AddSafeLocation (int x, int y)
{
	if (! SafeLocation(x,y))
	{
		Location location;
		location.X = x;
		location.Y = y;
		safeLocations.push_back (location);
		//cout << "Added safe location (" << x << "," << y << ")\n";
	}
}

// Remove given location from safeLocations list
void SearchEngine::RemoveSafeLocation (int x, int y)
{
	Location location;
	location.X = x;
	location.Y = y;
	list<Location>::iterator itr = findLocation (safeLocations.begin(), safeLocations.end(), location);
	if (itr != safeLocations.end())
	{
		safeLocations.erase(itr);
		//cout << "Removed safe location (" << x << "," << y << ")\n";
	}
}

// Main search algorithm. Returns goal state from which you can follow the parent pointers
// to get the actions in the solution path.
SearchState* SearchEngine::Search (SearchState* initialState, SearchState* goalState)
{
	Clear();
	nodeCount = 0;
	cout << "Calling search...\n";
	SearchState* finalState = AStarSearch (initialState, goalState);
	if (finalState == NULL) {
		cout << "No solution found.\n";
	} else {
		cout << "Solution found.\n";
	}
	cout << nodeCount << " nodes generated.\n\n";
	return finalState;
}

// Clear the explored and frontier lists
void SearchEngine::Clear ()
{
	SearchState* tmpState;
	list<SearchState*>::iterator itr;
	for (itr = explored.begin(); itr != explored.end(); itr++)
	{
		tmpState = *itr;
		delete tmpState;
	}
	for (itr = frontier.begin(); itr != frontier.end(); itr++)
	{
		tmpState = *itr;
		delete tmpState;
	}
	frontier.clear();
	explored.clear();
}

// A* search = uniform cost search using cost = (depth + heuristic)
SearchState* SearchEngine::AStarSearch (SearchState* initialState, SearchState* goalState)
{
	SearchState* state;
	SearchState* childState;
	SearchState* tmpState;
	list<SearchState*>::iterator itr;

	initialState->heuristic = CityBlockDistance (initialState->location, goalState->location);
	initialState->cost = initialState->depth + initialState->heuristic;
	frontier.push_back (initialState);

	while (! frontier.empty())
	{
		state = frontier.front();
		frontier.pop_front();
		if (GoalTest (state, goalState))
		{
			return state;
		}
		explored.push_back (state);
		// Try each action: GOFORWARD=0, TURNLEFT=1, TURNRIGHT=2
		for (int action = 0; action < 3; action++)
		{
			childState = GetChildState (state, (Action) action);
			if (childState != NULL)
			{
				nodeCount++;
				childState->heuristic = CityBlockDistance (childState->location, goalState->location);
				childState->cost = childState->depth + childState->heuristic;
				if (! Visited (childState))
				{
					AddToFrontierInOrder (childState);
				} else {
					// Check if childState on frontier, but has lower cost
					// Could do the more efficiently by remembering it from Visited call, but good enough
					for (itr = frontier.begin(); itr != frontier.end(); itr++)
					{
						tmpState = *itr;
						if (*tmpState == *childState)
						{
							if (tmpState->cost > childState->cost)
							{
								// Child state is better, so replace frontier state with child state
								frontier.insert (itr, childState);
								childState = *itr;
								frontier.erase (itr);
								break;
							}
						}
					}
					delete childState;
				}
			}
		}
	}
	return NULL; // failure
}

// True if state location same as goal location, ignoring orientation.
bool SearchEngine::GoalTest (SearchState* state, SearchState* goalState)
{
	if (*state == *goalState)
		return true;
	else return false;
}

// Returns new state after applying action to given state. For GOFORWARD, only
// works if adjacent location exists and is safe. If not, return NULL.
SearchState* SearchEngine::GetChildState (SearchState* state, Action action)
{
	int x, y;
	SearchState* childState = NULL;
	Location newLocation;

	if (action == TURNLEFT)
	{
		childState = new SearchState (state->location, state->orientation, state->depth + 1, state, TURNLEFT);
		switch (state->orientation)
		{
			case UP: childState->orientation = LEFT; break;
			case DOWN: childState->orientation = RIGHT; break;
			case LEFT: childState->orientation = DOWN; break;
			case RIGHT: childState->orientation = UP; break;
		}
	}

	if (action == TURNRIGHT)
	{
		childState = new SearchState (state->location, state->orientation, state->depth + 1, state, TURNRIGHT);
		switch (state->orientation)
		{
			case UP: childState->orientation = RIGHT; break;
			case DOWN: childState->orientation = LEFT; break;
			case LEFT: childState->orientation = UP; break;
			case RIGHT: childState->orientation = DOWN; break;
		}
	}

	if (action == GOFORWARD)
	{
		x = state->location.X;
		y = state->location.Y;
		switch (state->orientation)
		{
			case UP: y++; break;
			case DOWN: y--; break;
			case LEFT: x--; break;
			case RIGHT: x++; break;
		}
		if (SafeLocation(x,y))
		{
			newLocation.X = x;
			newLocation.Y = y;
			childState = new SearchState (newLocation, state->orientation, state->depth + 1, state, GOFORWARD);
		}
	}
	return childState;
}

int SearchEngine::CityBlockDistance (Location& location1, Location& location2)
{
	return (abs (location1.X - location2.X) + abs (location1.Y - location2.Y));
}

bool SearchEngine::SafeLocation (int x, int y)
{
	Location location;
	location.X = x;
	location.Y = y;
	if (findLocation (safeLocations.begin(), safeLocations.end(), location) != safeLocations.end())
		return true;
	else return false;
}

// Return true if state on explored or frontier lists
bool SearchEngine::Visited (SearchState* state)
{
	SearchState* tmpState;
	list<SearchState*>::iterator itr;
	for (itr = explored.begin(); itr != explored.end(); itr++)
	{
		tmpState = *itr;
		if (*tmpState == *state)
			return true;
	}
	for (itr = frontier.begin(); itr != frontier.end(); itr++)
	{
		tmpState = *itr;
		if (*tmpState == *state)
			return true;
	}
	return false;
}

// Insert state into frontier, keeping it in order by state->cost
// Among equal-cost states, the new state is put first so that A* performs
// a DFS (more efficient than BFS) among states with equal costs.
void SearchEngine::AddToFrontierInOrder (SearchState* state)
{
	SearchState* tmpState;
	list<SearchState*>::iterator itr;

	for (itr = frontier.begin(); itr != frontier.end(); itr++)
	{
		tmpState = *itr;
		if (tmpState->cost >= state->cost)
			break;
	}
	frontier.insert (itr, state);
}


// ----- Utility methods

list<Location>::iterator findLocation (list<Location>::iterator first, list<Location>::iterator last, const Location& val)
{
	while (first != last)
	{
		if (*first == val)
			return first;
		else first++;
	}
	return last;
}
