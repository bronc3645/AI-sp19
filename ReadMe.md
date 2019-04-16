Charlie Reger
Jerry Malcolmson
Seth Stovall
Amy Dixon

Implemented probability-based agent that calculates chance that a location contains a pit based on breeze locations in our 4x4 world. 

Variables include: 
 
lowest: variable to test which location has lowest probability of a pit. Initialized to 1.

lolocation: stores location of the lowest probability so far

breezes[]: location of each space that has breeze so when a breeze is found, the location will be added and handled in the agent's 

pits[]: location of each space that has pit 

Methods include: 

getPit(): iterates through each breeze in current breeze[] array, pops discovered breezes at x and y locations, and appends pit[] array. This method is called each iteration of the world. Currently only set to 4x4 grid.

getProb(): creates copy of breezes[] to test against and checks if breezes can be satisfied by different breeze-pit combinations. At the end of each set, the tempbreeze test array is reset so iteration over each pit-breeze combo can continue sequentially. 

Process: 

In a world with 3 possible pits, the agent should calculate the probability of each space having a pit and adds the space with lowest probability to the toVisit[] array of "safe" locations. Probabilities were calculate via brute-force in getProb(), which hardcoded 2D arrays for all possible pit-breeze combinations given .2 chance that a location has a pit and 3 pits in the grid. GetProb() increments each space to probabilities and checks every location where a pit can satisfy breeze. If a location does not satisfy breeze, then additions to total probability are not made. If a pit is found, the method checks up-down-left-right locations surrounding it, doing additions to total probability. Each breeze-pit if-check then resets the temporary breeze array to prevent duplicates, and found breezes are added to the numerator and denominator. 

Once a lowest probability is calculated in getProb(), it is compared against the current grid location's iteration of probability. If current probability is lower than previous lowest, it is replaced and Process() sets a new lolocation. If the lowest pit probability is less than 0.5, then AddSafeLocation() (Search.py) is called on that space. 

Testing: 

The agent scored 155 on average over 4000 trials with the built-in world generator. 

Conclusions: 

The probability-based agent is less cautious than its A*Search counterpart: it takes more risks, making its overall score lower than the AStarSearch agent. AStarSearch agent scores better because it does not take any risks: if any breeze is encountered, it will return to [1,1]. The probability agent searches over all spaces even if a breeze is encountered. The probability agent still performs better than the simple agent. The probability agent only calculates based on one percept (breeze), so it privileges moving over multiple spaces exclusively to avoid pits. Therefore, its likelihood of running into a Wumpus is higher than the AStarSearch agent.  