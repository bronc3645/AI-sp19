// Agent.h

#ifndef AGENT_H
#define AGENT_H

#include "Action.h"
#include "Percept.h"

#include "Location.h"
#include "Orientation.h"
#include "Search.h"
#include <list>

class Agent
{
public:
	Agent ();
	~Agent ();
	void Initialize ();
	Action Process (Percept& percept);
	void GameOver (int score);

	bool agentHasGold;
	list<Action> actionList;
	SearchEngine searchEngine;
};

#endif // AGENT_H
