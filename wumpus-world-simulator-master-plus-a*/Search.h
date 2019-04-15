// Search.h
//
// A* search for wumpus world navigation.

#ifndef SEARCH_H
#define SEARCH_H

#include <list>
#include "Action.h"
#include "Percept.h"
#include "Location.h"
#include "Orientation.h"
#include "WorldState.h"

class SearchState
{
public:
	SearchState (Location& loc, Orientation& ori, int dep, SearchState* par, Action act)
	{
		location.X = loc.X;
		location.Y = loc.Y;
		orientation = ori;
		depth = dep;
		parent = par;
		action = act;
		heuristic = 0;
		cost = 0;
	}

	bool operator== (const SearchState& state);

	Location location;
	Orientation orientation;
	int depth;
	int heuristic;
	int cost;
	SearchState* parent;
	Action action; // action used to get to this state from parent state
};

class SearchEngine
{
public:
	SearchEngine () {};
	~SearchEngine () {};

	// These are the main methods:
	// - AddSafeLocation: Tell the search about locations you think are safe; the search only considers safe locations to move through.
	// - RemoveSafeLocation: If you determine a safe location is in fact not safe, then you can remove it from consideration.
	// - FindPath: The main method to call to use search to find a sequence of actions leading from start to goal only through safe locations.
	void AddSafeLocation (int x, int y);
	void RemoveSafeLocation (int x, int y);
	list<Action> FindPath (Location startLocation, Orientation startOrientation, Location goalLocation, Orientation goalOrientation);

	SearchState* Search (SearchState* initialState, SearchState* goalState);
	SearchState* AStarSearch (SearchState* initialState, SearchState* goalState);
	bool GoalTest (SearchState* state, SearchState* goalState);
	SearchState* GetChildState (SearchState* state, Action action);
	int CityBlockDistance (Location& location1, Location& location2);
	void Clear();
	bool SafeLocation (int x, int y);
	bool Visited (SearchState* state);
	void AddToFrontierInOrder (SearchState* state);

	list<SearchState*> frontier;
	list<SearchState*> explored;
	list<Location> safeLocations;
	int nodeCount;
};

list<Location>::iterator findLocation (list<Location>::iterator first, list<Location>::iterator last, const Location& val);

#endif // SEARCH_H
