// Agent.cc

#include <iostream>
#include <list>
#include "Agent.h"

using namespace std;

Agent::Agent ()
{

}

Agent::~Agent ()
{

}

void Agent::Initialize ()
{
	// Works only for test world.
	// You won't initially know safe locations or world size.
	for (int x = 1; x <= 4; x++) {
		for (int y = 1; y <= 4; y++) {
			searchEngine.AddSafeLocation(x,y);
		}
	}
	searchEngine.RemoveSafeLocation(1,3); // wumpus
	searchEngine.RemoveSafeLocation(3,1); // pit
	searchEngine.RemoveSafeLocation(3,3); // pit
	searchEngine.RemoveSafeLocation(4,4); // pit

	agentHasGold = false;
	actionList.clear();
}

Action Agent::Process (Percept& percept)
{
	list<Action> actionList2;
	if (actionList.empty()) {

		// Works only for test world (you won't initially know gold location)
		if (! agentHasGold) {
			// Goto (2,3) and GRAB
			actionList2 = searchEngine.FindPath(Location(1,1), RIGHT, Location(2,3), RIGHT);
			actionList.splice(actionList.end(), actionList2);
			actionList.push_back(GRAB);
			agentHasGold = true;
		} else {
			// Goto (1,1) and CLIMB
			actionList2 = searchEngine.FindPath(Location(2,3), RIGHT, Location(1,1), RIGHT);
			actionList.splice(actionList.end(), actionList2);
			actionList.push_back(CLIMB);
		}

	}
	Action action = actionList.front();
	actionList.pop_front();
	return action;
}

void Agent::GameOver (int score)
{

}


