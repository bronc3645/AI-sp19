There is a way to get the individual pieces out of the frontier and visited just treat them like 2D arrays

Need method to calculate probability of pit given breeze, add locations to 'safe' or 'unsafe' arrays

Need to make 2D array of all locations

TODO: 
Redo arrays of safety status, location on grid to OBJECTS 

Location objects: 
self.Posx
self.Posy
Starting orientation
Final orientation 
safe (bool)
hasBreeze (bool)
visited 


calcProbabilityPit(location1)
initialize all locations to 0.2 at first 
[1,1] = safe
iterate over each location's probability; if >0.5, = unsafe 

prob of pit in middle = 60% (add to unsafe)

add frontier array that stores updated location probabilities
iteration over all frontier possibilities each time 